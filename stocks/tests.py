from rest_framework import status
from rest_framework.test import APITestCase
from .models import Stock, DatesValues
import datetime

class CalculateAPITestCase(APITestCase):
    def setUp(self):
        self.stock = Stock.objects.create(name="IBM", abbreviation="IBM")

        self.datevalue1 = DatesValues.objects.create(stock=self.stock, date=datetime.date(2023, 1, 14), close=50)
        self.datevalue2 = DatesValues.objects.create(stock=self.stock, date=datetime.date(2023, 1, 15), close=52)
        self.datevalue3 = DatesValues.objects.create(stock=self.stock, date=datetime.date(2023, 1, 16), close=48)
        self.datevalue4 = DatesValues.objects.create(stock=self.stock, date=datetime.date(2023, 1, 17), close=50)
        self.datevalue5 = DatesValues.objects.create(stock=self.stock, date=datetime.date(2023, 1, 19), close=55)
        self.datevalue6 = DatesValues.objects.create(stock=self.stock, date=datetime.date(2023, 1, 20), close=53)
        self.datevalue7 = DatesValues.objects.create(stock=self.stock, date=datetime.date(2023, 1, 21), close=45)
        self.datevalue8 = DatesValues.objects.create(stock=self.stock, date=datetime.date(2023, 1, 22), close=56)
        self.datevalue9 = DatesValues.objects.create(stock=self.stock, date=datetime.date(2023, 1, 23), close=52)
        self.datevalue10 = DatesValues.objects.create(stock=self.stock, date=datetime.date(2023, 1, 24), close=51)

        self.api = "/api/calculation/"


    def test_calculate_one_trade_success(self):
        url = self.api + "?start_date=1/17/2023&end_date=1/21/2023&company=IBM"
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json().get("pre_range").get("profit"), 2)
        self.assertEqual(response.json().get("in_range").get("profit"), 5)
        self.assertEqual(response.json().get("post_range").get("profit"), 0)

    def test_calculate_more_trade_success(self):
        url = self.api + "?start_date=1/14/2023&end_date=1/24/2023&company=IBM"
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json().get("pre_range").get("more_trade_profit"), 0)
        self.assertEqual(response.json().get("in_range").get("more_trade_profit"), 20)
        self.assertEqual(response.json().get("post_range").get("more_trade_profit"), 0)


    def test_calculate_out_of_range_success(self):
        url = self.api + "?start_date=1/25/2023&end_date=1/28/2023&company=IBM"
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json().get("pre_range").get("profit"), 11)
        self.assertEqual(response.json().get("in_range").get("message"), "The period is out of range.")
        self.assertEqual(response.json().get("post_range").get("message"), "The period is out of range.")

    def test_missing_parameter(self):
        url = self.api + "?end_date=06/01/2023&companyIBM"
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("Some parameters are missing", response.json().get("error_message"))

    def test_stock_doesnt_exist(self):
        url = self.api + "?start_date=06/10/2023&end_date=06/01/2023&company=DELL"
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertIn("Stock does not exist", response.json().get("error_message"))

    def test_wrong_start_date(self):
        url = self.api + "?start_date=06/0asd1/2023&end_date=06/10/2023&company=IBM"
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("Invalid start date", response.json().get("error_message"))

    def test_wrong_end_date(self):
        url = self.api + "?start_date=06/01/2023&end_date=06/01/sdsd2023&company=IBM"
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("Invalid end date", response.json().get("error_message"))

    def test_start_date(self):
        url = self.api + "?start_date=04/04/2026&end_date=04/10/2026&company=IBM"
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("Start date must be in the past", response.json().get("error_message"))

    def test_calculate_wrong_input_dates(self):
        url = self.api + "?start_date=06/10/2023&end_date=06/01/2023&company=IBM"
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("Start date must be before end date", response.json().get("error_message"))




