from bs4 import BeautifulSoup
from urllib.request import urlopen
import re
import sys
import csv
import os
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

base_url = "https://www.wholecome.tw/shop/"
output_csv = "wholecome.csv"
output_xls = "wholecome.xls"

myitems = []

# 合康
def getinfo():

    # his = ["/item/%E7%BD%91%E7%BB%9C%E7%88%AC%E8%99%AB/5162711"]
    his = []

    url = base_url + ""

    # 取得網址
    try:
        html = urlopen(url, timeout=10).read().decode('utf-8')
    except Exception as e:
        print(e)
        sys.exit(1)

    soup = BeautifulSoup(html, features='lxml')
    # print("URL: ", end='')
    # print(soup.find('headNav').get_text())

    # 网络爬虫     url:

    # find valid urls
    # sub_urls = soup.find_all("a", {"target": "_top", "href": re.compile("/TinTin/EC*")})

    productDivs = soup.find_all('div', attrs={'id': 'cate-list'})

    my = []

    for div in productDivs:
        groups = div.find_all('dl', attrs={'class': 'cate-group'})
        for item in groups:
            # print(item)
            item_as = item.find_all('a')
            for aitem in item_as:
                my.append(aitem['href'])
                # print(aitem)

        # print(div)

    i = 0

    for ref in my:
        getitems(str(ref))

    '''
    re1 = '(\\/)'  # Any Single Character 1
    re2 = '.*?'  # Non-greedy match on filler
    re3 = '(C)'  # Any Single Word Character (Not Whitespace) 1

    for div in productDivs:
        # print(div)
        a = div.find_all('a', attrs={'class': 'headNav'})

        for ref in a:
            rg = re.compile(re1 + re2 + re3, re.IGNORECASE | re.DOTALL)
            m = rg.search(str(ref))
            if m:
                # print("%d: " % i, end='')
                # print(ref['href'])
                my.append(str(ref['href']))
                i = i + 1

        i = 0

        for ref in my:
            getitems(str(ref))
            #print("%d: " % i, end='')
            #print(ref)
            #i = i + 1


        # 使用link抓資料
    '''
    writetocsv(myitems)


def getitems(url: str):

    myurl = base_url + url
    #printf("url: %s\n", myurl)
    # 取得網址
    try:
        html = urlopen(myurl, timeout=10).read().decode('utf-8')
    except Exception as e:
        print(e)
        sys.exit(1)

    soup = BeautifulSoup(html, features='lxml')

    prdt_names = []
    prdt_prices = []

    productDivs = soup.find('div', attrs={'class': 'prod-div'})
    # print(productDivs)

    if bool(productDivs) == False:
        return

    prdt_name = productDivs.find_all('div', attrs={'class': 'prod-block'})
    prdt_price = productDivs.find_all('div', attrs={'class': ['prod-img-price-b']})
    for p in prdt_name:
        # print(p['title'])
        prdt_names.append(str(p['title']))

    for p in prdt_price:
        # print(str(p.find('span').get_text()))
        prdt_prices.append(str(p.find('span').get_text()))
    '''
    i = 0
    for p in prdt_names:
        #print("prdt_names[%d]: " % i, end='')
        #print(p)
        i = i + 1

    i = 0
    for p in prdt_prices:
        #print("prdt_price[%d]: " % i, end='')
        #print(p)
        i = i + 1
    '''

    if len(prdt_names) == len(prdt_prices):
        for i in range(0, len(prdt_names) - 1, 1):
            price = prdt_prices[i].replace(",", "")
            items = [prdt_names[i], price]
            myitems.append(items)


    # readfromcsv()


def printf(format, *args):
    sys.stdout.write(format % args)


def writetocsv(data):
    if bool(data):
        with open(output_csv, "a", newline='') as csv_file:
            writer = csv.writer(csv_file, delimiter="\n")
            writer.writerow(['品名, 價格'])
            # for line in data:
                # print(line)

            writer.writerow(data)


def readfromcsv():
    i = 0
    with open(output_csv, newline='') as myFile:
        reader = csv.reader(myFile)
        for row in reader:
            #print("data[%d]: " % i, end='')
            #print(row)
            i = i + 1


def checkfile():
    if os.path.isfile(output_csv):
        os.remove(output_csv)


# exists
def csv_to_xlsx_pd():
    mycsv = pd.read_csv(output_csv, encoding='utf-8')
    mycsv.to_excel(output_xls, sheet_name='data')


# 進入點
if __name__ == '__main__':
    checkfile()
    getinfo()
    csv_to_xlsx_pd()
