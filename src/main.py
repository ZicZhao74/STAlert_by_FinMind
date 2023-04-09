import os
from backtesting import Backtest, Strategy
import pandas as pd
import shutil
import strategies


class DynamicStrategy(Strategy):
    def init(self):
        '''先處理好策略定義'''
        super().init()
        # read demanded strategies
        buy_strategies = pd.read_csv('config/buy.csv', thousands=',')
        sell_strategies = pd.read_csv('config/sell.csv', thousands=',')

        # for i, s in buy_strategies.iterrows():
        #     args = s[1:].to_list()
        #     print(getattr(strategies, s[0]))
        #     print(args)
        self.buy_strategies = []
        for i, s in buy_strategies.iterrows():
            func = getattr(strategies, s[0])
            args = s[1:].to_list()
            self.buy_strategies.append(func(*args))
        self.sell_strategies = [getattr(strategies, s[0])(*s[1:].to_list())
                                for i, s in sell_strategies.iterrows()]

    def next(self):
        if self.check_buy():
            self.buy(size=1000, )

        elif self.check_sell():
            # self.sell(size=1000)
            self.position.close()

    def check_buy(self):
        for s in self.buy_strategies:
            if s.check_buy(self.data) is True:
                continue
            else:
                return False
        return True

    def check_sell(self):
        for s in self.sell_strategies:
            if s.check_sell(self.data) is True:
                continue
            else:
                return False
        return True


if __name__ == '__main__':
    # 讀取歷史資料檔名列表
    stockList = pd.read_csv('data/stock_file_list.csv', thousands=',')
    # read demanded strategies
    # strategy = DynamicStrategy(strategyList, strategyList)
    # result = pd.DataFrame().set_index('stock')

    for index, stock in stockList.iterrows():
        stock_name = stock['Name']
        print(stock_name)
        # history_data = pd.DataFrame()
        history_data = pd.read_csv('data/price/'+stock_name, thousands=',')
        # history_data.rename(columns={"date": "Date"})
        # history_data.set_index("date", inplace=True)
        # history_data = history_data.set_index(
        #     pd.DatetimeIndex(pd.to_datetime(history_data.index)))

        bt = Backtest(history_data, DynamicStrategy, commission=0,
                      exclusive_orders=True, cash=100_0000)
        stats = bt.run()
        stats.name = stock_name
        bt.plot(open_browser=False, filename='result/'+stock[0])

        # 寫入Headers
        if (index == 0):
            result = stats.to_frame().T
            continue

        result.loc[stock_name] = stats

    result.to_csv('result/result.csv')
