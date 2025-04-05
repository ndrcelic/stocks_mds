from .models import Stock, DatesValues
from datetime import timedelta
from typing import List, Tuple, Dict

def calculation(start_date=None, end_date=None, company=None):
    number_of_days = (end_date - start_date).days

    pre_range_end_date_qs = DatesValues.objects.filter(date__lt=start_date, stock__abbreviation=company).order_by('date').last()
    pre_range_end_date = pre_range_end_date_qs.date if pre_range_end_date_qs else (start_date - timedelta(days=1))
    pre_range_start_date = pre_range_end_date - timedelta(days=number_of_days)


    post_range_start_date_qs = DatesValues.objects.filter(date__gt=end_date, stock__abbreviation=company).order_by('date').first()
    post_range_start_date = post_range_start_date_qs.date if post_range_start_date_qs else (end_date + timedelta(days=1))
    post_range_end_date = post_range_start_date + timedelta(days=number_of_days)

    pre_range_dict = read_from_db(pre_range_start_date, pre_range_end_date, company)
    in_range_dict = read_from_db(start_date, end_date, company)
    post_range_dict = read_from_db(post_range_start_date, post_range_end_date, company)

    processed_data = {"pre_range": pre_range_dict,
                    "in_range": in_range_dict,
                    "post_range": post_range_dict}

    return processed_data


def read_from_db(range_start_date, range_end_date, company) -> Dict:
    range_qs = DatesValues.objects.filter(date__gte=range_start_date, date__lte=range_end_date)
    companies = list(range_qs.filter(stock__abbreviation=company))

    range_dict = {"in_date": range_start_date.strftime("%m/%d/%Y"),
                  "end_date": range_end_date.strftime("%m/%d/%Y")}

    if not companies:
        range_dict.update({"message": "The period is out of range."})
        return range_dict

    range_profit = 0
    ret_vals = one_trade_calculate(companies)
    if ret_vals:
        range_profit = ret_vals[1].close - ret_vals[0].close if ret_vals else 0

        range_dict.update({"best_buy_date": ret_vals[0].date.strftime("%m/%d/%Y"),
                           "best_buy_close": ret_vals[0].close,
                           "best_sale_date": ret_vals[1].date.strftime("%m/%d/%Y"),
                           "best_sale_close": ret_vals[1].close,
                           "profit": range_profit})
    else:
        range_dict.update({"message": "It was not a good period for trading.",
                           "profit": range_profit})

    range_more_trade_profit = more_trade_calculate(companies)
    range_better_stocks = compare(range_qs, company, range_profit)
    range_dict.update({"more_trade_profit": range_more_trade_profit,
                        "better_stocks": range_better_stocks})

    return range_dict


def one_trade_calculate(input_values: List) -> Tuple:
    if not input_values:
        return ()

    max_profit = 0
    date_values_buy = None
    i = 0
    while i < len(input_values):
        if input_values[i].close is not None:
            date_values_buy = input_values[i]
            i = i + 1
            break
        i = i + 1

    results = (None, None)

    for value in input_values[i:]:
        if value.close is None:
            continue
        profit = value.close - date_values_buy.close
        if profit > max_profit:
            max_profit = profit
            results = (date_values_buy, value)

        if value.close < date_values_buy.close:
            date_values_buy = value

    if max_profit == 0:
        return ()

    return results


def more_trade_calculate(input_values: List):
    profit = 0

    for i in range(1, len(input_values)):
        if input_values[i].close is None or input_values[i-1].close is None:
            continue
        if input_values[i].close > input_values[i-1].close:
            profit += input_values[i].close - input_values[i-1].close

    return profit


def compare(query_set, company, profit):
    stocks = Stock.objects.exclude(abbreviation=company)
    ret_list = []

    for stock in stocks:
        stock_set = query_set.filter(stock=stock)
        result = one_trade_calculate(list(stock_set))

        range_profit = result[1].close - result[0].close if result else 0
        if range_profit and range_profit > profit:
            ret_list.append([stock.name, range_profit])

    return ret_list
