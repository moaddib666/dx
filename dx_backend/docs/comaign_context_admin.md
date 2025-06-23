# Steps to Add Global Campaign Context to Django Admin

## 1. Create Campaign Context Middleware

```python
# middleware.py
class CampaignContextMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if request.path.startswith('/admin/'):
            # Initialize campaign in session if not exists
            if 'campaign_id' not in request.session:
                first_campaign = Campaign.objects.first()
                request.session['campaign_id'] = first_campaign.id if first_campaign else None

            # Handle campaign switching via POST
            if request.method == 'POST' and 'switch_campaign' in request.POST:
                request.session['campaign_id'] = int(request.POST.get('campaign_id'))
                return redirect(request.get_full_path())

            # Add current campaign to request
            if request.session.get('campaign_id'):
                request.current_campaign = Campaign.objects.get(id=request.session['campaign_id'])
```

## 2. Create Admin Mixin for Campaign Filtering

```python
# admin/mixins.py
class CampaignAdminMixin:
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        campaign_id = request.session.get('campaign_id')

        if campaign_id and hasattr(self.model, 'campaign'):
            return qs.filter(campaign_id=campaign_id)
        # Add logic for indirect campaign filtering via relationships
        return qs

    def save_model(self, request, obj, form, change):
        if not change and hasattr(obj, 'campaign_id') and not obj.campaign_id:
            obj.campaign_id = request.session.get('campaign_id')
        super().save_model(request, obj, form, change)
```

## 3. Add Campaign Switcher to Admin UI

```html
<!-- templates/admin/base_site.html -->
{% extends "admin/base.html" %}

{% block nav-global %}
<div style="float: right; margin: 5px;">
    <form method="post" style="display: inline;">
        {% csrf_token %}
        <select name="campaign_id" onchange="this.form.submit()">
            {% for campaign in available_campaigns %}
            <option value="{{ campaign.id }}"
                    {% if campaign.id== request.current_campaign.id %}selected{% endif %}>
                {{ campaign.name }}
            </option>
            {% endfor %}
        </select>
        <input type="hidden" name="switch_campaign" value="1">
    </form>
    <span style="color: #ffc;">Current: {{ request.current_campaign.name }}</span>
</div>
{% endblock %}
```

## 4. Add Context Processor

```python
# context_processors.py
def campaign_context(request):
    if request.path.startswith('/admin/'):
        return {
            'available_campaigns': Campaign.objects.all(),
            'current_campaign': getattr(request, 'current_campaign', None)
        }
    return {}
```

## 5. Update Settings

```python
# settings.py
MIDDLEWARE = [
    # ... existing middleware
    'your_app.middleware.CampaignContextMiddleware',
    # ... rest
]

TEMPLATES = [{
    'OPTIONS': {
        'context_processors': [
            # ... existing processors
            'your_app.context_processors.campaign_context',
        ],
    },
}]
```

## 6. Apply Mixin to All Admin Classes

```python
# admin.py
from .mixins import CampaignAdminMixin


@admin.register(Character)
class CharacterAdmin(CampaignAdminMixin, admin.ModelAdmin):
    list_display = ['name', 'campaign']


@admin.register(Organization)
class OrganizationAdmin(CampaignAdminMixin, admin.ModelAdmin):
    list_display = ['name', 'campaign']

# Apply to ALL your model admins
```

## That's It! 🎯

After these 6 steps, your Django admin will have:

- **Global campaign context** stored in session
- **Automatic filtering** of all admin lists by selected campaign
- **Campaign switcher** in admin header
- **Auto-assignment** of campaign to new objects
- **Persistent selection** across tabs and page refreshes