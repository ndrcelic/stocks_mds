from rest_framework import viewsets
from rest_framework.views import APIView

from .models import Stock, DatesValues
from .serializers import StockSerializer, DatesValuesSerializer


class StockViewSet(viewsets.ModelViewSet):
    queryset = Stock.objects.all()
    serializer_class = StockSerializer


class DatesValuesViewSet(viewsets.ModelViewSet):
    queryset = DatesValues.objects.all()
    serializer_class = DatesValuesSerializer


