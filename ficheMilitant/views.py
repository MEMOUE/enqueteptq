from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import HttpResponse
from django.template import loader
from .forms import FicheMilitantForm, EnquetePolitiqueForm
from .models import Enqueteur, FicheMilitant
from .csv_utils import verifier_personne_dans_csv, compter_electeurs_csv

def ficheMilitant(request):
    template = loader.get_template('login.html')
    return HttpResponse(template.render())

def fiche(request):
    fiche = loader.get_template('fiche.html')
    return HttpResponse(fiche.render())

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
        form = FicheMilitantForm(request.POST)
        if form.is_valid():
            fiche = form.save(commit=False)
            fiche.enqueteur = enqueteur  # Associer la fiche à l'enquêteur connecté

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

            fiche.save()
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
    try:
        enqueteur = request.user.enqueteur
        total_fiches = enqueteur.fiches_militant.count()
        fiches_dans_csv = enqueteur.fiches_militant.filter(est_dans_csv=True).count()

        # Calculer le pourcentage
        pourcentage = 0
        if total_fiches > 0:
            pourcentage = (fiches_dans_csv / total_fiches) * 100

    except Enqueteur.DoesNotExist:
        total_fiches = 0
        fiches_dans_csv = 0
        pourcentage = 0

    return render(request, "merci.html", {
        'total_enquetes': total_fiches,
        'fiches_dans_csv': fiches_dans_csv,
        'pourcentage_csv': pourcentage,
        'nouvelles_inscriptions': total_fiches - fiches_dans_csv
    })

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