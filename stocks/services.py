from .models import Stock, DatesValues
from datetime import timedelta
from typing import List, Tuple

def calculation(start_date=None, end_date=None, company=None):
    number_of_days = 1 + end_date.day - start_date.day

    pre_range_start_date = start_date - timedelta(days=number_of_days)
    pre_range_end_date = pre_range_start_date + timedelta(days=number_of_days - 1)
    post_range_start_date = end_date + timedelta(days=1)
    post_range_end_date = end_date + timedelta(days=number_of_days)

    pre_range = DatesValues.objects.filter(date__gte=pre_range_start_date, date__lte=pre_range_end_date)
    ret_vals =one_trade_calculate(list(pre_range.filter(stock__abbreviation=company)))
    pre_range_buy = ret_vals[0] if len(ret_vals) else None
    pre_range_sale = ret_vals[1] if len(ret_vals) else None
    pre_range_profit = pre_range_sale.close - pre_range_buy.close if len(ret_vals) else "not"

    pre_range_more_trade_profit = more_trade_calculate(list(pre_range.filter(stock__abbreviation=company)))
    pre_range_better_stocks = compare(pre_range, company)

    in_range = DatesValues.objects.filter(date__range=[start_date, end_date])
    ret_vals = one_trade_calculate(list(in_range.filter(stock__abbreviation=company)))
    in_range_buy = ret_vals[0] if len(ret_vals) else None
    in_range_sale = ret_vals[1] if len(ret_vals) else None
    in_range_profit = in_range_sale.close - in_range_buy.close if len(ret_vals) else "not"

    in_range_more_trade_profit = more_trade_calculate(list(in_range.filter(stock__abbreviation=company)))
    in_range_better_stocks = compare(in_range, company)

    post_range = DatesValues.objects.filter(date__gte=post_range_start_date, date__lte=post_range_end_date, )
    ret_vals = one_trade_calculate(list(post_range.filter(stock__abbreviation=company)))
    post_range_buy = ret_vals[0] if len(ret_vals) else None
    post_range_sale = ret_vals[1] if len(ret_vals) else None
    post_range_profit = post_range_sale.close - post_range_buy.close if len(ret_vals) else "not"

    post_range_more_trade_profit = more_trade_calculate(list(post_range.filter(stock__abbreviation=company)))
    post_range_better_stocks = compare(post_range, company)

    processed_data = {"pre_range": {"in_date": pre_range_start_date.strftime("%m/%d/%Y"),
                                       "end_date": pre_range_end_date.strftime("%m/%d/%Y"),
                                       "best_buy_date": pre_range_buy.date.strftime("%m/%d/%Y"),
                                       "best_buy_close": pre_range_buy.close,
                                       "best_sale_date": pre_range_sale.date.strftime("%m/%d/%Y"),
                                       "best_sale_close": pre_range_sale.close,
                                       "profit": pre_range_profit,
                                       "more_trade_profit": pre_range_more_trade_profit,
                                       "better_stocks": pre_range_better_stocks},
                         "in_range": {"in_date": start_date.strftime("%m/%d/%Y"),
                                      "end_date": end_date.strftime("%m/%d/%Y"),
                                      "best_buy_date": in_range_buy.date.strftime("%m/%d/%Y"),
                                      "best_buy_close": in_range_buy.close,
                                      "best_sale_date": in_range_sale.date.strftime("%m/%d/%Y"),
                                      "best_sale_close": in_range_sale.close,
                                      "profit": in_range_profit,
                                      "more_trade_profit": in_range_more_trade_profit,
                                      "better_stocks": in_range_better_stocks},
                         "post_range": {"in_date": post_range_start_date.strftime("%m/%d/%Y"),
                                        "end_date": post_range_end_date.strftime("%m/%d/%Y"),
                                        "best_buy_date": post_range_buy.date.strftime("%m/%d/%Y"),
                                        "best_buy_close": post_range_buy.close,
                                        "best_sale_date": post_range_sale.date.strftime("%m/%d/%Y"),
                                        "best_sale_close": post_range_sale.close,
                                        "profit": post_range_profit,
                                        "more_trade_profit": post_range_more_trade_profit,
                                        "better_stocks": post_range_better_stocks},
                         }

    return processed_data


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

    for obj_buy in input_values:
        temp_profit = 0
        for obj_sale in input_values:
            if obj_buy.date >= obj_sale.date:
                continue
            # print(obj_buy.date, obj_sale.date)
            difference = obj_sale.close - obj_buy.close
            if difference > 0 and difference > temp_profit:
                temp_profit = difference

        profit += temp_profit
        # print(profit)

    # print(profit)
    return profit


def compare(query_set, company):
    stocks = Stock.objects.exclude(abbreviation=company)
    ret_list = []

    for stock in stocks:
        print(stock.name)
        stock_set = query_set.filter(stock=stock)
        if len(one_trade_calculate(list(stock_set))) > 0:
            ret_list.append(stock.name)

    for ret in ret_list:
        print(ret)

    return ret_list
