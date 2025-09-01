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
    list_display = ('prenom', 'nom', 'user', 'telephone', 'actif', 'date_creation', 'nombre_fiches', 'fiches_csv')
    list_filter = ('actif', 'date_creation')
    search_fields = ('prenom', 'nom', 'user__username', 'user__email', 'telephone')
    readonly_fields = ('date_creation', 'nombre_fiches', 'fiches_csv')

    fieldsets = (
        ('Informations personnelles', {
            'fields': ('prenom', 'nom', 'telephone')
        }),
        ('Compte utilisateur', {
            'fields': ('user',)
        }),
        ('Statistiques', {
            'fields': ('actif', 'date_creation', 'nombre_fiches', 'fiches_csv')
        }),
    )

    def nombre_fiches(self, obj):
        return obj.fiches_militant.count()
    nombre_fiches.short_description = "Total fiches"

    def fiches_csv(self, obj):
        total = obj.fiches_militant.count()
        dans_csv = obj.fiches_militant.filter(est_dans_csv=True).count()
        if total > 0:
            pourcentage = (dans_csv / total) * 100
            return f"{dans_csv}/{total} ({pourcentage:.0f}%)"
        return "0/0"
    fiches_csv.short_description = "Fiches dans CSV"

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        # Synchroniser les informations de l'utilisateur
        if obj.user:
            obj.user.first_name = obj.prenom
            obj.user.last_name = obj.nom
            obj.user.save()

@admin.register(FicheMilitant)
class FicheMilitantAdmin(admin.ModelAdmin):
    list_display = ('prenoms', 'nom', 'sexe', 'region', 'section', 'enqueteur',
                    'statut_csv', 'numero_electeur_csv', 'date_soumission')
    list_filter = ('sexe', 'region', 'departement', 'inscription_electorale',
                   'enqueteur', 'est_dans_csv', 'date_soumission')
    search_fields = ('prenoms', 'nom', 'contacts', 'section', 'comite_base',
                     'enqueteur__prenom', 'enqueteur__nom', 'numero_carte_electeur', 'numero_electeur_csv')
    readonly_fields = ('date_soumission', 'est_dans_csv', 'numero_electeur_csv')

    fieldsets = (
        ('Enquêteur', {
            'fields': ('enqueteur',)
        }),
        ('Statut électoral', {
            'fields': ('est_dans_csv', 'numero_electeur_csv'),
            'description': 'Indique si la personne a été trouvée dans le fichier électoral CSV'
        }),
        ('1. Localisation', {
            'fields': (
                'region', 'departement_administratif', 'departement', 'zone',
                'section', 'qualite_section', 'comite_base', 'qualite_cb',
                'lieu_vote'  # Supprimé: fonction_parti et poste_electif
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

    def statut_csv(self, obj):
        if obj.est_dans_csv:
            return "✅ Électeur connu"
        return "🆕 Nouveau"
    statut_csv.short_description = "Statut CSV"
    statut_csv.admin_order_field = 'est_dans_csv'

    actions = ['export_fiches_csv']

    def export_fiches_csv(self, request, queryset):
        """Action pour exporter les fiches sélectionnées en CSV"""
        import csv
        from django.http import HttpResponse

        response = HttpResponse(content_type='text/csv; charset=utf-8')
        response['Content-Disposition'] = 'attachment; filename="fiches_militants_export.csv"'
        response.write('\ufeff')  # BOM pour Excel

        writer = csv.writer(response)
        writer.writerow([
            'Nom', 'Prénoms', 'Date Naissance', 'Lieu Naissance',
            'Sexe', 'Contacts', 'Section', 'Comité de Base',
            'Dans CSV', 'N° Électeur CSV', 'Enquêteur', 'Date Soumission'
        ])

        for fiche in queryset:
            writer.writerow([
                fiche.nom,
                fiche.prenoms,
                fiche.date_naissance.strftime('%d/%m/%Y') if fiche.date_naissance else '',
                fiche.lieu_naissance or '',
                fiche.get_sexe_display(),
                fiche.contacts,
                fiche.section,
                fiche.comite_base,
                'Oui' if fiche.est_dans_csv else 'Non',
                fiche.numero_electeur_csv or '',
                f"{fiche.enqueteur.prenom} {fiche.enqueteur.nom}",
                fiche.date_soumission.strftime('%d/%m/%Y %H:%M')
            ])

        return response

    export_fiches_csv.short_description = "Exporter les fiches sélectionnées en CSV"

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
admin.site.site_header = "Administration des Fiches Militants"
admin.site.site_title = "Admin Militants"
admin.site.index_title = "Gestion des Fiches de Militants"