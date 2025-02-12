from rest_framework_nested import routers

from apps.bargain.api.views.openai import OpenBargainViewSet, OpenBargainItemsViewSet

router = routers.SimpleRouter()
router.register(r'open_bargains', OpenBargainViewSet)
open_bargain_router = routers.NestedSimpleRouter(router, r'open_bargains', lookup='bargain')
open_bargain_router.register(r'items', OpenBargainItemsViewSet, basename='bargain-items')
urlpatterns = router.urls + open_bargain_router.urls
