# ficheMilitant/csv_utils.py

import csv
import os
from django.conf import settings
from datetime import datetime
import unicodedata

# Chemin vers le fichier CSV
CSV_FILE_PATH = os.path.join(settings.BASE_DIR, 'data', 'sous_prefectures_selection.csv')

def normalize_text(text):
    """Normalise le texte pour la comparaison (enlève accents, met en majuscules)"""
    if not text:
        return ""
    # Enlever les accents
    text = unicodedata.normalize('NFD', str(text))
    text = ''.join(char for char in text if unicodedata.category(char) != 'Mn')
    # Mettre en majuscules et enlever les espaces superflus
    return text.upper().strip()

def convert_date_format(date_str):
    """Convertit différents formats de date vers DD/MM/YYYY"""
    if not date_str:
        return ""

    # Si c'est un objet date Django
    if hasattr(date_str, 'strftime'):
        return date_str.strftime('%d/%m/%Y')

    date_str = str(date_str)

    # Si c'est déjà au bon format
    if '/' in date_str:
        return date_str

    # Si c'est au format YYYY-MM-DD
    if '-' in date_str:
        try:
            # Format standard Django
            date_obj = datetime.strptime(date_str, '%Y-%m-%d')
            return date_obj.strftime('%d/%m/%Y')
        except:
            pass

    return date_str

def verifier_personne_dans_csv(nom, prenoms, date_naissance=None, lieu_naissance=None):
    """
    Vérifie si une personne existe dans le fichier CSV
    Retourne un dictionnaire avec les informations trouvées ou None
    """

    print(f"[DEBUG] Recherche dans CSV : {nom} {prenoms}, né le {date_naissance} à {lieu_naissance}")
    print(f"[DEBUG] Fichier CSV : {CSV_FILE_PATH}")

    # Vérifier si le fichier existe
    if not os.path.exists(CSV_FILE_PATH):
        print(f"[ERREUR] Fichier CSV non trouvé : {CSV_FILE_PATH}")
        return {'trouve': False, 'message': 'Fichier CSV non trouvé'}

    # Normaliser les données de recherche
    nom_recherche = normalize_text(nom)
    prenoms_recherche = normalize_text(prenoms)
    date_recherche = convert_date_format(date_naissance) if date_naissance else ""
    lieu_recherche = normalize_text(lieu_naissance) if lieu_naissance else ""

    print(f"[DEBUG] Données normalisées : NOM={nom_recherche}, PRENOMS={prenoms_recherche}, DATE={date_recherche}, LIEU={lieu_recherche}")

    lignes_parcourues = 0
    personne_trouvee = False

    try:
        # Essayer différents encodages
        encodings = ['utf-8', 'latin-1', 'cp1252', 'iso-8859-1']

        for encoding in encodings:
            try:
                with open(CSV_FILE_PATH, 'r', encoding=encoding) as file:
                    # Lire les premières lignes pour détecter le délimiteur
                    sample = file.read(1024)
                    file.seek(0)

                    # Détecter le délimiteur (probablement ;)
                    delimiter = ';'  # Par défaut pour votre CSV
                    if '\t' in sample and ';' not in sample:
                        delimiter = '\t'
                    elif ',' in sample and ';' not in sample:
                        delimiter = ','

                    print(f"[DEBUG] Encodage: {encoding}, Délimiteur détecté: '{delimiter}'")

                    reader = csv.DictReader(file, delimiter=delimiter)

                    # Afficher les colonnes trouvées (une seule fois)
                    if lignes_parcourues == 0:
                        print(f"[DEBUG] Colonnes du CSV : {reader.fieldnames}")

                    for row in reader:
                        lignes_parcourues += 1

                        # Normaliser les données du CSV
                        nom_csv = normalize_text(row.get('Nom/Nom de Jeune Fille', ''))
                        prenoms_csv = normalize_text(row.get('Prenoms', ''))
                        date_csv = row.get('Date de Naissance', '').strip()
                        lieu_csv = normalize_text(row.get('Lieu de Naissance', ''))

                        # Afficher les premières lignes pour debug
                        if lignes_parcourues <= 3:
                            print(f"[DEBUG] Ligne {lignes_parcourues}: {nom_csv} {prenoms_csv}, {date_csv}, {lieu_csv}")

                        # Comparaison exacte (pas de "in", mais égalité)
                        match_nom = nom_recherche == nom_csv
                        match_prenoms = prenoms_recherche == prenoms_csv

                        # Si nom et prénoms correspondent exactement
                        if match_nom and match_prenoms:
                            print(f"[DEBUG] ✅ Correspondance NOM et PRENOMS trouvée !")

                            # Vérifier les critères supplémentaires si fournis
                            if date_recherche and date_csv and date_csv != 'inconnu':
                                if date_recherche != date_csv:
                                    print(f"[DEBUG] ❌ Date ne correspond pas : {date_recherche} != {date_csv}")
                                    continue
                                else:
                                    print(f"[DEBUG] ✅ Date correspond aussi")

                            if lieu_recherche and lieu_csv and lieu_csv != 'INCONNU':
                                # Pour le lieu, on peut être plus flexible
                                if lieu_recherche not in lieu_csv and lieu_csv not in lieu_recherche:
                                    print(f"[DEBUG] ❌ Lieu ne correspond pas : {lieu_recherche} != {lieu_csv}")
                                    continue
                                else:
                                    print(f"[DEBUG] ✅ Lieu correspond aussi")

                            # Personne trouvée !
                            personne_trouvee = True
                            numero_electeur = row.get('Numero Electeur', '').strip()

                            print(f"[DEBUG] 🎉 PERSONNE TROUVÉE ! Numéro électeur : {numero_electeur}")

                            return {
                                'trouve': True,
                                'nom': row.get('Nom/Nom de Jeune Fille', ''),
                                'prenoms': row.get('Prenoms', ''),
                                'numero_electeur': numero_electeur,
                                'sexe': row.get('Sexe', ''),
                                'date_naissance': row.get('Date de Naissance', ''),
                                'lieu_naissance': row.get('Lieu de Naissance', ''),
                                'commune': row.get('Libelle Commune', ''),
                                'lieu_vote': row.get('Libelle Lieu de Vote', ''),
                                'bureau_vote': row.get('Bureau de vote', ''),
                                'profession': row.get('Profession', ''),
                                'adresse': row.get('Adresse Physique', '')
                            }

                    # Si on arrive ici, la personne n'a pas été trouvée
                    print(f"[DEBUG] ❌ Personne non trouvée après {lignes_parcourues} lignes")
                    return {'trouve': False}

            except UnicodeDecodeError:
                print(f"[DEBUG] Erreur d'encodage avec {encoding}, essai suivant...")
                continue
            except Exception as e:
                print(f"[ERREUR] Erreur avec l'encodage {encoding}: {e}")
                continue

    except Exception as e:
        print(f"[ERREUR] Erreur générale lors de la lecture du CSV : {e}")
        return {'trouve': False, 'message': str(e)}

    print(f"[DEBUG] Fin de recherche - Personne non trouvée")
    return {'trouve': False}

def compter_electeurs_csv():
    """Compte le nombre total d'électeurs dans le CSV"""
    if not os.path.exists(CSV_FILE_PATH):
        print(f"[DEBUG] Fichier CSV non trouvé pour comptage")
        return 0

    count = 0
    try:
        encodings = ['utf-8', 'latin-1', 'cp1252']
        for encoding in encodings:
            try:
                with open(CSV_FILE_PATH, 'r', encoding=encoding) as file:
                    # Utiliser ; comme délimiteur par défaut
                    reader = csv.DictReader(file, delimiter=';')
                    for row in reader:
                        if row.get('Nom/Nom de Jeune Fille') and row.get('Prenoms'):
                            count += 1
                print(f"[DEBUG] Total électeurs dans CSV : {count}")
                return count
            except:
                continue
    except Exception as e:
        print(f"[ERREUR] Erreur lors du comptage : {e}")

    return count

# Fonction de test pour vérifier que le CSV est bien lu
def tester_lecture_csv():
    """Fonction de test pour vérifier la lecture du CSV"""
    print("\n=== TEST DE LECTURE DU CSV ===")
    print(f"Chemin du fichier : {CSV_FILE_PATH}")
    print(f"Le fichier existe : {os.path.exists(CSV_FILE_PATH)}")

    if os.path.exists(CSV_FILE_PATH):
        try:
            with open(CSV_FILE_PATH, 'r', encoding='utf-8') as file:
                # Lire les 5 premières lignes
                for i, line in enumerate(file):
                    if i >= 5:
                        break
                    print(f"Ligne {i+1}: {line[:100]}...")  # Afficher les 100 premiers caractères
        except Exception as e:
            print(f"Erreur lors de la lecture : {e}")

    print("\nNombre total d'électeurs : ", compter_electeurs_csv())

    # Tester avec une personne connue
    print("\n=== TEST AVEC ABA MICHEL ===")
    resultat = verifier_personne_dans_csv("ABA", "MICHEL", "01/01/1993", "DANANE")
    print(f"Résultat : {resultat}")

    print("\n=== FIN DES TESTS ===\n")