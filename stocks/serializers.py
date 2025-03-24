from rest_framework import serializers
from .models import Stock, DatesValues


class DatesValuesSerializer(serializers.ModelSerializer):
    # stock = StockSerializer()
    date = serializers.DateField(input_formats=['%m/%d/%Y'])

    class Meta:
        model = DatesValues
        fields = ['id', 'date', 'stock', 'open', 'high', 'low', 'close', 'adj_close', 'volume']


class StockSerializer(serializers.ModelSerializer):
    # date_values = DatesValuesSerializer(many=True, read_only=True)
    date_of_creation = serializers.DateTimeField(input_formats=['%m/%d/%Y'])

    class Meta:
        model = Stock
        fields = ['id', 'name', 'date_of_creation', 'abbreviation']