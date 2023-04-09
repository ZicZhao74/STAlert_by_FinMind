
from pandas import DataFrame
from backtesting import Strategy
from backtesting.test import SMA


def kd_passavation(data, x):  # kd值三日鈍化判斷
    if data.at[x, 'k'] > 0.8 and data.at[x-1, 'k'] > 0.8 and data.at[x-2, 'k'] > 0.8 and data.at[x-3, 'k'] < 0.8:
        kd = True
    else:
        kd = False
    return kd


def MApass(data, x):
    '''
    123
    '''
    if data.at[x-2, '20MA'] > data.at[x-2, 'close'] and data.at[x-1, '20MA'] > data.at[x-1, 'close'] and data.at[x, '20MA'] < data.at[x, 'close']:
        MApassJ = True
    else:
        MApassJ = False
    return MApassJ


def MAlowsupport(data: DataFrame, x: int):
    '''20MA有支撐'''
    if x < 2:
        return False
    if data.at[x-2, '20MA'] < data.at[x-2, 'close'] and data.at[x-1, '20MA'] < data.at[x-1, 'close'] and data.at[x, 'low'] <= data.at[x, '20MA'] < data.at[x, 'close']:
        MAlowsupportJ = True
    else:
        MAlowsupportJ = False
    return MAlowsupportJ


def sma5(strategy: Strategy, price, period):
    return strategy.I(SMA, price, period)


def volume_explode(multi: int):
    '''
    curring化的偏函數
    '''
    def volume_explode2(data: DataFrame, x: int):
        ave_volume = data['Trading_Volume'].mean()
        if data.at[x, "Trading_Volume"] > multi*ave_volume:  # 低於平均交易量的1倍
            explode = True
        else:
            explode = False
        return explode
    return volume_explode2
