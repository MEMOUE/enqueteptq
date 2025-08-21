from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_view, name='home'),  # Page d'accueil = login
    path('ficheMilitant', views.ficheMilitant, name='ficheMilitant'),
    path('fiche', views.fiche, name='fiche'),
    path("enquete/", views.enquete_view, name="enquete"),
    path("merci/", views.merci_view, name="merci"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
]