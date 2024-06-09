from rest_framework_nested import routers
from apps.world.api.views.openai import OpenAILocationManagementViewSet, OpenAIAreaManagementViewSet, OpenAICityManagementViewSet, OpenAIDimensionManagementViewSet


router = routers.SimpleRouter()
router.register(r'locations', OpenAILocationManagementViewSet, basename='locations')
router.register(r'areas', OpenAIAreaManagementViewSet, basename='areas')
router.register(r'cities', OpenAICityManagementViewSet, basename='cities')
router.register(r'dimensions', OpenAIDimensionManagementViewSet, basename='dimensions')

