
import os
from ast import List
import json
import pandas as pd
from custom_types import Order

from indexes import MAlowsupport, kd_passavation, MApass, volume_explode

SELL_RATIO_THRESHOLD = 0.10


def checkStrategyPass(index, rule):

    return False


def checkOrder():
    pass


def backTest(target, data: pd.DataFrame, strategies):
    orders: List[Order] = []
    for index, d in data.iterrows():
        # print([strategy(data, index) for strategy in strategies])
        if all([strategy(data, index) for strategy in strategies]):
            orders.append(Order(
                d[0],
                data.at[index+1, 'open'],
            ))
        if len(orders) == 0:
            continue
        unsold_orders = filter(lambda order: order.isSold is False, orders)
        for order in unsold_orders:
            # print(json.dumps(last_order.__dict__))
            if order and order.isSold is False:
                price_diff = d['close'] - order.buy_price
                price_diff_with_high = d['high'] - order.buy_price

                price_diff_ratio = price_diff / order.buy_price
                price_diff_ratio_with_heigh = price_diff_with_high / order.buy_price
                if abs(price_diff_ratio) > SELL_RATIO_THRESHOLD:
                    order.isSold = True
                    order.profit = round(price_diff, 2)
                    order.sell_date = d[0]
                    order.sell_price = d['close']
                    order.sell_on = 'close'
                elif abs(price_diff_ratio_with_heigh) > SELL_RATIO_THRESHOLD:
                    order.isSold = True
                    order.profit = round(price_diff_with_high, 2)
                    order.sell_date = d[0]
                    order.sell_price = d['high']
                    order.sell_on = 'high'
    # print(json.dumps([o.__dict__ for o in orders], sort_keys=True, indent=4))

    # for order in orders:
    #     pass
    order_count = len(orders)
    win_ratio = sum([order.profit >
                    0 for order in orders]) / order_count if order_count > 0 else 0
    profit = sum(order.profit for order in orders)
    return order_count, round(win_ratio*100, 2), round(profit, 2)


if __name__ == '__main__':
    # 讀取歷史資料檔名列表
    stockList = pd.read_csv('data/stock_file_list.csv', thousands=',')
    # stockList..astype(float)

    print(os.getcwd())
    for index, stock in stockList.iterrows():
        print(stock[0])
        history_data = pd.read_csv(
            os.getcwd()+'/data/price/'+stock[0], thousands=',')
        order_count, win_ratio, profit = backTest(
            stock, history_data, [volume_explode(2)])
        print(f'{order_count}次, {win_ratio}%勝率, ${profit}')
