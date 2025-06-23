from django.shortcuts import redirect
from django.utils.deprecation import MiddlewareMixin

from apps.game.models import Campaign


class CampaignContextMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if request.path.startswith('/admin/'):
            # Initialize campaign in session if not exists
            if 'campaign_id' not in request.session:
                first_campaign = Campaign.objects.first()
                request.session['campaign_id'] = str(first_campaign.id) if first_campaign else None

            # Handle campaign switching via POST
            if request.method == 'POST' and 'switch_campaign' in request.POST:
                campaign_id = request.POST.get('campaign_id')
                if campaign_id:
                    request.session['campaign_id'] = campaign_id
                else:
                    # Log the issue for debugging
                    import logging
                    logger = logging.getLogger(__name__)
                    logger.error(f"Campaign switching failed: No campaign_id in POST data. POST data: {request.POST}")

                # Check if it's an AJAX request
                if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                    from django.http import JsonResponse

                    if not campaign_id:
                        return JsonResponse({
                            'success': False,
                            'error': 'No campaign ID provided'
                        }, status=400)

                    try:
                        campaign = Campaign.objects.get(id=campaign_id)
                        return JsonResponse({
                            'success': True,
                            'campaign_name': campaign.name,
                            'campaign_id': str(campaign.id)
                        })
                    except Campaign.DoesNotExist:
                        return JsonResponse({
                            'success': False,
                            'error': 'Campaign not found'
                        }, status=404)
                    except Exception as e:
                        import logging
                        logger = logging.getLogger(__name__)
                        logger.error(f"Campaign switching error: {str(e)}")
                        return JsonResponse({
                            'success': False,
                            'error': 'An error occurred while switching campaigns'
                        }, status=500)

                return redirect(request.get_full_path())

            # Add current campaign to request
            if request.session.get('campaign_id'):
                try:
                    request.current_campaign = Campaign.objects.get(id=request.session['campaign_id'])
                except Campaign.DoesNotExist:
                    # If campaign doesn't exist, reset to first campaign
                    first_campaign = Campaign.objects.first()
                    request.session['campaign_id'] = str(first_campaign.id) if first_campaign else None
                    request.current_campaign = first_campaign
