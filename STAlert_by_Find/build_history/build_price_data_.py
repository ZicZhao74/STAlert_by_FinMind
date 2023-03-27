from FinMind.data import DataLoader
import pandas as pd
import os
from indicators import increase_indicators


def build_price_data(target_stocks_list_name, start_date, end_date):

    # 股票清單
    stock_id_list = pd.read_csv(
        os.getcwd()+'/'+target_stocks_list_name, dtype={'stock_id': str}, index_col=False)

    # 逐一去撈，並存為EXCEL
    for index, d in stock_id_list.iterrows():
        stock_id = d['stock_id']
        stock_name = d['stock_name']
        data = DataLoader().taiwan_stock_daily(stock_id, start_date, end_date)
        data = increase_indicators(data)

        filename = stock_id+'_'+stock_name + '.csv'
        data.to_csv(os.getcwd()+'/price_record/'+filename,
                    encoding='utf-8-sig', index=False)
        print(stock_id, stock_name, 'build_price_data work')


if __name__ == '__main__':

    target_stocks_list_name = 'tracing_stock_list.csv'
    start_date = '2021-01-01'
    end_date = '2023-03-20'
    build_price_data(target_stocks_list_name, start_date, end_date)

    # 建立檔名列表
    stock_file_list = pd.DataFrame(os.listdir(os.getcwd()+'/price_record/'))
    filelist_name = 'stock_file_list.csv'
    stock_file_list.to_csv(filelist_name, index=False,
                           encoding='utf-8-sig')
