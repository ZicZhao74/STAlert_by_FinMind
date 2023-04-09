from abc import abstractmethod
from enum import Enum
from backtesting import Strategy
from backtesting.test import SMA
from backtesting.lib import crossover
from pandas import DataFrame


class StrategyType(Enum):
    Buy = 1
    Sell = 2


class MyStrategy:
    '''工廠模式'''
    @abstractmethod
    def __init__(self, *args):
        # self.strategyType = strategyType
        pass

    @abstractmethod
    def check(self, data):
        pass


def SlowKFuncSell(data):
    return crossover(data.slowk, 80)


class SlowK(MyStrategy):
    def __init__(self, *args):
        # super.__init__()
        self.threshold = args[0]

    def check_buy(self, data):
        if crossover(self.threshold, data.slowk):
            # print(self.threshold)
            return True
        return False

    def check_sell(self, data):
        # print('qqq', type(self.threshold))
        if crossover(data.slowk, self.threshold):
            return True
        return False


class SmaCross(Strategy):
    def init(self):
        price = self.data.Close
        self.ma1 = self.I(SMA, price, 10)
        self.ma2 = self.I(SMA, price, 20)

    def next(self):
        if crossover(self.ma1, self.ma2):
            self.buy()
        elif crossover(self.ma2, self.ma1):
            self.sell()


def MAlowsupport():
    '''20MA有支撐'''
    def gogogo(data: DataFrame, x: int):
        if x < 2:
            return False
        if data.at[x-2, '20MA'] < data.at[x-2, 'close'] and data.at[x-1, '20MA'] < data.at[x-1, 'close'] and data.at[x, 'low'] <= data.at[x, '20MA'] < data.at[x, 'close']:
            MAlowsupportJ = True
        else:
            MAlowsupportJ = False
        return MAlowsupportJ
    return gogogo
