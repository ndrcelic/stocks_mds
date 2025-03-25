from .models import Stock, DatesValues
from datetime import timedelta
from typing import List, Tuple, Dict

def calculation(start_date=None, end_date=None, company=None):
    number_of_days = 1 + end_date.day - start_date.day

    pre_range_start_date = start_date - timedelta(days=number_of_days)
    pre_range_end_date = pre_range_start_date + timedelta(days=number_of_days - 1)

    post_range_start_date = end_date + timedelta(days=1)
    post_range_end_date = end_date + timedelta(days=number_of_days)

    pre_range_dict = read_from_db(pre_range_start_date, pre_range_end_date, company)
    in_range_dict = read_from_db(start_date, end_date, company)
    post_range_dict = read_from_db(post_range_start_date, post_range_end_date, company)

    processed_data = {"pre_range": pre_range_dict,
                    "in_range": in_range_dict,
                    "post_range": post_range_dict}

    return processed_data


def read_from_db(range_start_date, range_end_date, company) -> Dict:
    range = DatesValues.objects.filter(date__gte=range_start_date, date__lte=range_end_date)
    ret_vals = one_trade_calculate(list(range.filter(stock__abbreviation=company)))
    range_buy = ret_vals[0] if len(ret_vals) else None
    range_sale = ret_vals[1] if len(ret_vals) else None
    range_profit = range_sale.close - range_buy.close if len(ret_vals) else 0

    range_more_trade_profit = more_trade_calculate(list(range.filter(stock__abbreviation=company)))
    range_better_stocks = compare(range, company)

    range_dict = {"in_date": range_start_date.strftime("%m/%d/%Y"),
                      "end_date": range_end_date.strftime("%m/%d/%Y")}
    if len(ret_vals) == 0:
        if range.count() == 0:
            range_dict.update({"message": "The period is out of range."})
        else:
            range_dict.update({"message": "It was not a good period for trading."})
    if len(ret_vals) > 0:
        range_dict.update({"best_buy_date": range_buy.date.strftime("%m/%d/%Y") if range_buy else "",
                               "best_buy_close": range_buy.close if range_buy else "",
                               "best_sale_date": range_sale.date.strftime("%m/%d/%Y") if range_buy else "",
                               "best_sale_close": range_sale.close if range_buy else ""})
    range_dict.update({"profit": range_profit,
                           "more_trade_profit": range_more_trade_profit,
                           "better_stocks": range_better_stocks})

    return range_dict


def one_trade_calculate(input_values: List) -> Tuple:
    # high = sale
    # low = buy
    profit = 0
    date_values_buy = DatesValues()
    date_values_sale = DatesValues()

    for obj_buy in input_values:
        for obj_sale in input_values:
            if obj_buy.date >= obj_sale.date:
                continue
            # print(obj_buy.date, obj_sale.date)
            temp_profit = obj_sale.close - obj_buy.close
            if temp_profit > 0 and temp_profit > profit:
                profit = temp_profit
                date_values_buy = obj_buy
                date_values_sale = obj_sale
                # print(profit)

    # print(profit)
    if profit == 0:
        return ()

    return date_values_buy, date_values_sale


def more_trade_calculate(input_values: List):
    profit = 0

    for i in range(1, len(input_values)):
        if input_values[i].close > input_values[i-1].close:
            profit += input_values[i].close - input_values[i-1].close

    return profit


def compare(query_set, company):
    stocks = Stock.objects.exclude(abbreviation=company)
    ret_list = []

    for stock in stocks:
        #print(stock.name)
        stock_set = query_set.filter(stock=stock)
        if len(one_trade_calculate(list(stock_set))) > 0:
            ret_list.append(stock.name)

    return ret_list
