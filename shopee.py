import requests
import json
import os
import csv
import sys
import pandas as pd
from selenium import webdriver

base_url = "https://shopee.tw/api/v2/search_items/"
output_csv = "shopee.csv"
output_xls = "shopee.xls"

#幫寶適
#get_para1 = '?by=relevancy&keyword=%E5%B9%AB%E5%AF%B6%E9%81%A9&limit=50&match_id=100&newest=0&order=desc&page_type=search'
get_para1 = '?by=price&keyword=%E5%B9%AB%E5%AF%B6%E9%81%A9&limit=50&newest=0&order=desc&page_type=search'

#頁數
get_para2 = '&page='

#排序
get_para3 = '&sortBy=relevancy'

refer_header = 'https://shopee.tw/search?category=100&keyword=%E5%B9%AB%E5%AF%B6%E9%81%A9&page=0&sortBy=price'

pagelimit = 50

items = []

cookie = {'enwiki_session': '17ab96bd8ffbe8ca58a78657a918558'}

def checkfile():
    if os.path.isfile(output_csv):
        os.remove(output_csv)


def getinfo(mycookie):
    header = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) '
                      'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36',
        #'X-api-source': 'pc',
        'X-requested-with': 'XMLHttpRequest',
        'Referer': 'https://shopee.tw/search?keyword=%E5%B9%AB%E5%AF%B6%E9%81%A9&order=desc&page=0&sortBy=price',
        'Accept': '*/*',
        #'Cookies': '__BWfp=c1511593309147x2a0f0ffef; SPC_F=WP7nEeiwHzBXR7544CSdnONec2sjCIL3; REC_T_ID=81eed1c2-d1ae-11e7-af60-c81f66de718d; _atrk_siteuid=8XcCVQrxaZQFRHAQ; csrftoken=2LeS0cqX6OrxH2XSxCNQ22rTHyfwxVvd; SPC_IA=-1; _ga=GA1.2.301573250.1511593309; __utmz=88845529.1515113659.3.3.utmcsr=google|utmccn=(organic)|utmcmd=organic|utmctr=(not%20provided); cto_lwid=602b8030-ec03-41b2-bc9b-495eaa31d239; __utma=88845529.301573250.1511593309.1515113659.1523580954.4; _gac_UA-61915057-6=1.1533480335.CjwKCAjwwJrbBRAoEiwAGA1B_e0Rpy3JtNlfCvNo0oHTxhj3fB-HVh-L3x8xhMNL3RXC2w20f0v9IRoC-moQAvD_BwE; _gcl_aw=GCL.1533480335.CjwKCAjwwJrbBRAoEiwAGA1B_e0Rpy3JtNlfCvNo0oHTxhj3fB-HVh-L3x8xhMNL3RXC2w20f0v9IRoC-moQAvD_BwE; SPC_SC_TK=1ff616e3cf045ace2660e0986f3813e7; SPC_SC_UD=40372974; _gid=GA1.2.1167799841.1535007087; SPC_T_ID="kN9ReyLxs7Wfm3EzZqbXqj9WUcr0Gpg8GqRctCIXOa7kv0crJKGac+T/Y+Vvb+1MLz24kJ8AXHhmWqPDuw/+B36sGcnold70yoXnKfMn0rk="; SPC_SI=eugvjmvk97ta85lfzysxvv0wrfky04y9; SPC_U=-; SPC_T_IV="9fYgryMz96nwXYhbTfYzFQ=="; SPC_EC=-; bannerShown=true; _gat=1',
        #'X-csrftoken': '2LeS0cqX6OrxH2XSxCNQ22rTHyfwxVvd',
        #'If-none-match': '1e4bf67a2e529e42ad15f4afd5aa5f64;gzip',
        #'If-none-match-': '55b03-ebeb1d2c0ecdd6e82b6b1ff386d7df04'
    }

    #'referer':'https://shopee.tw/search?keyword=%E5%B9%AB%E5%AF%B6%E9%81%A9&order=desc&page=0&sortBy=price'
    #res = requests.get(base_url + get_para1 + get_para2 + '0' + get_para3, headers=header)
    #mycookie = res.cookies

    # js = json.load()

    res = requests.get(base_url + get_para1 + get_para2 + '0' + get_para3, headers=header)
    #url = 'https://shopee.tw/search?category=100&keyword=%E5%B9%AB%E5%AF%B6%E9%81%A9&page=2&sortBy=relevancy'
    try:
        #print(res.text)
        myjson = json.loads(res.text)
    except Exception as e:
        print(e)
        sys.exit(1)

    total = myjson['total_count']
    lastpage = total // pagelimit
    last = total % pagelimit

    if last == 0:
        lastpage = lastpage - 1
    else:
        lastpage = lastpage

    #lastpage = 4
    items.append(['品名', '價格'])

    for i in range(0, lastpage, 1):
        res = requests.get(base_url+get_para1+get_para2+str(i)+get_para3, headers=header)
        #print(res.text)
        try:
            myjson = json.loads(res.text)
        except Exception as e:
            continue

        subjson = myjson['items']
        for item in subjson:
            prdt_names = item['name']

            if bool(item['price']):
                prdt_prices = str(int(item['price'])/100000)
            else:
                prdt_prices = '-1'
            myitems = [prdt_names, prdt_prices]
            items.append(myitems)

            #print(store_details)
        # print(myjson['items'])

    writetocsv(items)

def writetocsv(data):
    if bool(data):
        with open(output_csv, "w", newline='') as csv_file:
            writer = csv.writer(csv_file, delimiter='\n')

            # for line in data:
                # print(line)

            writer.writerow(data)

def parsecsv():
    '''
    i = 0
    mystr: str = []
    with open(output_csv, newline='') as myFile:
        reader = csv.reader(myFile)
        for row in reader:
            # print("data[%d]: " % i, end='')
            # print(row)
            mystr = row
            #print(mystr)
            i = i + 1
    '''
    #csv_data = pd.read_csv(output_csv)

    #print(csv_data)


def getcookie():

    driverLocation = '/Users/hsiehkaiyang/chromedriver/chromedriver'
    driver = webdriver.Chrome(driverLocation)
    driver.get("https://shopee.tw/")

    #print(driver.get_cookies())
    return driver.get_cookies()


def csv_to_xlsx_pd():
    mycsv = pd.read_csv(output_csv, encoding='utf-8')
    mycsv.to_excel(output_xls, sheet_name='data')


# 進入點
if __name__ == '__main__':
    #checkfile()
    #mycookie = getcookie()
    #getinfo(mycookie)
    #parsecsv()
    csv_to_xlsx_pd()
