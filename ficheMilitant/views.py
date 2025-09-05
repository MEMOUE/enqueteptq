# ficheMilitant/views.py

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import HttpResponse
from django.template import loader
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from PIL import Image
import os
from .forms import FicheMilitantForm, EnquetePolitiqueForm
from .models import Enqueteur, FicheMilitant
from .csv_utils import verifier_personne_dans_csv, compter_electeurs_csv

def ficheMilitant(request):
    template = loader.get_template('login.html')
    return HttpResponse(template.render())

def fiche(request):
    fiche = loader.get_template('fiche.html')
    return HttpResponse(fiche.render())

def optimize_image(image_file, max_size=(800, 800), quality=85):
    """
    Optimise une image en la redimensionnant et en réduisant la qualité
    """
    try:
        with Image.open(image_file) as img:
            # Convertir en RGB si nécessaire
            if img.mode in ('RGBA', 'LA', 'P'):
                img = img.convert('RGB')

            # Redimensionner si l'image est trop grande
            img.thumbnail(max_size, Image.Resampling.LANCZOS)

            # Sauvegarder dans un buffer
            from io import BytesIO
            buffer = BytesIO()
            img.save(buffer, format='JPEG', quality=quality, optimize=True)
            buffer.seek(0)

            return ContentFile(buffer.read())
    except Exception as e:
        print(f"Erreur lors de l'optimisation de l'image: {e}")
        return image_file

@login_required
def enquete_view(request):
    """Vue principale pour la fiche de militant"""
    # Vérifier que l'utilisateur connecté est un enquêteur
    try:
        enqueteur = request.user.enqueteur
        if not enqueteur.actif:
            messages.error(request, "Votre compte enquêteur n'est pas actif.")
            return redirect('login')
    except Enqueteur.DoesNotExist:
        messages.error(request, "Vous n'êtes pas autorisé à accéder à cette page.")
        return redirect('login')

    if request.method == "POST":
        form = FicheMilitantForm(request.POST, request.FILES)
        if form.is_valid():
            fiche = form.save(commit=False)
            fiche.enqueteur = enqueteur  # Associer la fiche à l'enquêteur connecté

            # Traitement de la photo
            if 'photo' in request.FILES:
                photo_file = request.FILES['photo']
                try:
                    # Optimiser l'image
                    optimized_photo = optimize_image(photo_file)

                    # Générer un nom de fichier unique
                    file_extension = '.jpg'  # Toujours sauvegarder en JPEG après optimisation
                    filename = f"{fiche.prenoms}_{fiche.nom}_{enqueteur.id}".replace(' ', '_').replace('/', '_')
                    filename = f"{filename}{file_extension}"

                    # Sauvegarder la photo optimisée
                    fiche.photo.save(filename, optimized_photo, save=False)

                    messages.info(request, "📷 Photo ajoutée et optimisée avec succès.")

                except Exception as e:
                    messages.warning(request, f"Erreur lors du traitement de la photo: {str(e)}")

            # Vérifier si la personne existe dans le CSV
            nom = fiche.nom
            prenoms = fiche.prenoms
            date_naissance = fiche.date_naissance
            lieu_naissance = fiche.lieu_naissance

            # Recherche dans le CSV
            resultat = verifier_personne_dans_csv(
                nom=nom,
                prenoms=prenoms,
                date_naissance=date_naissance,
                lieu_naissance=lieu_naissance
            )

            if resultat and resultat.get('trouve'):
                fiche.est_dans_csv = True

                # Stocker le numéro électeur s'il existe
                if resultat.get('numero_electeur'):
                    fiche.numero_electeur_csv = resultat['numero_electeur']
                    # Si le champ numéro carte électeur est vide, le remplir
                    if not fiche.numero_carte_electeur:
                        fiche.numero_carte_electeur = resultat['numero_electeur']

                messages.warning(
                    request,
                    f"⚠️ Cette personne ({prenoms} {nom}) est déjà enregistrée dans le fichier électoral. "
                    f"Numéro électeur : {resultat.get('numero_electeur', 'Non renseigné')} | "
                    f"Lieu de vote : {resultat.get('lieu_vote', 'Non renseigné')}"
                )
            else:
                fiche.est_dans_csv = False
                messages.info(
                    request,
                    f"ℹ️ Cette personne ({prenoms} {nom}) n'a pas été trouvée dans le fichier électoral. "
                    "Elle sera enregistrée comme nouvelle inscription potentielle."
                )

            # Sauvegarder la fiche
            fiche.save()

            # IMPORTANT: Stocker l'ID de la fiche dans la session pour l'afficher sur la page merci
            request.session['derniere_fiche_id'] = fiche.id
            request.session['fiche_nom_complet'] = f"{fiche.prenoms} {fiche.nom}"

            messages.success(request, "✅ Fiche de militant enregistrée avec succès !")
            return redirect("merci")
        else:
            messages.error(request, "Veuillez corriger les erreurs dans le formulaire.")
    else:
        form = FicheMilitantForm()

    # Compter le nombre total d'électeurs dans le CSV
    total_electeurs_csv = compter_electeurs_csv()

    context = {
        'form': form,
        'enqueteur': enqueteur,
        'total_fiches': enqueteur.fiches_militant.count(),
        'total_electeurs_csv': total_electeurs_csv,
    }
    return render(request, "enquete_form.html", context)

@login_required
def merci_view(request):
    """Vue pour la page de remerciement avec affichage de la dernière fiche"""
    derniere_fiche = None
    nom_complet = None

    # Récupérer les informations de la dernière fiche enregistrée depuis la session
    derniere_fiche_id = request.session.get('derniere_fiche_id')
    nom_complet = request.session.get('fiche_nom_complet', 'Militant')

    print(f"DEBUG: derniere_fiche_id = {derniere_fiche_id}")  # Debug

    if derniere_fiche_id:
        try:
            # Récupérer la fiche depuis la base de données
            derniere_fiche = FicheMilitant.objects.get(
                id=derniere_fiche_id,
                enqueteur=request.user.enqueteur
            )
            print(f"DEBUG: Fiche trouvée - {derniere_fiche.prenoms} {derniere_fiche.nom}")  # Debug
            print(f"DEBUG: Photo URL - {derniere_fiche.photo.url if derniere_fiche.photo else 'Pas de photo'}")  # Debug

            # Nettoyer la session après utilisation
            if 'derniere_fiche_id' in request.session:
                del request.session['derniere_fiche_id']
            if 'fiche_nom_complet' in request.session:
                del request.session['fiche_nom_complet']

        except FicheMilitant.DoesNotExist:
            print("DEBUG: Fiche non trouvée")  # Debug
            derniere_fiche = None
        except Exception as e:
            print(f"DEBUG: Erreur - {e}")  # Debug
            derniere_fiche = None

    # Calculer les statistiques générales
    try:
        enqueteur = request.user.enqueteur
        total_fiches = enqueteur.fiches_militant.count()
        fiches_dans_csv = enqueteur.fiches_militant.filter(est_dans_csv=True).count()
        fiches_avec_photo = enqueteur.fiches_militant.exclude(photo='').count()

        # Calculer le pourcentage
        pourcentage = 0
        if total_fiches > 0:
            pourcentage = (fiches_dans_csv / total_fiches) * 100

        # Pourcentage de fiches avec photo
        pourcentage_photo = 0
        if total_fiches > 0:
            pourcentage_photo = (fiches_avec_photo / total_fiches) * 100

    except Enqueteur.DoesNotExist:
        total_fiches = 0
        fiches_dans_csv = 0
        pourcentage = 0
        fiches_avec_photo = 0
        pourcentage_photo = 0

    # Préparer le contexte pour le template
    context = {
        'total_enquetes': total_fiches,
        'fiches_dans_csv': fiches_dans_csv,
        'pourcentage_csv': pourcentage,
        'nouvelles_inscriptions': total_fiches - fiches_dans_csv,
        'fiches_avec_photo': fiches_avec_photo,
        'pourcentage_photo': pourcentage_photo,
        'derniere_fiche': derniere_fiche,
        'nom_complet': nom_complet,
    }

    print(f"DEBUG: Context - derniere_fiche = {derniere_fiche}")  # Debug

    return render(request, "merci.html", context)

def login_view(request):
    # ✅ Vérifier si l'utilisateur est connecté ET bien un enquêteur actif
    if request.user.is_authenticated:
        try:
            if request.user.enqueteur.actif:
                return redirect("enquete")
            else:
                logout(request)  # déconnecter les comptes inactifs
        except Enqueteur.DoesNotExist:
            logout(request)  # déconnecter les utilisateurs non enquêteurs

    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        user = authenticate(request, username=email, password=password)

        if user is None:
            try:
                user_obj = User.objects.get(email=email)
                user = authenticate(request, username=user_obj.username, password=password)
            except User.DoesNotExist:
                pass

        if user is not None:
            try:
                enqueteur = user.enqueteur
                if not enqueteur.actif:
                    messages.error(request, "Votre compte est désactivé. Contactez l'administrateur.")
                    return render(request, "login.html", {"error": True})

                login(request, user)
                messages.success(request, f"Bienvenue {enqueteur.prenom} !")
                return redirect("enquete")

            except Enqueteur.DoesNotExist:
                messages.error(request, "Accès non autorisé. Seuls les enquêteurs peuvent se connecter.")
                return render(request, "login.html", {"error": True})

        else:
            messages.error(request, "Email ou mot de passe incorrect.")
            return render(request, "login.html", {"error": True})

    return render(request, "login.html")


@login_required
def logout_view(request):
    logout(request)
    messages.info(request, "Vous avez été déconnecté avec succès.")
    return redirect("login")