from django.contrib import admin
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import path, reverse
from django.utils.html import format_html
from django.contrib import messages
from django.http import JsonResponse
from django.db.models import Q

from ..models import Character
from ...skills.models import LearnedSkill
from ...school.models import Skill, School


class SkillSelectionAdminView:
    """
    Custom admin view for skill selection with proper filtering and visual display.
    """
    
    def get_urls(self):
        """Define custom URLs for skill selection."""
        urls = [
            path(
                'character/<uuid:character_id>/add-skills/',
                self.admin_site.admin_view(self.skill_selection_view),
                name='character_add_skills'
            ),
            path(
                'character/<uuid:character_id>/add-skills/save/',
                self.admin_site.admin_view(self.save_selected_skills),
                name='character_save_skills'
            ),
            path(
                'api/skills-by-school/<int:school_id>/',
                self.admin_site.admin_view(self.get_skills_by_school),
                name='skills_by_school_api'
            ),
        ]
        return urls
    
    def skill_selection_view(self, request, character_id):
        """
        Display the skill selection page with filtering and visual display.
        """
        character = get_object_or_404(Character, id=character_id)
        
        # Get all schools for filtering
        schools = School.objects.all().order_by('name')
        
        # Get selected school from query params
        selected_school_id = request.GET.get('school')
        selected_school = None
        if selected_school_id:
            try:
                selected_school = School.objects.get(id=selected_school_id)
            except School.DoesNotExist:
                pass
        
        # Get skills based on school filter
        skills_query = Skill.objects.select_related('school').order_by('school__name', 'grade', 'name')
        if selected_school:
            skills_query = skills_query.filter(school=selected_school)
        
        # Get already learned skills for this character
        learned_skill_ids = set(
            LearnedSkill.objects.filter(character=character).values_list('skill_id', flat=True)
        )
        
        # Prepare skills data with learned status
        skills_data = []
        for skill in skills_query:
            skills_data.append({
                'skill': skill,
                'is_learned': skill.id in learned_skill_ids,
                'school_name': skill.school.name if skill.school else 'No School'
            })
        
        context = {
            'character': character,
            'schools': schools,
            'selected_school': selected_school,
            'skills_data': skills_data,
            'title': f'Add Skills to {character.name}',
            'opts': Character._meta,
            'has_change_permission': True,
        }
        
        return render(request, 'admin/character/skill_selection.html', context)
    
    def save_selected_skills(self, request, character_id):
        """
        Save the selected skills for the character.
        """
        if request.method != 'POST':
            return redirect('admin:character_add_skills', character_id=character_id)
        
        character = get_object_or_404(Character, id=character_id)
        
        # Get selected skill IDs from the form
        selected_skill_ids = request.POST.getlist('selected_skills')
        is_base_skills = request.POST.getlist('is_base_skills')
        
        added_count = 0
        
        for skill_id in selected_skill_ids:
            try:
                skill = Skill.objects.get(id=skill_id)
                
                # Check if skill is already learned
                if not LearnedSkill.objects.filter(character=character, skill=skill).exists():
                    is_base = str(skill_id) in is_base_skills
                    
                    LearnedSkill.objects.create(
                        character=character,
                        skill=skill,
                        is_base=is_base
                    )
                    added_count += 1
                    
            except Skill.DoesNotExist:
                continue
        
        if added_count > 0:
            messages.success(request, f'Successfully added {added_count} skill(s) to {character.name}.')
        else:
            messages.info(request, 'No new skills were added.')
        
        # Redirect back to character admin
        return redirect('admin:character_character_change', object_id=character_id)
    
    def get_skills_by_school(self, request, school_id):
        """
        API endpoint to get skills filtered by school (for AJAX requests).
        """
        try:
            school = School.objects.get(id=school_id)
            skills = Skill.objects.filter(school=school).order_by('grade', 'name')
            
            skills_data = []
            for skill in skills:
                skills_data.append({
                    'id': skill.id,
                    'name': skill.name,
                    'grade': skill.grade,
                    'description': skill.description,
                    'icon_url': skill.icon.url if skill.icon else None,
                })
            
            return JsonResponse({
                'success': True,
                'skills': skills_data,
                'school_name': school.name
            })
            
        except School.DoesNotExist:
            return JsonResponse({
                'success': False,
                'error': 'School not found'
            })


# Mixin to add skill selection functionality to CharacterAdmin
class SkillSelectionMixin:
    """
    Mixin to add skill selection functionality to the Character admin.
    """
    
    def get_urls(self):
        """Add skill selection URLs to the admin."""
        urls = super().get_urls()
        skill_view = SkillSelectionAdminView()
        skill_view.admin_site = self.admin_site
        custom_urls = skill_view.get_urls()
        return custom_urls + urls
    
    def change_view(self, request, object_id, form_url='', extra_context=None):
        """Add skill selection button to the character change view."""
        extra_context = extra_context or {}
        
        # Add custom button for skill selection
        if object_id:
            skill_selection_url = reverse('admin:character_add_skills', args=[object_id])
            extra_context['skill_selection_url'] = skill_selection_url
        
        return super().change_view(request, object_id, form_url, extra_context)
    
    def render_change_form(self, request, context, add=False, change=False, form_url='', obj=None):
        """Add skill selection button to the change form."""
        if obj and change:
            skill_selection_url = reverse('admin:character_add_skills', args=[obj.id])
            context['skill_selection_url'] = skill_selection_url
            
            # Add custom button HTML
            context['skill_selection_button'] = format_html(
                '<a href="{}" class="button" style="margin-left: 10px; background-color: #417690; color: white; padding: 8px 16px; text-decoration: none; border-radius: 4px;">'
                '🎯 Add Skills'
                '</a>',
                skill_selection_url
            )
        
        return super().render_change_form(request, context, add, change, form_url, obj)