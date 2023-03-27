import pandas as pd
import para
from FinMind.data import DataLoader
import datetime
import os
from build_history.inves_data_trans import investor_data_transformer
path = os.getcwd()
api = DataLoader()
files_list = pd.read_csv(path+'/stock_file_list.csv', encoding='utf-8-sig')

# 更新每日股價、融資融券、三大法人
# for 所有股票
#     每日股價

if __name__ == '__main__':

    # today = datetime.datetime.now()-datetime.timedelta(days=1)
    today = datetime.datetime.now()
    today_str = datetime.datetime.strftime(today, '%Y-%m-%d')

    # 依列表更新個股
    for index, per in files_list.iterrows():

        filename = per[0]
        stock_id, stock_name = per[0].split('_')
        print(stock_id, stock_name)

    # 股價資料
        # 取歷史股價資料準備更新
        history_price_data = pd.read_csv(
            path+para.price_dir+filename, encoding='utf-8-sig', dtype={'stock_id': str})
        # 若重複結束
        if history_price_data.iloc[-1].at['date'] == today_str:
            print('repeat')

        # 撈取今日資料並合併
        else:
            new_price_data = api.taiwan_stock_daily(stock_id, today_str, today_str)
            price_data = pd.concat([history_price_data, new_price_data]).reset_index(drop=True)
            price_data.to_csv(path+para.price_dir+filename,
                              encoding='utf-8-sig', index=None)

    # 融資融券、三大法人
        # 取歷史股價資料準備更新
        history_chip_data = pd.read_csv(
            path+para.chip_dir+filename, encoding='utf-8-sig', dtype={'stock_id': str})
        # 若重複結束
        if history_chip_data.iloc[-1].at['date'] == today_str:
            print('repeat')
        else:
            # 撈取今日資料並合併
            # 融資融券API
            margin_data = DataLoader().taiwan_daily_short_sale_balances(stock_id, today_str, today_str)
            # 三大法人API
            investor_data = DataLoader().taiwan_stock_institutional_investors(stock_id, today_str, today_str)
            investor_data = investor_data_transformer(investor_data)  # 轉換格式
            # 左右合併
            chips_data = margin_data.merge(investor_data, on=['date', 'stock_id'])
            # 新舊合併
            chips_data = pd.concat([history_chip_data, chips_data]).reset_index(drop=True)
            chips_data.to_csv(os.getcwd()+'/chips_record/'+filename,
                              encoding='utf-8-sig', index=None)


# 每月更新營收表

# 基本資料
