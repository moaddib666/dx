class CampaignAdminMixin:
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        campaign_id = request.session.get('campaign_id')

        if campaign_id and hasattr(self.model, 'campaign'):
            return qs.filter(campaign_id=campaign_id)

        # Handle indirect campaign filtering via relationships
        # For models that don't have a direct campaign field but are related to models that do
        if hasattr(self.model, 'character') and hasattr(self.model.character.field.related_model, 'campaign'):
            return qs.filter(character__campaign_id=campaign_id)
        if hasattr(self.model, 'organization') and hasattr(self.model.organization.field.related_model, 'campaign'):
            return qs.filter(organization__campaign_id=campaign_id)
        if hasattr(self.model, 'dimension') and hasattr(self.model.dimension.field.related_model, 'campaign'):
            return qs.filter(dimension__campaign_id=campaign_id)

        return qs

    def save_model(self, request, obj, form, change):
        if not change and hasattr(obj, 'campaign_id') and not obj.campaign_id:
            obj.campaign_id = request.session.get('campaign_id')
        super().save_model(request, obj, form, change)
