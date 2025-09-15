# ficheMilitant/zone_lieu_utils.py

"""
Utilitaire pour gérer les zones et lieux de vote.
Les données sont intégrées directement dans le code pour éviter
la dépendance à un fichier Excel externe.

DONNÉES COMPLÈTES : 6 zones, 166 lieux de vote
"""

# Données complètes des zones et lieux de vote (extraction exhaustive de Zone_LieudeVote.xlsx)
ZONES_LIEUX_DATA = {
    'DALEU': [
        'EPP BLEUPLEU',
        'EPP BOUIMPLEU',
        'EPP DALEU 1',
        'EPP DANTONGOUINE',
        'EPP DIEMPLEU',
        'EPP DOUANGOPLEU',
        'EPP DOUAPLEU',
        'EPP DOUELEU',
        'EPP GBANLEU',
        'EPP GOPLEU',
        'EPP GOUEUPOUTA',
        'EPP GUIZREU',
        'EPP KATA',
        'EPP MLIMBA',
        'EPP NIMPLEU 1',
        'EPP NIMPLEU 2',
        'EPP PAULKRO',
        'EPP SOUABA',
        'EPP YALEGBEUPLEU',
        'EPP YANGUILEU',
        'EPP YASSEGOUINE',
        'EPP ZEREGOUINE',
        'EPP ZOUPLEU',
        'PLACE PUBLIQUE GBLINZEHIBA',
        'TIAPLEU'
    ],
    'DANANE': [
        'COLLEGE BABARA WELLER',
        'COLLEGE DIETY FELIX',
        'COLLEGE LES MERITANTS',
        'COLLEGE PRIVE SANKHORE',
        'ECOLE FRANCO-ARABE',
        'ECOLE FRANCO-ARABE DE GONTIPLEU',
        'EPP BLIZREU',
        'EPP BOUAGLEU 1',
        'EPP BOULEU',
        'EPP DEAGBALOUPLEU',
        'EPP DIOTOUO',
        'EPP DIOULABOUGOU 2',
        'EPP DONGOUINE',
        'EPP DOUGBOLEU',
        'EPP DRONGOUINE',
        'EPP DRONGOUINE 2',
        'EPP GANHIBA',
        'EPP GOUALEU',
        'EPP GUEIVILLE',
        'EPP GUIALOPLEU',
        'EPP HOUPHOUETVILLE TP',
        'EPP KINNEU',
        'EPP KOYATROGBEUPLEU',
        'EPP KPAKIEPLEU',
        'EPP LEKPEAVILLE',
        'EPP SOGALE',
        'EPP TIEUKPOLOPLEU',
        'EPP TRODELEPLEU NANTA',
        'EPP TROKOLIMPLEU',
        'EPP TROUIMPLEU',
        'EPP YOLEU',
        'EPP ZOLEU 1',
        'GROUPE SCOLAIRE COMMERCE',
        'GROUPE SCOLAIRE DANANE VILLAGE',
        'GROUPE SCOLAIRE LAPLEU',
        'GS BLESSALEU',
        'GS DIOULABOUGOU 1-3',
        'GS GNINGLEU',
        'GS HOUPHOUET-VILLE',
        'GS MISSION CATHOLIQUE',
        'GS MORIBADOUGOU',
        'GS PROTESTANT',
        'JARDIN D\'ENFANTS',
        'LYCEE MODERNE ZINGBE MATHIAS',
        'MATERNELLE HOUPHOUETVILLE',
        'PLACE PUBLIC TOUAGOPLEU',
        'PLACE PUBLIQUE TROZANDEPLEU',
        'PLACE PUBLIQUE ZOLEU 2'
    ],
    'DANANE SP': [
        'EPP DEAHOUEPLEU',
        'EPP DIETTA',
        'EPP GAHAPLEU',
        'EPP GBALLEU',
        'EPP GBEUNTA',
        'EPP GOUEGBEUPLEU',
        'EPP GUIAPLEU',
        'EPP GUIN-HOUYE',
        'EPP GUISSIPLEU',
        'EPP KEDERE',
        'EPP PEPLEU 2',
        'EPP SALEUPLEU',
        'EPP SALLEU',
        'EPP SIOBA',
        'EPP YELEU',
        'EPP YEPLEU',
        'GROUPE SCOLAIRE GOUTRO',
        'PLACE PUBLIQUE BEATRO',
        'PLACE PUBLIQUE BEHIPLEU',
        'PLACE PUBLIQUE DOUAPLEU',
        'PLACE PUBLIQUE GBEADAPLEU',
        'PLACE PUBLIQUE GOLEU',
        'PLACE PUBLIQUE KANAPLEU',
        'PLACE PUBLIQUE KPANGUIDOUOPLEU',
        'PLACE PUBLIQUE MOUATOUO',
        'PLACE PUBLIQUE OUYALEU'
    ],
    'GBON-HOUYE': [
        'EPP BIEUPLEU',
        'EPP BONTRO',
        'EPP DANIPLEU',
        'EPP DANKOUAMPLEU',
        'EPP DOUALEU',
        'EPP GBANTOPLEU',
        'EPP GBETA',
        'EPP GBON-HOUYE',
        'EPP GUIAN-HOUYE',
        'EPP KANTA-YOLE',
        'EPP KPON-HOUYE',
        'EPP TOUOPLEU',
        'EPP YEALE',
        'GROUPE SCOLAIRE GLAN-HOUYE',
        'PLACE PUBLIQUE DROPLEU 2',
        'PLACE PUBLIQUE GNINGLIPLEU'
    ],
    'KOUAN-HOULE': [
        'EPP BAMPLEU',
        'EPP BOUAN-HOUYE',
        'EPP DOHOUBA',
        'EPP FEAPLEU',
        'EPP FLAMPLEU 2',
        'EPP GBATA',
        'EPP GOPOUPLEU',
        'EPP GOUELEU',
        'EPP GUETTA',
        'EPP GUEUPLEU',
        'EPP GUEUTAGBEUPLEU',
        'EPP GUEUTEAGBEUPLEU',
        'EPP KOHIBA',
        'EPP KOUAN HOULE 3',
        'EPP KPOLEU',
        'EPP LAMPLEU',
        'EPP NATTA',
        'EPP OUMPLEUPLEU',
        'EPP SORYDOUGOU',
        'EPP TIEPLEU 2',
        'EPP TIEUPLEU 1',
        'EPP ZANKAGLEU',
        'EPP ZEALE',
        'GROUPE SCOLAIRE GBAPLEU',
        'GROUPE SCOLAIRE KPANPLEU-SIN-HOUYE',
        'GS KOUAN-HOULE',
        'PLACE PUBLIQUE GBLEUPLEU',
        'PLACE PUBLIQUE MAMPLEU'
    ],
    'SEILEU': [
        'EPP DOPLEU',
        'EPP FIEUPLEU',
        'EPP GUEUDOLOUPLEU',
        'EPP KPANZEGUEPLEU',
        'EPP MESSAMPLEU',
        'EPP SOHOUPLEU',
        'EPP TONNONTOUO',
        'EPP TRON-HOUNIEN',
        'EPP VIPLEU',
        'EPP YOTTA',
        'EPP ZAN-HOUNIEN',
        'EPP ZANGBATOUO',
        'EPP ZEUGUETOUO',
        'GROUPE SCOLAIRE BOUNTA',
        'GROUPE SCOLAIRE GNIAMPLEU',
        'GROUPE SCOLAIRE KANTA',
        'GROUPE SCOLAIRE SEILEU',
        'PLACE PUBLIQUE BANZANDEPLEU',
        'PLACE PUBLIQUE DOUATOUO',
        'PLACE PUBLIQUE KONGATOUO',
        'PLACE PUBLIQUE KPEAPLEU',
        'PLACE PUBLIQUE LOLLEU',
        'PLACE PUBLIQUE YELLEU'
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
        'zone_plus_lieux': max(zones_lieux.items(), key=lambda x: len(x[1]))[0],
        'zone_moins_lieux': min(zones_lieux.items(), key=lambda x: len(x[1]))[0]
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

    print(f"\nZone avec le plus de lieux : {stats['zone_plus_lieux']} ({stats['repartition_par_zone'][stats['zone_plus_lieux']]} lieux)")
    print(f"Zone avec le moins de lieux : {stats['zone_moins_lieux']} ({stats['repartition_par_zone'][stats['zone_moins_lieux']]} lieux)")

    # Afficher quelques exemples de lieux par zone
    print(f"\nExemples de lieux par zone :")
    for zone, lieux in zones_lieux.items():
        print(f"  [{zone}] : {', '.join(lieux[:3])}{'...' if len(lieux) > 3 else ''}")

    print("\n=== FIN DU TEST ===")

if __name__ == "__main__":
    tester_chargement()