from rest_framework.routers import DefaultRouter
from .views import StockViewSet, DatesValuesViewSet

router = DefaultRouter()
router.register(r'stocks', StockViewSet)
router.register(r'dates', DatesValuesViewSet)
urlpatterns = router.urls