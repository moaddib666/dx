from apps.game.models import Campaign


def campaign_context(request):
    if request.path.startswith('/admin/'):
        return {
            'available_campaigns': Campaign.objects.all(),
            'current_campaign': getattr(request, 'current_campaign', None)
        }
    return {}
