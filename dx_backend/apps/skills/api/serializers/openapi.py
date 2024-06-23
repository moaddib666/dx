from rest_framework import serializers

from apps.school.api.serializers.openapi import OpenaiSkillSerializer
from apps.skills.models import LearnedSkill, LearnedSchool


class LearnedSkillSerializer(serializers.ModelSerializer):
    skill = OpenaiSkillSerializer()

    class Meta:
        model = LearnedSkill
        fields = ['id', 'player', 'skill']
        read_only_fields = ['id', 'player']


class LearnedSchoolSerializer(serializers.ModelSerializer):
    class Meta:
        model = LearnedSchool
        fields = ['id', 'player', 'school']
        read_only_fields = ['id', 'player']
