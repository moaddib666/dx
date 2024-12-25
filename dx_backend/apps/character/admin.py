from django import forms
from django.contrib import admin
from django.shortcuts import redirect, render
from django.urls import path, reverse
from django.utils.html import format_html

from .models import Organization, Rank, Character, CharacterBiography


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


@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name', 'description')


@admin.register(Rank)
class RankAdmin(admin.ModelAdmin):
    list_display = ('name', 'experience_needed', 'grade')
    search_fields = ('name',)
    list_filter = ('experience_needed',)


class CharacterBiographyInline(admin.StackedInline):
    """
    Inline admin for managing CharacterBiography directly within Character admin.
    """
    model = CharacterBiography
    extra = 0  # No extra blank forms
    fields = ('age', 'gender', 'background', 'appearance', 'avatar', 'avatar_preview')
    readonly_fields = ('avatar_preview',)

    def avatar_preview(self, obj):
        """
        Displays the avatar image as a preview in the admin interface.
        """
        if obj.avatar:
            return format_html('<img src="{}" style="max-height: 100px; max-width: 100px;" />', obj.avatar.url)
        return "No Image"

    avatar_preview.short_description = "Avatar Preview"


class SubLocationFilter(admin.SimpleListFilter):
    """
    Custom filter for filtering by sublocation.
    """
    title = 'SubLocation'
    parameter_name = 'position__sublocation'

    def lookups(self, request, model_admin):
        sublocations = set(
            obj.position.sub_location for obj in Character.objects.select_related('position__sub_location') if
            obj.position)
        return [(s.id, s.name) for s in sublocations]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(position__sub_location_id=self.value())
        return queryset


class GridZFilter(admin.SimpleListFilter):
    """
    Custom filter for filtering by grid_z.
    """
    title = 'Grid Z'
    parameter_name = 'position__grid_z'

    def lookups(self, request, model_admin):
        grid_z_values = set(obj.position.grid_z for obj in Character.objects.select_related('position') if obj.position)
        return [(z, f'Grid Z: {z}') for z in grid_z_values]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(position__grid_z=self.value())
        return queryset


@admin.register(Character)
class CharacterAdmin(admin.ModelAdmin):
    """
    Admin interface for Character with integrated CharacterBiography.
    """
    list_display = (
        'name', 'pictogram', 'position', 'get_age', 'get_gender', 'rank',
        'current_health_points', 'current_energy_points',
        'organization', 'is_active', 'npc'
    )
    search_fields = ('name', 'biography__background', 'biography__appearance')
    # list_filter = ('biography__gender', 'rank', 'organization', 'is_active', 'npc')
    list_filter = (
    'biography__gender', 'rank', 'organization', 'is_active', 'npc', SubLocationFilter, GridZFilter)

    # TODO add multichoise filter by: position__sublocation, position__grid_z, organization

    inlines = [CharacterBiographyInline]
    actions = ['bulk_set_active', 'bulk_set_inactive', 'bulk_change_organization', 'duplicate_character',
               'bulk_change_avatar', 'bulk_set_npc']

    def pictogram(self, obj):
        """
        Displays the avatar image in the list view.
        """
        if obj.biography and obj.biography.avatar:
            return format_html('<img src="{}" style="height: 50px; width: 50px; border-radius: 50%;" />',
                               obj.biography.avatar.url)
        return "No Image"

    pictogram.short_description = "Avatar"

    def get_age(self, obj):
        """
        Retrieve age from the associated CharacterBiography.
        """
        return obj.biography.age if obj.biography else "N/A"

    get_age.short_description = "Age"

    def get_gender(self, obj):
        """
        Retrieve gender from the associated CharacterBiography.
        """
        return obj.biography.gender if obj.biography else "N/A"

    get_gender.short_description = "Gender"

    # Bulk actions
    @admin.action(description='Set selected characters as Active')
    def bulk_set_active(self, request, queryset):
        updated = queryset.update(is_active=True)
        self.message_user(request, f"{updated} character(s) set as active.")

    @admin.action(description='Set selected characters as NPC')
    def bulk_set_npc(self, request, queryset):
        updated = queryset.update(npc=True)
        self.message_user(request, f"{updated} character(s) set as NPC.")

    @admin.action(description='Set selected characters as Inactive')
    def bulk_set_inactive(self, request, queryset):
        updated = queryset.update(is_active=False)
        self.message_user(request, f"{updated} character(s) set as inactive.")

    @admin.action(description='Change Organization for selected characters')
    def bulk_change_organization(self, request, queryset):
        """
        Redirects to a custom view for selecting an organization to apply to selected characters.
        """
        selected = queryset.values_list('id', flat=True)
        return redirect(f'{reverse("admin:bulk_change_organization_view")}?ids={",".join(map(str, selected))}')

    @admin.action(description='Duplicate selected character(s)')
    def duplicate_character(self, request, queryset):
        """
        Duplicate selected characters with "Copy: {InitialName}" as the new name.
        """
        for character in queryset:
            new_character = Character.objects.get(pk=character.pk)
            new_character.pk = None  # Reset primary key to create a new instance
            new_character.name = f"Copy: {character.name}"  # Rename duplicated character
            new_character.save()

            # Duplicate biography if exists
            if character.biography:
                CharacterBiography.objects.create(
                    character=new_character,
                    age=character.biography.age,
                    gender=character.biography.gender,
                    background=character.biography.background,
                    appearance=character.biography.appearance,
                    avatar=character.biography.avatar
                )

        self.message_user(request, f"{queryset.count()} character(s) duplicated successfully.")

    @admin.action(description='Change Avatar for selected characters')
    def bulk_change_avatar(self, request, queryset):
        """
        Redirects to a custom view for changing the avatar of selected characters.
        """
        selected = queryset.values_list('id', flat=True)
        return redirect(f'{reverse("admin:bulk_change_avatar_view")}?ids={",".join(map(str, selected))}')

    def get_urls(self):
        """
        Adds custom URLs for the bulk change organization and avatar views.
        """
        urls = super().get_urls()
        custom_urls = [
            path('bulk_change_avatar/', self.admin_site.admin_view(self.bulk_change_avatar_view),
                 name='bulk_change_avatar_view'),
            path('bulk_change_organization/', self.admin_site.admin_view(self.bulk_change_organization_view),
                 name='bulk_change_organization_view'),
        ]
        return custom_urls + urls

    def bulk_change_avatar_view(self, request):
        """
        Custom view for bulk changing the avatar of selected characters.
        """
        if request.method == 'POST':
            form = BulkChangeAvatarForm(request.POST, request.FILES)
            if form.is_valid():
                avatar = form.cleaned_data['avatar']
                ids = request.GET.get('ids', '').split(',')
                characters = Character.objects.filter(id__in=ids)

                for character in characters:
                    if character.biography:
                        character.biography.avatar = avatar
                        character.biography.save()

                self.message_user(request, f"{characters.count()} character(s) updated with the new avatar.")
                return redirect('..')
        else:
            form = BulkChangeAvatarForm()

        return render(request, 'admin/bulk_change_avatar.html', {'form': form})

    def bulk_change_organization_view(self, request):
        """
        Custom view for bulk changing the organization of selected characters.
        """
        if request.method == 'POST':
            form = BulkChangeOrganizationForm(request.POST)
            if form.is_valid():
                organization = form.cleaned_data['organization']
                ids = request.GET.get('ids', '').split(',')
                characters = Character.objects.filter(id__in=ids)

                updated = characters.update(organization=organization)
                self.message_user(request, f"{updated} character(s) assigned to {organization.name}.")
                return redirect('..')
        else:
            form = BulkChangeOrganizationForm()

        return render(request, 'admin/bulk_change_organization.html', {'form': form})
