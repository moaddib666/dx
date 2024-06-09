from rest_framework import serializers

from apps.school.models import School, Skill, ThePath


class OpenaiSchoolSerializer(serializers.ModelSerializer):

    class Meta:
        model = School
        fields = "__all__"


class OpenaiSkillSerializer(serializers.ModelSerializer):

    class Meta:
        model = Skill
        fields = "__all__"


class OpenaiPathSerializer(serializers.ModelSerializer):
    class Meta:
        model = ThePath
        fields = "__all__"
