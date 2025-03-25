from rest_framework import serializers
from .models import Stock, DatesValues


class StockSerializer(serializers.ModelSerializer):
    date_of_creation = serializers.DateTimeField(input_formats=['%m/%d/%Y'])

    class Meta:
        model = Stock
        fields = ['id', 'name', 'date_of_creation', 'abbreviation']

    def to_representation(self, instance):
        representation = super().to_representation(instance) or {}

        if "date_of_creation" in representation:
            representation["date_of_creation"] = instance.date_of_creation.strftime("%m/%d/%Y") \
                if instance.date_of_creation else None

        return representation


class DatesValuesSerializer(serializers.ModelSerializer):
    stock = StockSerializer()
    date = serializers.DateField(input_formats=['%m/%d/%Y'])

    class Meta:
        model = DatesValues
        fields = ['id', 'date', 'stock', 'open', 'high', 'low', 'close', 'adj_close', 'volume']

    def to_representation(self, instance):
        representation = super().to_representation(instance)

        if "date" in representation:
            representation["date"] = instance.date.strftime("%m/%d/%Y")

        return representation