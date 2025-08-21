from rest_framework import serializers

from apps.school.api.serializers.openapi import OpenaiSkillSerializer
from apps.school.models import Skill
from apps.skills.models import LearnedSkill, LearnedSchool


class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        exclude = ['created_at', 'updated_at']


class LearnedSkillSerializer(serializers.ModelSerializer):
    skill = OpenaiSkillSerializer()

    class Meta:
        model = LearnedSkill
        fields = ['id', 'character', 'skill']
        read_only_fields = ['id', 'character']


class LearnedSchoolSerializer(serializers.ModelSerializer):
    class Meta:
        model = LearnedSchool
        fields = ['id', 'character', 'school']
        read_only_fields = ['id', 'character']
