from django.contrib import admin

from apps.core.admin.mixins import CampaignAdminMixin


class CampaignModelAdmin(CampaignAdminMixin, admin.ModelAdmin):
    """
    Base admin class that includes campaign filtering.
    
    Usage:
    ```python
    from apps.core.admin import CampaignModelAdmin
    
    @admin.register(YourModel)
    class YourModelAdmin(CampaignModelAdmin):
        list_display = ['name', 'campaign']
    ```
    """
    pass
