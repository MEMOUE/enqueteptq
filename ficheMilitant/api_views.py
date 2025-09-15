# ficheMilitant/api_views.py

from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from .zone_lieu_utils import get_zones_lieux_cached, get_lieux_vote_par_zone

@login_required
@require_http_methods(["GET"])
def get_lieux_vote_api(request):
    """
    API pour récupérer les lieux de vote d'une zone spécifique
    Usage: /api/lieux-vote/?zone=DANANE
    """
    zone = request.GET.get('zone', '').strip()

    if not zone:
        return JsonResponse({
            'error': 'Paramètre zone requis',
            'lieux': []
        }, status=400)

    try:
        lieux = get_lieux_vote_par_zone(zone)
        return JsonResponse({
            'zone': zone,
            'lieux': lieux,
            'count': len(lieux)
        })
    except Exception as e:
        return JsonResponse({
            'error': f'Erreur lors de la récupération des lieux: {str(e)}',
            'lieux': []
        }, status=500)

@login_required
@require_http_methods(["GET"])
def get_all_zones_lieux_api(request):
    """
    API pour récupérer toutes les zones et leurs lieux de vote
    Usage: /api/zones-lieux/
    """
    try:
        zones_lieux = get_zones_lieux_cached()

        # Statistiques
        total_zones = len(zones_lieux)
        total_lieux = sum(len(lieux) for lieux in zones_lieux.values())

        return JsonResponse({
            'zones_lieux': zones_lieux,
            'stats': {
                'total_zones': total_zones,
                'total_lieux': total_lieux,
                'zones_disponibles': list(zones_lieux.keys())
            }
        })
    except Exception as e:
        return JsonResponse({
            'error': f'Erreur lors de la récupération des données: {str(e)}',
            'zones_lieux': {}
        }, status=500)

@login_required
@require_http_methods(["GET"])
def get_zones_api(request):
    """
    API pour récupérer uniquement la liste des zones
    Usage: /api/zones/
    """
    try:
        zones_lieux = get_zones_lieux_cached()
        zones = list(zones_lieux.keys())

        return JsonResponse({
            'zones': sorted(zones),
            'count': len(zones)
        })
    except Exception as e:
        return JsonResponse({
            'error': f'Erreur lors de la récupération des zones: {str(e)}',
            'zones': []
        }, status=500)