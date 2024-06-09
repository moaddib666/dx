from rest_framework_nested import routers
from apps.school.api.views.openai import OpenAISchoolManagementViewSet, OpenAISkillManagementViewSet, OpenAIPathManagementViewSet


router = routers.SimpleRouter()
router.register(r'paths', OpenAIPathManagementViewSet)
router.register(r'schools', OpenAISchoolManagementViewSet, basename='path-school')

school_router = routers.NestedSimpleRouter(router, r'schools', lookup='school')
school_router.register(r'skills', OpenAISkillManagementViewSet, basename='school-skill')
