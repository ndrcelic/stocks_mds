from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Stock, DatesValues
from .serializers import StockSerializer, DatesValuesSerializer
from datetime import datetime, timedelta
from typing import List, Tuple
from rest_framework.views import APIView
from .services import calculation


class StockViewSet(viewsets.ModelViewSet):
    queryset = Stock.objects.all()
    serializer_class = StockSerializer


class DatesValuesViewSet(viewsets.ModelViewSet):
    queryset = DatesValues.objects.all()
    serializer_class = DatesValuesSerializer


class CalculateVew(APIView):
    def post(self, request):
        start_date_str = request.data.get('start_date')
        end_date_str = request.data.get('end_date')
        company = request.data.get('company')

        if start_date_str is None or end_date_str is None or company is None:
            return Response({"error_message": "Some parameters are missing"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            Stock.objects.get(abbreviation=company)
        except Stock.DoesNotExist:
            return Response({"error_message": "Stock does not exist"}, status=status.HTTP_404_NOT_FOUND)
        try:
            start_date = datetime.strptime(start_date_str, '%m/%d/%Y').date()
        except ValueError:
            return Response({"error_message": "Invalid start date"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            end_date = datetime.strptime(end_date_str, '%m/%d/%Y').date()
        except ValueError:
            return Response({"error_message": "Invalid end date"}, status=status.HTTP_400_BAD_REQUEST)

        if start_date >= end_date:
            return Response({"error_message": "Start date must be before end date"}, status=status.HTTP_400_BAD_REQUEST)

        if start_date > datetime.today().date():
            return Response({"error_message": "Start date must be in the past"}, status=status.HTTP_400_BAD_REQUEST)

        processed_data = calculation(start_date, end_date, company)

        response = Response(processed_data, status=status.HTTP_200_OK)
        return response

