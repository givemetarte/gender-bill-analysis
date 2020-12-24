
from selenium import webdriver
from random import randint
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
from tqdm import tqdm
import time
import pandas as pd
import re

options = webdriver.ChromeOptions()
options.add_argument('headless')
options.add_argument('window-size=1920x1080')
options.add_argument("disable-gpu")
options.add_argument(
    "user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36")
# 혹은 options.add_argument("--disable-gpu")

driver = webdriver.Chrome(
    '/Users/harampark/Documents/chromedriver', chrome_options=options)
# driver = webdriver.Chrome('C:/Users/ramsclub/Downloads/chromedriver_win32.exe')
#driver = webdriver.Chrome('/Users/harampark/Documents/chromedriver')
# driver = webdriver.PhantomJS('C:/Users/ramsclub/Downloads/phantomjs-2.1.1-windows/phantomjs-2.1.1-windows/bin/phantomjs.exe')
url = 'http://likms.assembly.go.kr/bill/main.do'
driver.get(url)

search = driver.find_element_by_css_selector('li.gnbL2')
search.click()
time.sleep(2)
'''
driver.find_element_by_css_selector(
    '#AGE_AREA > select:nth-child(2) > option:nth-child(1)').click()

driver.find_element_by_css_selector(
    '#AGE_AREA > select:nth-child(3) > option:nth-child(1)').click()
'''
driver.find_element_by_css_selector(
    'body > div > div.contentWrap > div.subContents > div > form > div > div > div:nth-child(3) > select:nth-child(2) > option:nth-child(2)').click()

search = driver.find_element_by_css_selector('div.mt20.alignC > button.btnd')
search .click()
time.sleep(2)

more_bill = driver.find_element_by_css_selector(
    '#pageSizeOption > option:nth-child(4)').click()

num_list = []
# handled_list = []
title_list = []
proposer_type_list = []
propose_date_list = []
resolution_date_list = []
resolution_result_list = []
# progress_list = []

proposer_list = []
# paper_list = []
session_list = []
reason_list = []
board_list = []

n_times = 0

# 원하는 시작페이지
n_iter = 0


driver.find_element_by_css_selector(
    '#pageListViewArea > a:nth-child(11)').click()
while n_times <= n_iter - 2:
    driver.find_element_by_css_selector(
        '#pageListViewArea > a:nth-child(13)').click()
    n_times += 1

if n_iter == 0:
    start = 1
    end = 11
else:
    start = 3
    end = 13

# 10페이지가 끝나면 다음 10페이지를 불러옵니다.
while n_iter <= 6:

    # start번째 페이지에 접속합니다.
    for k in tqdm(range(start, end)):
        try:
            driver.find_element_by_css_selector(
                f'#pageListViewArea > a:nth-child({k})').click()
            # start번째 페이지의 i번째 의안에 접근합니다.
            for i in range(1, 101):
                # MAX_SLEEP_TIME = 4
                # rand_value = randint(2, MAX_SLEEP_TIME)
                # time.sleep(rand_value)
                # i 번째 의안에 접근합니다.
                bill = driver.find_element_by_css_selector(
                    f'body > div > div.contentWrap > div.subContents > div > div.tableCol01 > table > tbody > tr:nth-child({i})')

                num = bill.find_element_by_css_selector('td:nth-child(1)').text
                title = bill.find_element_by_css_selector('td.alignL').text
                proposer_type = bill.find_element_by_css_selector(
                    'td:nth-child(3)').text
                propose_date = bill.find_element_by_css_selector(
                    'td:nth-child(4)').text
                resolution_date = bill.find_element_by_css_selector(
                    'td:nth-child(5)').text
                resolution_result = bill.find_element_by_css_selector(
                    'td:nth-child(6)').text
                # progress = bill.find_element_by_css_selector('td:nth-child(8)').text

                num_list.append(num)

                # if resolution_date == '':
                # handled_list.append('계')
                # else:
                # handled_list.append('처')

                title_list.append(title)
                proposer_type_list.append(proposer_type)
                propose_date_list.append(propose_date)
                resolution_date_list.append(resolution_date)
                resolution_result_list.append(resolution_result)
                # progress_list.append(progress)

                # start번째 페이지의 i번째 의안에 접속합니다.
                bill = driver.find_element_by_css_selector(
                    f'body > div > div.contentWrap > div.subContents > div > div.tableCol01 > table > tbody > tr:nth-child({i}) > td.alignL > div.pl25 > a')
                try:
                    bill.click()
                except:
                    bill.send_keys(Keys.ENTER)

                # MAX_SLEEP_TIME = 3
                # rand_value = randint(1, MAX_SLEEP_TIME)
                # time.sleep(rand_value)
                # paper = driver.find_element_by_css_selector('body > div > div.contentWrap > div.subContents > div > div.contIn > div.tableCol01 > table > tbody > tr > td:nth-child(4)').text
                session = driver.find_element_by_css_selector(
                    'body > div > div.contentWrap > div.subContents > div > div.contIn > div.tableCol01 > table > tbody > tr > td:nth-child(5)').text

                # paper_list.append(paper)
                session_list.append(session)

                # 제안이유를 담습니다.
                try:
                    # 더 보기를 클릭합니다.
                    more_info = driver.find_element_by_css_selector(
                        '#summaryContentMoreBtn').click()
                    reason_raw_text = driver.find_element_by_css_selector(
                        'div.contIn > div.textType02').text

                    content = []
                    reason_split = re.split('\r|\t|\n|\xa0', reason_raw_text)
                    content.append(''.join(reason_split))
                    reason_list.append(content)

                except:
                    reason_list.append([])

                # 소관위원회를 담습니다.
                try:
                    board = driver.find_element_by_css_selector(
                        'body > div > div.contentWrap > div.subContents > div > div:nth-child(5) > div > table > tbody > tr > td:nth-child(1)').text
                    board_list.append(board)
                except:
                    board_list.append([])

                # 제안자를 담습니다.
                member_list = []
                try:
                    proposer = driver.find_element_by_css_selector(
                        'body > div > div.contentWrap > div.subContents > div > div.contIn > div.tableCol01 > table > tbody > tr > td:nth-child(3) > a > img')
                    proposer.click()

                    # 새로운 창으로 초점을 바꿉니다.
                    driver.switch_to_window(driver.window_handles[1])
                    driver.get_window_position(driver.window_handles[1])

                    member_num = len(driver.find_elements_by_tag_name('a'))
                    member_end = (member_num//3) + member_num + 2

                    for j in range(2, member_end):
                        try:
                            member = driver.find_element_by_css_selector(
                                f'#periodDiv > div.layerInScroll.coaTxtScroll > div > a:nth-child({j})').text
                            member_list.append(member)
                        except:
                            continue

                    driver.close()
                    proposer_list.append(member_list)

                    # 원래 창으로 초점을 바꿉니다.
                    driver.switch_to_window(driver.window_handles[0])
                    driver.get_window_position(driver.window_handles[0])

                except:
                    proposer_list.append([])

                print(i, '번째 의안 완료')
                driver.back()
                driver.execute_script(
                    "window.scrollTo(0, window.scrollY + 70)")

        except:
            print('해당 페이지 의안을 가져올 수 없습니다😱')
            pass
            break
    try:
        driver.find_element_by_css_selector(
            f'#pageListViewArea > a:nth-child({10+start})').click()
        if n_iter == 0:
            start = 1
            end = 11
        else:
            start = 3
            end = 13
        print(f'{n_iter}만큼 크롤링했습니다😍')
        n_iter += 1
    except:
        print('해당 페이지 버튼을 클릭할 수 없습니다😢')
        pass
        break


result = [num_list, title_list, propose_date_list, proposer_type_list, resolution_date_list,
          resolution_result_list, session_list, reason_list, board_list, proposer_list]
result_df = pd.DataFrame(result).T
result_df.columns = ['의안번호', '의안명', '제안일자', '제안자구분',
                     '의결일자', '의결결과', '제안회기', '제안이유', '소관위원회', '제안자']
print(len(result_df))

result_df.to_csv('21대 국회 의안정보.csv', encoding='utf-8-sig', index=False)
print('데이터가 저장되었습니다👏')
