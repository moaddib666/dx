from rest_framework import serializers

from apps.school.api.serializers.openapi import OpenaiSkillSerializer
from apps.skills.models import LearnedSkill, LearnedSchool


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
