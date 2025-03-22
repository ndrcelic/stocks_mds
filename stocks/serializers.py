from rest_framework import serializers
from .models import Stock, DatesValues


class DatesValuesSerializer(serializers.ModelSerializer):
    # stock = StockSerializer()

    class Meta:
        model = DatesValues
        fields = ['id', 'date', 'stock', 'open', 'high', 'low', 'close', 'adj_close', 'volume']


class StockSerializer(serializers.ModelSerializer):
    date_values = DatesValuesSerializer(many=True, read_only=True)
    
    class Meta:
        model = Stock
        fields = ['id', 'name', 'date_of_creation', 'abbreviation', 'date_values']