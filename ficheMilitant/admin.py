from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from .models import Enqueteur, FicheMilitant, EnquetePolitique

class EnqueteurInline(admin.StackedInline):
    model = Enqueteur
    can_delete = False
    verbose_name_plural = 'Informations Enquêteur'
    fields = ('prenom', 'nom', 'telephone', 'actif')

class EnqueteurUserAdmin(UserAdmin):
    """Administration personnalisée pour les utilisateurs enquêteurs"""
    inlines = (EnqueteurInline,)
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_active', 'get_enqueteur_info')
    list_filter = ('is_active', 'date_joined', 'enqueteur__actif')
    search_fields = ('username', 'email', 'enqueteur__prenom', 'enqueteur__nom')

    def get_enqueteur_info(self, obj):
        try:
            enqueteur = obj.enqueteur
            return f"{enqueteur.prenom} {enqueteur.nom} ({'Actif' if enqueteur.actif else 'Inactif'})"
        except Enqueteur.DoesNotExist:
            return "Non enquêteur"
    get_enqueteur_info.short_description = "Info Enquêteur"

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('enqueteur')

@admin.register(Enqueteur)
class EnqueteurAdmin(admin.ModelAdmin):
    list_display = ('prenom', 'nom', 'user', 'telephone', 'actif', 'date_creation', 'nombre_fiches')
    list_filter = ('actif', 'date_creation')
    search_fields = ('prenom', 'nom', 'user__username', 'user__email', 'telephone')
    readonly_fields = ('date_creation', 'nombre_fiches')

    fieldsets = (
        ('Informations personnelles', {
            'fields': ('prenom', 'nom', 'telephone')
        }),
        ('Compte utilisateur', {
            'fields': ('user',)
        }),
        ('Statut', {
            'fields': ('actif', 'date_creation', 'nombre_fiches')
        }),
    )

    def nombre_fiches(self, obj):
        return obj.fiches_militant.count()
    nombre_fiches.short_description = "Nombre de fiches"

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        # Synchroniser les informations de l'utilisateur
        if obj.user:
            obj.user.first_name = obj.prenom
            obj.user.last_name = obj.nom
            obj.user.save()

@admin.register(FicheMilitant)
class FicheMilitantAdmin(admin.ModelAdmin):
    list_display = ('prenoms', 'nom', 'sexe', 'region', 'section', 'enqueteur', 'date_soumission')
    list_filter = ('sexe', 'region', 'departement', 'inscription_electorale', 'enqueteur', 'date_soumission')
    search_fields = ('prenoms', 'nom', 'contacts', 'section', 'comite_base', 'enqueteur__prenom', 'enqueteur__nom')
    readonly_fields = ('date_soumission',)

    fieldsets = (
        ('Enquêteur', {
            'fields': ('enqueteur',)
        }),
        ('1. Localisation', {
            'fields': (
                'region', 'departement_administratif', 'departement', 'zone',
                'section', 'qualite_section', 'comite_base', 'qualite_cb',
                'fonction_parti', 'lieu_vote', 'poste_electif'
            )
        }),
        ('2. État Civil', {
            'fields': (
                'prenoms', 'nom', 'date_naissance', 'lieu_naissance',
                'contacts', 'email', 'sexe', 'profession', 'fonction'
            )
        }),
        ('3. Document d\'Identité', {
            'fields': (
                'inscription_electorale',
                ('a_cni', 'a_attestation', 'a_certificat'),
                ('a_extrait', 'a_recepisse', 'aucune_piece'),
                'numero_piece', 'numero_carte_electeur', 'nni'
            )
        }),
        ('Métadonnées', {
            'fields': ('date_soumission',),
            'classes': ('collapse',)
        }),
    )

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('enqueteur', 'enqueteur__user')

# Garder l'ancien modèle pour compatibilité
@admin.register(EnquetePolitique)
class EnquetePolitiqueAdmin(admin.ModelAdmin):
    list_display = ('prenom', 'nom', 'age', 'commune', 'parti', 'candidat', 'enqueteur', 'date_soumission')
    list_filter = ('commune', 'parti', 'sexe', 'niveau_etudes', 'enqueteur', 'date_soumission')
    search_fields = ('prenom', 'nom', 'contact', 'parti', 'candidat', 'enqueteur__prenom', 'enqueteur__nom')
    readonly_fields = ('date_soumission', 'departement')

    fieldsets = (
        ('Enquêteur', {
            'fields': ('enqueteur',)
        }),
        ('Informations personnelles', {
            'fields': ('prenom', 'nom', 'age', 'sexe', 'contact', 'email', 'profession', 'niveau_etudes')
        }),
        ('Localisation électorale', {
            'fields': ('region', 'departement', 'commune', 'lieu_vote', 'carte_electeur')
        }),
        ('Opinion politique', {
            'fields': ('parti', 'candidat', 'attentes')
        }),
        ('Métadonnées', {
            'fields': ('date_soumission',),
            'classes': ('collapse',)
        }),
    )

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('enqueteur', 'enqueteur__user')

# Désenregistrer le UserAdmin par défaut et enregistrer le nôtre
admin.site.unregister(User)
admin.site.register(User, EnqueteurUserAdmin)

# Configuration du site admin
admin.site.site_header = "Administration des Fiches Militants "
admin.site.site_title = "Admin Militants"
admin.site.index_title = "Gestion des Fiches de Militants"