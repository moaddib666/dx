from rest_framework import serializers

from apps.skills.models import LearnedSkill, LearnedSchool


class LearnedSkillSerializer(serializers.ModelSerializer):

    class Meta:
        model = LearnedSkill
        fields = ['id', 'player', 'skill']
        read_only_fields = ['id', 'player']


class LearnedSchoolSerializer(serializers.ModelSerializer):

    class Meta:
        model = LearnedSchool
        fields = ['id', 'player', 'school']
        read_only_fields = ['id', 'player']
