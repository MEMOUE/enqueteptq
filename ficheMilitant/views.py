from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import HttpResponse
from django.template import loader
from .forms import FicheMilitantForm, EnquetePolitiqueForm
from .models import Enqueteur, FicheMilitant

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
            fiche.save()
            messages.success(request, "Fiche de militant enregistrée avec succès !")
            return redirect("merci")
        else:
            messages.error(request, "Veuillez corriger les erreurs dans le formulaire.")
    else:
        form = FicheMilitantForm()

    context = {
        'form': form,
        'enqueteur': enqueteur,
        'total_fiches': enqueteur.fiches_militant.count()
    }
    return render(request, "enquete_form.html", context)

@login_required
def merci_view(request):
    try:
        enqueteur = request.user.enqueteur
        total_fiches = enqueteur.fiches_militant.count()
    except Enqueteur.DoesNotExist:
        total_fiches = 0

    return render(request, "merci.html", {'total_enquetes': total_fiches})

def login_view(request):
    if request.user.is_authenticated:
        return redirect("enquete")

    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        # Méthode améliorée : chercher l'utilisateur par email
        user = None

        # Première tentative : authentification directe (si email = username)
        user = authenticate(request, username=email, password=password)

        # Deuxième tentative : chercher par email si la première échoue
        if user is None:
            try:
                user_obj = User.objects.get(email=email)
                user = authenticate(request, username=user_obj.username, password=password)
            except User.DoesNotExist:
                pass

        if user is not None:
            # Vérifier que l'utilisateur est un enquêteur actif
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