import pandas as pd
from bs4 import BeautifulSoup
import requests
from tqdm import tqdm
import numpy as np

def get_committee(bill_df):
    bill_id_list = bill_df['의안 ID'].to_list()
    committeelist = []
    key = 'X8D3ieWlnaETG%2F8ao7onl%2FJ6safe1VHOT8dnqbiBW%2BrHTqj7uFAtJKpcSJ0XHli3SbGa0clTNkcne8G0xFWXWg%3D%3D'
    for bill_id in tqdm(bill_id_list): 
        open_api = f"http://apis.data.go.kr/9710000/BillInfoService2/getBillCommissionExaminationInfo?serviceKey={key}&bill_id={bill_id}"

        res = requests.get(open_api)
        soup = BeautifulSoup(res.content, 'html.parser')

        try: 
            committeename = soup.find('committeename').get_text()
            committeelist.append(committeename)
            # print('committeename')
        except: 
            committeelist.append('-')
            # print('-')

    bill_df['소관위원회'] = committeelist   
    return bill_df

# 19대 의안 
bill_df = pd.read_csv(open('/Users/harampark/Documents/research/gender-bill-analysis/data/19th-lawbill-list.csv', 'rU'), index_col=0, encoding='utf-8')
bill_df = get_committee(bill_df)
bill_df.to_csv('19th-lawbill-list.csv', encoding='utf-8-sig')

# 20대 의안 
bill_df = pd.read_csv(open('/Users/harampark/Documents/research/gender-bill-analysis/data/20th-lawbill-list.csv', 'rU'), index_col=0, encoding='utf-8')
bill_df = get_committee(bill_df)
bill_df.to_csv('20th-lawbill-list.csv', encoding='utf-8-sig')

# 21대 의안
bill_df = pd.read_csv(open('/Users/harampark/Documents/research/gender-bill-analysis/data/21th-lawbill-list.csv', 'rU'), index_col=0, encoding='utf-8')
bill_df = get_committee(bill_df)
bill_df.to_csv('21th-lawbill-list.csv', encoding='utf-8-sig')
