import pandas as pd
import requests
from bs4 import BeautifulSoup
from styleframe import StyleFrame
from os import path
import re

StyleFrame.A_FACTOR = 13
StyleFrame.P_FACTOR = 1.5

cn_to_int = {'一': 0, '二': 1, '三': 2, '四': 3, '五': 4, '六': 5, '日': 6}
class_map = {'0': 0, '1': 1, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, '10': 10, 'A': 11, 'B': 12,
             'C': 13, 'D': 14}


def soup_to_df(soup):
    table_raw = soup.find('table', border="1", cellspacing="1", cellpadding="1", bordercolorlight="#CCCCCC",
                          bordercolordark="#CCCCCC")
    table_row = table_raw.select('tr')
    data = []
    for tr in table_row[1:]:
        td = tr.find_all('td')
        data.append([tr.text.strip() for tr in td])

    try:
        df = pd.DataFrame(data,
                          columns=['流水號', '授課對象', '課號', '班次', '課程名稱', '簡介影片', '學分', '課程識別碼', '全/半年', '必/選修', '授課教師',
                                   '加選方式', '時間教室', '總人數', '選課限制條件', '備註', '課程網頁', '本學期我預計要選的課程'])
    except ValueError:
        df = pd.DataFrame(data,
                          columns=['流水號', '授課對象', '課號', '班次', '課程名稱', '簡介影片', '學分', '課程識別碼', '全/半年', '授課教師', '加選方式',
                                   '時間教室', '總人數', '選課限制條件', '備註', '課程網頁', '本學期我預計要選的課程'])
    df['classroom'] = ''
    for i in range(7):
        for j in range(15):
            df['time_' + str(i) + '_' + str(j)] = 0
    for i in range(1, 9):
        df['A' + str(i)] = 0
    return df


def url_to_df(mode='9010', sem='110-1', startrec=0):
    # get url
    url = ''
    if type(mode) == int:
        mode = str(mode)
    if len(mode) == 3:
        mode += '0'

    if mode == '通識':
        url = "https://nol.ntu.edu.tw/nol/coursesearch/search_for_03_co.php?alltime=yes&allproced=yes&selcode=-1&coursename=&teachername=&current_sem=" + sem + "&yearcode=0&op=&startrec=0&week1=&week2=&week3=&week4=&week5=&week6=&proced0=&proced1=&proced2=&proced3=&proced4=&procedE=&proced5=&proced6=&proced7=&proced8=&proced9=&procedA=&procedB=&procedC=&procedD=&allsel=yes&selCode1=&selCode2=&selCode3=&page_cnt=20000"
    elif mode == '體育':
        url = "https://nol.ntu.edu.tw/nol/coursesearch/search_for_09_gym.php?current_sem=" + sem + "&op=S&startrec=" + \
              str(startrec) + "&cou_cname=&tea_cname=&year_code=2&checkbox=&checkbox2=&alltime=yes&allproced=yes&week1=&week2=&week3=&week4=&week5=&week6=&proced0=&proced1=&proced2=&proced3=&proced4=&procedE=&proced5=&proced6=&proced7=&proced8=&proced9=&procedA=&procedB=&procedC=&procedD="
    elif mode == '外文':
        url = "https://nol.ntu.edu.tw/nol/coursesearch/search_for_01_major.php?alltime=yes&allproced=yes＆selcode=-1&coursename&teachername&couarea=7&current_sem=" + sem + "&yearcode=0&op&startrec=0&week1&week2&week3&week4&week5&week6&proced0&proced1&proced2&proced3&proced4&procedE&proced5&proced6&proced7&proced8&proced9&procedA&procedB&procedC&procedD&allsel=yes&selCode1&selCode2&selCode3&page_cnt=20000&fbclid=IwAR1rbn6rZfQM5ETlZRqXNvMN-Wg6ChCBduyccCxOPdDfzgOMIPclNcSJmnw"
    elif mode == '共同':
        url = "https://nol.ntu.edu.tw/nol/coursesearch/search_for_01_major.php?alltime=yes&allproced=yes＆selcode=-1&coursename&teachername&current_sem=" + sem + "&yearcode=0&op&startrec=0&week1&week2&week3&week4&week5&week6&proced0&proced1&proced2&proced3&proced4&procedE&proced5&proced6&proced7&proced8&proced9&procedA&procedB&procedC&procedD&allsel=yes&selCode1&selCode2&selCode3&page_cnt=20000&fbclid=IwAR1rbn6rZfQM5ETlZRqXNvMN-Wg6ChCBduyccCxOPdDfzgOMIPclNcSJmnw"
    else:
        url = "https://nol.ntu.edu.tw/nol/coursesearch/search_for_02_dpt.php?alltime=yes&allproced=yes&selcode=-1&dptname=" + mode + \
              "&coursename&teachername&current_sem=" + sem + \
              "&yearcode=0&op&startrec=0&week1&week2&week3&week4&week5&week6&proced0&proced1&proced2&proced3&proced4&procedE&proced5&proced6&proced7&proced8&proced9&procedA&procedB&procedC&procedD&allsel=yes&selCode1&selCode2&selCode3&page_cnt=20000&fbclid=IwAR2rwV0EENp6Yf5XmXrl1CGotWEXHtw2eBb-7gGFO-PbhjJCfYN3v1q_9sc"

    # get soup
    response = requests.get(url)
    response.encoding = 'big5'
    soup = BeautifulSoup(response.text, "html.parser")

    # soup to df
    df = soup_to_df(soup)
    return df


def get_time(df):
    for i, raw in enumerate(df['時間教室']):
        m = re.findall(r'(\S*?)\((.*?)\)', raw)
        for group in m:
            time_raw = group[0]
            df.at[i, 'classroom'] = group[1]
            time_raw = re.match(r'週?(.)(.*)', time_raw)
            weekday = cn_to_int[time_raw.group(1)]
            periods = time_raw.group(2).split(',')
            for period in periods:
                period = class_map[period]
                df.at[i, 'time_' + str(weekday) + '_' + str(period)] = 1
    return df


def get_field(df):
    for i, raw in enumerate(df['備註']):
        m = re.search(r'A(\d*)', raw)
        if m:
            for f in m.group(1):
                df.at[i, 'A' + f] = 1
    return df


def get_df(mode='9010', sem='110-1', startrec=0):
    df = url_to_df(mode, sem, startrec)
    df = get_time(df)
    df = get_field(df)
    return df


def save_csv(mode='系所', sem='110-1'):
    if mode == '體育':
        df = get_df(mode, sem, 0)
        for i in range(15, 210, 15):
            df = df.append(get_df(mode, sem, i), ignore_index=True, sort=False)
    else:
        df = get_df(mode, sem)
    df.to_csv('./save_csv/' + mode + '.csv', encoding='utf-8-sig', index=0)


def read_csv(name):
    if not path.exists(f'save_csv/{name}.csv'):
        save_csv(mode=name)
    if path.exists(f'new_csv/{name}.csv'):
        df = pd.read_csv(f'new_csv/{name}.csv')
    else:
        df = pd.read_csv(f'save_csv/{name}.csv')
    return df


def prefered_cols(df, cols=None):
    if cols is None:
        if '必/選修' in df.columns:
            cols = ['流水號', '課程名稱', '學分', '全/半年', '必/選修', '授課教師', '加選方式', '時間教室', '總人數', '選課限制條件', '備註']
        else:
            cols = ['流水號', '課程名稱', '學分', '全/半年', '授課教師', '加選方式', '時間教室', '總人數', '選課限制條件', '備註']

    if '登記人數' in df.columns:
        cols += ['人數上限', '登記人數', '剩餘名額']
    return df[cols]


def general_filter(name, writer, schedule, fields):
    df = read_csv('通識')

    for i in range(7):
        for j in range(15):
            if schedule[i][j]:
                df.drop(df[df['time_' + str(i) + '_' + str(j)] == 1].index, inplace=True)
    df.drop(df[~df[['A' + f for f in fields]].any(axis=1)].index, inplace=True)
    if name == 'Ray':
        df.drop(df[df['備註'].str.contains('限非電資|限電資學院以外', regex=1)].index, inplace=True)
    df = prefered_cols(df)
    sf = StyleFrame(df)
    sf.to_excel(writer, sheet_name='通識', index=0, row_to_add_filters=0,
                best_fit=['流水號', '課程名稱', '學分', '全/半年', '授課教師', '加選方式', '時間教室', '總人數', '選課限制條件', '備註'])
    print(name + ' 通識 export success')
    return df


def department_filter(name, dpt, writer, schedule):
    if type(dpt) == int:
        dpt = str(dpt)
    df = read_csv(dpt)

    for i in range(7):
        for j in range(15):
            if schedule[i][j]:
                df.drop(df[df['time_' + str(i) + '_' + str(j)] == 1].index, inplace=True)
    df.drop(df[df['課程名稱'].str.contains('服務學習|專題研究', regex=1)].index, inplace=True)

    df = prefered_cols(df)
    sf = StyleFrame(df)
    sf.to_excel(writer, sheet_name=dpt, index=0, row_to_add_filters=0,
                best_fit=['流水號', '課程名稱', '學分', '全/半年', '授課教師', '加選方式', '時間教室', '總人數', '選課限制條件', '備註'])
    print(name + ' ' + dpt + ' export success')
    return df


def language_filter(name, writer, schedule):
    df1 = read_csv('共同')
    df2 = read_csv('外文')

    df = df1.append(df2, ignore_index=True, sort=False)
    # print(df)
    for i in range(7):
        for j in range(15):
            if schedule[i][j]:
                df.drop(df[df['time_' + str(i) + '_' + str(j)] == 1].index, inplace=True)
    df.drop(df[df['課程名稱'].str.contains('國際|僑生', regex=1)].index, inplace=True)
    # df.drop(df[df['選課限制條件'].str.contains('限生農學院學生|限僑生、國際學生|限醫學院學生|限文學院學生|限學士班一年級|限國際學生', regex=1)].index, inplace=True)

    df = prefered_cols(df)
    sf = StyleFrame(df)
    sf.to_excel(writer, sheet_name='共同', index=0, row_to_add_filters=0,
                best_fit=['流水號', '課程名稱', '學分', '全/半年', '授課教師', '加選方式', '時間教室', '總人數', '選課限制條件', '備註'])
    print(name + ' 語文 export success')
    return df


def pe_filter(name, writer, schedule):
    df = read_csv('體育')

    for i in range(7):
        for j in range(15):
            if schedule[i][j]:
                df.drop(df[df['time_' + str(i) + '_' + str(j)] == 1].index, inplace=True)

    df = prefered_cols(df)
    sf = StyleFrame(df)
    sf.to_excel(writer, sheet_name='體育', index=0, row_to_add_filters=0,
                best_fit=['流水號', '課程名稱', '學分', '全/半年', '授課教師', '加選方式', '時間教室', '總人數', '選課限制條件', '備註'])
    print(name + ' 體育 export success')
    return df


if __name__ == "__main__":
    # print(get_url(mode='通識'))
    # print(url_to_df(mode='通識'))
    # print(url_to_df(mode='9010'))
    print(url_to_df(mode='體育'))
    # print(url_to_df(mode='所有'))

    pd.set_option('display.max_columns', None)
    save_csv(mode='9010')
    save_csv(mode='9020')
    save_csv(mode='通識')
    save_csv(mode='體育')
