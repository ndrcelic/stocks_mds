from rest_framework.routers import DefaultRouter
from .views import StockViewSet, DatesValuesViewSet, CalculateVew
from django.urls import path

router = DefaultRouter()
router.register(r'stocks', StockViewSet)
router.register(r'dates', DatesValuesViewSet)
urlpatterns = router.urls + [
    path('calculation/', CalculateVew.as_view(), name='calculation'),
]