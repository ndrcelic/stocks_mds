from django.core.management.base import BaseCommand
import csv
from stocks.models import Stock, DatesValues
import os
from pathlib import Path

class Command(BaseCommand):
    help = 'Import stocks from csv file'

    def add_arguments(self, parser):
        parser.add_argument('path', type=str)

    def handle(self, *args, **options):

        if options['path'] is None:
            return

        path = Path(options['path'])

        if os.path.isdir(options['path']):
            csv_files = [file for file in path.glob('*.csv')]

            for csv_file in csv_files:
                file_name = csv_file.stem
                self.write_in_db(csv_file, file_name)
        elif os.path.isfile(path):
            if path.suffix != '.csv':
                print('File must be .csv')
                return
            file_name = path.name.split('.')[0]
            self.write_in_db(path, file_name)
        else:
            print('This path does not exist')
            return


    def write_in_db(self, path, file_name):
        with open(path, 'r') as company:
            reader = csv.DictReader(company)

            stock, created = Stock.objects.get_or_create(name=file_name)
            for row in reader:
                if row['Adj Close'] == 'null':
                    row['Adj Close'] = None
                if row['Close'] == 'null':
                    row['Close'] = None
                if row['High'] == 'null':
                    row['High'] = None
                if row['Low'] == 'null':
                    row['Low'] = None
                if row['Open'] == 'null':
                    row['Open'] = None
                if row['Volume'] == 'null':
                    row['Volume'] = None
                DatesValues.objects.get_or_create(stock=stock, date=row['Date'], open=row['Open'],
                                                  close=row['Close'], high=row['High'], low=row['Low'],
                                                  adj_close=row['Adj Close'], volume=row['Volume'])
            print(f'Values were added for {file_name}')