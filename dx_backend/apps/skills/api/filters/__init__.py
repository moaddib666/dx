from django_filters import rest_framework as filters

from apps.skills.models import LearnedSkill


class CharacterLearnedSkillFilter(filters.FilterSet):
    character = filters.UUIDFilter()

    class Meta:
        model = LearnedSkill
        fields = ['character', ]
