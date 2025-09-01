from django.db import models
from django.contrib.auth.models import User

class Enqueteur(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    prenom = models.CharField(max_length=100)
    nom = models.CharField(max_length=100)
    telephone = models.CharField(max_length=20)
    date_creation = models.DateTimeField(auto_now_add=True)
    actif = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.prenom} {self.nom}"

    class Meta:
        verbose_name = "Enquêteur"
        verbose_name_plural = "Enquêteurs"

class FicheMilitant(models.Model):
    # Lien avec l'enquêteur qui a fait l'enquête
    enqueteur = models.ForeignKey(Enqueteur, on_delete=models.CASCADE, related_name='fiches_militant')

    # 1. LOCALISATION
    region = models.CharField(max_length=100, verbose_name="Région")
    departement_administratif = models.CharField(max_length=100, verbose_name="Département Administratif")
    departement = models.CharField(
        max_length=100,
        default="Danané",
        verbose_name="Département"
    )
    zone = models.CharField(max_length=100, verbose_name="Zone")
    section = models.CharField(max_length=100, verbose_name="Section")
    qualite_section = models.CharField(max_length=100, blank=True, null=True, verbose_name="Qualité dans la section")
    comite_base = models.CharField(max_length=100, verbose_name="Comité de base")
    qualite_cb = models.CharField(max_length=100, blank=True, null=True, verbose_name="Qualité dans le CB")
    # CHAMPS SUPPRIMÉS : fonction_parti et poste_electif
    lieu_vote = models.CharField(max_length=150, verbose_name="Lieu de vote")

    # 2. ETAT CIVIL
    prenoms = models.CharField(max_length=200, verbose_name="Prénom(s)")
    nom = models.CharField(max_length=100, verbose_name="Nom")
    date_naissance = models.DateField(verbose_name="Date de naissance")
    lieu_naissance = models.CharField(max_length=150, verbose_name="Lieu de naissance")
    contacts = models.CharField(max_length=100, verbose_name="Contact(s)")
    email = models.EmailField(blank=True, null=True, verbose_name="Email")
    SEXE_CHOICES = [
        ('M', 'Masculin'),
        ('F', 'Féminin')
    ]
    sexe = models.CharField(max_length=1, choices=SEXE_CHOICES, verbose_name="Sexe")
    profession = models.CharField(max_length=150, verbose_name="Profession")
    fonction = models.CharField(max_length=150, blank=True, null=True, verbose_name="Fonction")

    # 3. DOCUMENT D'IDENTITE
    INSCRIPTION_CHOICES = [
        ('inscrit', 'Inscrit sur la liste électorale'),
        ('non_inscrit', 'Non inscrit sur la liste électorale')
    ]
    inscription_electorale = models.CharField(
        max_length=15,
        choices=INSCRIPTION_CHOICES,
        verbose_name="Inscription électorale"
    )

    # Types de documents
    a_cni = models.BooleanField(default=False, verbose_name="Carte Nationale d'Identité (CNI)")
    a_attestation = models.BooleanField(default=False, verbose_name="Attestation d'identité")
    a_certificat = models.BooleanField(default=False, verbose_name="Certificat de Nationalité")
    a_extrait = models.BooleanField(default=False, verbose_name="Extrait de Naissance")
    a_recepisse = models.BooleanField(default=False, verbose_name="Récépissé Nouvelle CNI")
    aucune_piece = models.BooleanField(default=False, verbose_name="Aucune Pièce")

    numero_piece = models.CharField(max_length=50, blank=True, null=True, verbose_name="Numéro de la pièce")
    numero_carte_electeur = models.CharField(max_length=50, blank=True, null=True, verbose_name="Numéro carte électeur")
    nni = models.CharField(max_length=50, blank=True, null=True, verbose_name="Numéro d'Identification Unique (NNI)")

    # Métadonnées
    date_soumission = models.DateTimeField(auto_now_add=True)
    est_dans_csv = models.BooleanField(default=False, verbose_name="Présent dans le fichier électoral")
    numero_electeur_csv = models.CharField(max_length=50, blank=True, null=True, verbose_name="Numéro électeur trouvé")

    def __str__(self):
        return f"{self.prenoms} {self.nom} - {self.date_soumission.strftime('%d/%m/%Y')}"

    class Meta:
        verbose_name = "Fiche de Militant"
        verbose_name_plural = "Fiches de Militants"
        ordering = ['-date_soumission']

# Garder l'ancien modèle pour compatibilité si nécessaire
class EnquetePolitique(models.Model):
    # Lien avec l'enquêteur qui a fait l'enquête
    enqueteur = models.ForeignKey(Enqueteur, on_delete=models.CASCADE, related_name='enquetes')

    # Informations personnelles
    prenom = models.CharField(max_length=100)
    nom = models.CharField(max_length=100)
    age = models.PositiveIntegerField()
    sexe = models.CharField(max_length=1, choices=[('M', 'Masculin'), ('F', 'Féminin')])
    contact = models.CharField(max_length=50)
    email = models.EmailField(blank=True, null=True)
    profession = models.CharField(max_length=150)
    niveau_etudes = models.CharField(
        max_length=20,
        choices=[
            ('primaire', 'Primaire'),
            ('secondaire', 'Secondaire'),
            ('superieur', 'Supérieur'),
            ('aucun', 'Aucun')
        ],
        blank=True,
        null=True
    )

    # Localisation électorale
    region = models.CharField(max_length=100)
    departement = models.CharField(
        max_length=100,
        default="Danané",
        editable=False
    )

    SOUS_PREF_CHOICES = [
        ("Danané", "Danané"),
        ("Daleu", "Daleu"),
        ("Kouan-Houlé", "Kouan-Houlé"),
        ("Gbon-Houyé", "Gbon-Houyé"),
        ("Seileu", "Seileu"),
    ]
    commune = models.CharField(max_length=100, choices=SOUS_PREF_CHOICES)

    lieu_vote = models.CharField(max_length=150)
    carte_electeur = models.CharField(max_length=50, blank=True, null=True)

    # Opinion politique
    parti = models.CharField(max_length=100)
    candidat = models.CharField(max_length=100)
    attentes = models.TextField(blank=True, null=True)

    date_soumission = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.prenom} {self.nom} - {self.date_soumission.strftime('%d/%m/%Y')}"

    class Meta:
        verbose_name = "Enquête Politique"
        verbose_name_plural = "Enquêtes Politiques"
        ordering = ['-date_soumission']