from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from bs4 import BeautifulSoup
import pandas as pd
import glob


data = []
urls = ['http://140.112.161.154/regquery/Chinese.aspx',
        'http://140.112.161.154/regquery/Foreign.aspx',
        'http://140.112.161.154/regquery/Reqcou.aspx',
        'http://140.112.161.154/regquery/FreshmanSeminar.aspx',
        'http://140.112.161.154/regquery/Physical.aspx',
        'http://140.112.161.154/regquery/MilTr.aspx',]

options = Options()
options.add_argument('--headless')
driver = webdriver.Chrome('./chromedriver', options=options)

for url in urls:
    print(url)
    driver.get(url)
    while True:
        try:
            WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.CLASS_NAME, 'main')))
        except Exception as e:
            print(e)

        soup = BeautifulSoup(driver.page_source, 'html.parser')

        table_raw = soup.find('table', id='MainContent_GridView1')

        if table_raw is None:
            print('None')
            break

        table_row = table_raw.select('tr')

        for tr in table_row[1:-2]:
            td = tr.find_all('td')
            data.append([t.text.strip() for t in td])

        try:
            next_page = driver.find_element_by_link_text('下一頁').click()
        except NoSuchElementException:
            break

driver.get('http://140.112.161.154/regquery/Dept.aspx')
try:
    WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.CLASS_NAME, 'main')))
except Exception as e:
    print(e)

soup = BeautifulSoup(driver.page_source, 'html.parser')

colleges = soup.find('select', id="MainContent_ddCollege")
colleges = colleges.select('option')
# print(colleges)

for college in colleges[1:]:
    print(college['value'])

    colleges_select = Select(driver.find_element_by_id("MainContent_ddCollege"))
    colleges_select.select_by_value(college['value'])
    try:
        WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.ID, "MainContent_ddDptcode")))
    except Exception as e:
        print(e)
    soup = BeautifulSoup(driver.page_source, 'html.parser')

    depts = soup.find('select', id="MainContent_ddDptcode")
    depts = depts.select('option')
    for dept in reversed(depts):
        print('-', dept['value'])
        dept_select = Select(driver.find_element_by_id("MainContent_ddDptcode"))
        dept_select.select_by_value(dept['value'])
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        while True:
            try:
                WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.CLASS_NAME, 'main')))
            except Exception as e:
                print(e)

            soup = BeautifulSoup(driver.page_source, 'html.parser')

            table_raw = soup.find('table', id='MainContent_GridView1')

            if table_raw is None:
                print('None')
                break

            table_row = table_raw.select('tr')

            for tr in table_row[1:-2]:
                td = tr.find_all('td')
                data.append([t.text.strip() for t in td])

            try:
                next_page = driver.find_element_by_link_text('下一頁').click()
            except NoSuchElementException:
                try:
                    next_page = driver.find_element_by_link_text('第一頁').click()
                except NoSuchElementException:
                    pass
                break

driver.quit()

df_new = pd.DataFrame(data, columns=['流水號', '課號', '課程識別碼', '班次', '課程名稱', '學分', '授課教師', '通識領域', '加選方式', '上課時間',
                                     '限制條件', '人數上限', '外系上限', '外校上限', '已選上人數', '已選上外系人數', '登記人數', '剩餘名額'])
df_new = df_new[['流水號', '人數上限', '外系上限', '外校上限', '已選上人數', '已選上外系人數', '登記人數', '剩餘名額']]
print(df_new)
df_new.to_csv('./save_csv/popularity.csv', encoding='utf-8-sig', index=False)

for file in glob.iglob('./save_csv/' + '**/*' + '.csv', recursive=True):
    if str(file) == './save_csv/popularity.csv':
        continue
    print(file)
    df_old = pd.read_csv(file)
    df_old['流水號'] = df_old['流水號'].fillna(0).astype(int)
    # print(df_old.head())

    df_new = df_new.astype(int)

    df = pd.merge(df_old, df_new, on='流水號', how='left')
    print(df)
    file_name = file.split('/')[-1]
    df = df.sort_values(by=['登記人數'], ascending=False)
    df.to_csv(f'./new_csv/{file_name}', encoding='utf-8-sig', index=False)