from FinMind.data import DataLoader
import pandas as pd
import os
import para
from build_history.inves_data_trans import investor_data_transformer


def build_margin_data(file_list_name, start_date, end_date):

    # 股票清單
    stock_id_list = pd.read_csv(os.getcwd()+'/'+file_list_name, dtype={'stock_id': str}, index_col=False)

    # 逐一去撈，並存為EXCEL
    for index, d in stock_id_list.iterrows():
        stock_id = d['stock_id']
        stock_name = d['stock_name']

        # 融資融券API
        margin_data = DataLoader().taiwan_daily_short_sale_balances(stock_id, start_date, end_date)
        # 三大法人API
        investor_data = DataLoader().taiwan_stock_institutional_investors(stock_id, start_date, end_date)
        investor_data = investor_data_transformer(investor_data)  # 轉換格式

        # 存檔
        filename = stock_id+'_'+stock_name + '.csv'
        # margin_data.to_csv(os.getcwd()+para.margin_dir+filename, encoding='utf-8-sig', index=None)
        # investor_data.to_csv(os.getcwd()+para.investors_dir+filename, encoding='utf-8-sig', index=None)
        # print(stock_id, stock_name, 'build_margin_data work')
        chips_data = margin_data.merge(investor_data, on=['date', 'stock_id'])
        chips_data.to_csv(os.getcwd()+'/chips_record/'+filename,
                          encoding='utf-8-sig', index=None)
        print(stock_id, stock_name, 'chips_data work')


if __name__ == '__main__':

    target_stocks_list_name = 'tracing_stock_list.csv'
    start_date = '2021-01-01'
    end_date = '2023-03-20'
    build_margin_data(target_stocks_list_name, start_date, end_date)
