from django.urls import path
from . import views, api_views

urlpatterns = [
    # Routes principales
    path('', views.login_view, name='home'),  # Page d'accueil = login
    path('ficheMilitant', views.ficheMilitant, name='ficheMilitant'),
    path('fiche', views.fiche, name='fiche'),
    path("enquete/", views.enquete_view, name="enquete"),
    path("merci/", views.merci_view, name="merci"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),

    # Routes API pour les zones et lieux de vote
    path("api/lieux-vote/", api_views.get_lieux_vote_api, name="api_lieux_vote"),
    path("api/zones-lieux/", api_views.get_all_zones_lieux_api, name="api_zones_lieux"),
    path("api/zones/", api_views.get_zones_api, name="api_zones"),
]