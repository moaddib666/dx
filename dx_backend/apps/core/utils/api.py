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

            # Check if the model has a campaign field before filtering
            model = queryset.model
            model_fields = [f.name for f in model._meta.get_fields()]

            if hasattr(model, self.campaign_field) or self.campaign_field in model_fields:
                filter_kwargs = {self.campaign_field: campaign}
                return queryset.filter(**filter_kwargs)

            # Check if the model has a cycle field with a campaign
            elif 'cycle' in model_fields:
                filter_kwargs = {'cycle__campaign': campaign}
                return queryset.filter(**filter_kwargs)

            # If the model doesn't have a campaign field or cycle field, return the queryset as is
            return queryset

        return queryset.none()  # No access if no campaign
