from rest_framework.viewsets import GenericViewSet


class CampaignFilterMixin(GenericViewSet):
    """
    Simple mixin that filters queryset by user's campaign
    """
    campaign_field = 'campaign'  # Override this if needed

    def get_queryset(self):
        queryset = super().get_queryset()

        # Get campaign from user's main character
        if (self.request.user.is_authenticated and
                hasattr(self.request.user, 'main_character') and
                self.request.user.main_character and
                self.request.user.main_character.campaign):
            campaign = self.request.user.main_character.campaign
            filter_kwargs = {self.campaign_field: campaign}
            return queryset.filter(**filter_kwargs)

        return queryset.none()  # No access if no campaign
