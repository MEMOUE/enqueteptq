# ficheMilitant/zone_lieu_utils.py

"""
Utilitaire pour gérer les zones et lieux de vote.
Les données sont intégrées directement dans le code pour éviter
la dépendance à un fichier Excel externe.

DONNÉES COMPLÈTES : 1 zone (MAN), 67 lieux de vote
"""

# Données complètes des zones et lieux de vote (extraction du fichier sous_prefectures_selection.csv de Man)
ZONES_LIEUX_DATA = {
    'MAN': [
        'APPATAM GOULEDEPLEU',
        'APPATAM PLOUBA',
        'APPATAM TIAGBEPLEU',
        'CAFOP DE MAN',
        'CENTRE SOCIAL GRAND GBAPLEU',
        'COLLEGE BLON BLAISE',
        'COLLEGE CATHOLIQUE JEAN DE LA MENNAIS',
        'COLLEGE MODERNE 2 GBE GOULEY ALPHONSE',
        'COLLEGE MODERNE JEUNE FILLE DOMINIQUE OUATTARA',
        'COLLEGE MODERNE MOUSSA KONE',
        'COLLEGE OPERI EMILE DOMORAUD',
        'COLLEGE PRIVE DIAWAR',
        'COLLEGE SIA ANDRE',
        'COLLEGE SUNGA DE GOGNAN',
        'COMPLEXE SOCIO-EDUCATIF DIOULABOUGOU',
        'ECOLE CONFESSIONNELLE SABIL HIDAYA',
        'ECOLE D\'EDUCATION ARABE',
        'EPC VOUNGOUE',
        'EPP BANTEGOUIN',
        'EPP BIGOUIN',
        'EPP BLOLE',
        'EPP BOTONGOUINE',
        'EPP CNPS',
        'EPP DAYNE',
        'EPP DIOULABOUGOU',
        'EPP GBATONGOUIN',
        'EPP GOUAKPALE',
        'EPP GOUIMPLEU',
        'EPP GUEUPLEU',
        'EPP KASSIAPLEU I',
        'EPP KENNEDY',
        'EPP KPANGOUIN 2',
        'EPP LIBREVILLE 4',
        'EPP MELAPLEU',
        'EPP ZADEPLEU',
        'EPP ZEREGOUIN',
        'GARE ROUTIERE TOUBA',
        'GROUPE SCOLAIRE BIELE',
        'GROUPE SCOLAIRE CATHOLIQUE MAN-FILLE',
        'GROUPE SCOLAIRE CATHOLIQUE STE-THERESE',
        'GROUPE SCOLAIRE CLUB',
        'GROUPE SCOLAIRE DOCTEUR ALBERT FLINDE DU CAMPUS',
        'GROUPE SCOLAIRE DOMAINE MISTROT',
        'GROUPE SCOLAIRE DOMPLEU',
        'GROUPE SCOLAIRE GBEPLEU',
        'GROUPE SCOLAIRE GLONGOUIN 1-2-3',
        'GROUPE SCOLAIRE GRAND GBAPLEU',
        'GROUPE SCOLAIRE GUIANLE',
        'GROUPE SCOLAIRE KIELE',
        'GROUPE SCOLAIRE KOGOUIN',
        'GROUPE SCOLAIRE KOKO 1-2-3-4',
        'GROUPE SCOLAIRE KPANGOUIN 1',
        'GROUPE SCOLAIRE KRIKOUMA',
        'GROUPE SCOLAIRE LIBREVILLE 1-2-3',
        'GROUPE SCOLAIRE MONGLAS',
        'GROUPE SCOLAIRE PROTESTANTE',
        'GROUPE SCOLAIRE TEMOIN DOYAGOUINE',
        'GROUPE SCOLAIRE ZELE',
        'GS BLOKOSSO C.H.R',
        'GS PERALDI',
        'GS PETIT GBAPLEU',
        'GS SAINT-MICHEL',
        'IFTG',
        'INSTITUT DAROUL FOURQUANE',
        'LYCEE MODERNE DION ROBERT',
        'LYCEE MODERNE JACQUET DROH FLAURENT',
        'LYCEE PROFESSIONELLE DE MAN',
    ]
}

def charger_zones_lieux():
    """
    Retourne les données des zones et lieux de vote.
    Les données sont maintenant intégrées directement dans le code.
    """
    # Copier les données pour éviter les modifications accidentelles
    zones_lieux = {}
    for zone, lieux in ZONES_LIEUX_DATA.items():
        zones_lieux[zone] = sorted(lieux.copy())  # Trier les lieux par ordre alphabétique

    print(f"[INFO] Zones chargées : {list(zones_lieux.keys())}")
    print(f"[INFO] Total lieux de vote : {sum(len(lieux) for lieux in zones_lieux.values())}")

    return zones_lieux

def get_lieux_vote_par_zone(zone):
    """
    Retourne la liste des lieux de vote pour une zone donnée
    """
    zones_lieux = charger_zones_lieux()
    return zones_lieux.get(zone, [])

def get_toutes_zones():
    """
    Retourne toutes les zones disponibles
    """
    return list(ZONES_LIEUX_DATA.keys())

def get_tous_lieux_vote():
    """
    Retourne tous les lieux de vote (toutes zones confondues)
    """
    tous_lieux = []
    for lieux in ZONES_LIEUX_DATA.values():
        tous_lieux.extend(lieux)
    return sorted(list(set(tous_lieux)))

# Cache pour éviter de recréer les données à chaque fois
_cache_zones_lieux = None

def get_zones_lieux_cached():
    """
    Version mise en cache pour de meilleures performances
    """
    global _cache_zones_lieux
    if _cache_zones_lieux is None:
        _cache_zones_lieux = charger_zones_lieux()
    return _cache_zones_lieux

def get_zones_choices():
    """
    Retourne les choix de zones pour les formulaires Django
    """
    zones = get_toutes_zones()
    choices = [('', 'Sélectionner une zone')]
    for zone in sorted(zones):
        choices.append((zone, zone))
    return choices

def get_statistiques():
    """
    Retourne des statistiques sur les zones et lieux de vote
    """
    zones_lieux = get_zones_lieux_cached()
    stats = {
        'total_zones': len(zones_lieux),
        'total_lieux': sum(len(lieux) for lieux in zones_lieux.values()),
        'repartition_par_zone': {zone: len(lieux) for zone, lieux in zones_lieux.items()},
        'zone_plus_lieux': max(zones_lieux.items(), key=lambda x: len(x[1]))[0] if zones_lieux else None,
        'zone_moins_lieux': min(zones_lieux.items(), key=lambda x: len(x[1]))[0] if zones_lieux else None
    }
    return stats

def tester_chargement():
    """
    Fonction de test pour vérifier le chargement des données
    """
    print("\n=== TEST DE CHARGEMENT ZONES-LIEUX ===")
    print("Source: Données intégrées dans le code Python")

    zones_lieux = charger_zones_lieux()
    stats = get_statistiques()

    print(f"\nNombre de zones trouvées : {stats['total_zones']}")
    print(f"Total des lieux de vote : {stats['total_lieux']}")

    print(f"\nRépartition par zone :")
    for zone, nombre in stats['repartition_par_zone'].items():
        print(f"  [{zone}] - {nombre} lieux de vote")

    if stats['zone_plus_lieux']:
        print(f"\nZone avec le plus de lieux : {stats['zone_plus_lieux']} ({stats['repartition_par_zone'][stats['zone_plus_lieux']]} lieux)")
    if stats['zone_moins_lieux']:
        print(f"Zone avec le moins de lieux : {stats['zone_moins_lieux']} ({stats['repartition_par_zone'][stats['zone_moins_lieux']]} lieux)")

    # Afficher quelques exemples de lieux par zone
    print(f"\nExemples de lieux par zone :")
    for zone, lieux in zones_lieux.items():
        print(f"  [{zone}] : {', '.join(lieux[:3])}{'...' if len(lieux) > 3 else ''}")

    print("\n=== FIN DU TEST ===")

if __name__ == "__main__":
    tester_chargement()