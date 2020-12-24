import pandas as pd
from bs4 import BeautifulSoup
import requests
from tqdm import tqdm
import numpy as np

def get_bill(page_num, start_propose_date, end_propose_date): 
    billid = []
    billname = []
    billno = []
    generalresult = []
    passgubn = []
    procdt = []
    procstagecd = []
    proposedt = []
    proposerkind = []
    summary = []
    
    key = 'X8D3ieWlnaETG%2F8ao7onl%2FJ6safe1VHOT8dnqbiBW%2BrHTqj7uFAtJKpcSJ0XHli3SbGa0clTNkcne8G0xFWXWg%3D%3D'
    for n in tqdm(range(1, page_num+1), desc='Page No.'): 
        open_api = "http://apis.data.go.kr/9710000/BillInfoService2/getBillInfoList?serviceKey=" + key + \
                   f"&pageNo={n}" + f"&numOfRows=1000&mem_name_check=&mem_name=&hj_nm=&ord=&start_ord=&end_ord=&process_num=-&start_process_num=-&end_process_num=-&propose_num=-&start_propose_num=-&end_propose_num=-&start_propose_date={start_propose_date}&end_propose_date={end_propose_date}&start_committee_dt=&end_committee_dt=&bill_kind_cd=B04&curr_committee=&proposer_kind_cd=&p_proc_result_cd=&b_proc_result_cd=&bill_name=&gbn=&amendmentyn=&budget="

        res = requests.get(open_api)
        soup = BeautifulSoup(res.content, 'html.parser')
        items = soup.find_all('item')
        # print('의안 수:', len(items))
        for item in tqdm(items):
            billid.append(item.find('billid').text)
            billname.append(item.find('billname').text)
            billno.append(item.find('billno').text)
            try: 
                generalresult.append(item.find('generalresult').text)
            except:
                generalresult.append('-')
            try: 
                passgubn.append(item.find('passgubn').text)
            except: 
                passgubn.append('-')
            try: 
                procdt.append(item.find('procdt').text)
            except: 
                procdt.append('-')
            try: 
                procstagecd.append(item.find('procstagecd').text)
            except: 
                procstagecd.append('-')
            proposedt.append(item.find('proposedt').text)
            proposerkind.append(item.find('proposerkind').text)
            try: 
                summary.append(item.find('summary').text)
            except: 
                summary.append('-')
           
    bill_dict = {'의안 ID': billid, '의안명': billname, '의안번호': billno, 
                    '처리결과':generalresult, '처리구분': passgubn, '의결일자':procdt,
                    '심사진행상태':procstagecd, '제안일자': proposedt, '제안자구분':proposerkind,
                    '주요내용':summary}
    bill_df = pd.DataFrame(bill_dict)
    return bill_df 

# 17대 법률안 
print('17대 법률안 크롤링 시작합니다.')
bill_df = get_bill(329, '2004-05-30', '2008-05-29')
bill_df = bill_df.drop_duplicates()
print(len(bill_df))
bill_df.to_csv('17th-lawbill-list.csv', encoding='utf-8-sig')
print('17대 법률안 크롤링 완료')

# 18대 법률안 
bill_df = get_bill(497, '2008-05-30', '2012-05-29')
bill_df = bill_df.drop_duplicates()
print(len(bill_df))
bill_df.to_csv('18th-lawbill-list.csv', encoding='utf-8-sig')
print('18대 법률안 크롤링 완료')

# 19대 법률안 
bill_df = get_bill(661, '2012-05-30', '2016-05-29')
bill_df = bill_df.drop_duplicates()
print(len(bill_df))
bill_df.to_csv('19th-lawbill-list.csv', encoding='utf-8-sig')
print('19대 법률안 크롤링 완료')

# 20대 법률안 
bill_df = get_bill(894, '2016-05-30', '2020-05-29')
bill_df = bill_df.drop_duplicates()
print(len(bill_df))
bill_df.to_csv('20th-lawbill-list.csv', encoding='utf-8-sig')
print('20대 법률안 크롤링 완료')

# 21대 법률안 (2020.09.09 기준)
bill_df = get_bill(154, '2020-05-30', '2020-09-09')
bill_df = bill_df.drop_duplicates()
print(len(bill_df))
bill_df.to_csv('21st-lawbill-list.csv', encoding='utf-8-sig')
print('21대 법률안 크롤링 완료')