from django import forms

from ..models import Organization


class BulkChangeAvatarForm(forms.Form):
    """
    Form to upload a new avatar for bulk action.
    """
    avatar = forms.ImageField(label="New Avatar")


class BulkChangeOrganizationForm(forms.Form):
    """
    Form to select an organization for bulk action.
    """
    organization = forms.ModelChoiceField(
        queryset=Organization.objects.all(),
        label="Select Organization",
        required=True
    )