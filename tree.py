from bs4 import BeautifulSoup
from urllib.request import urlopen
import re
import sys
import csv
import os
import pandas as pd

base_url = "https://shop.greattree.com.tw/greattree/"
output_csv = "tree.csv"
output_xls = "tree.xls"

myitems = []

#大樹
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

    productDivs = soup.find_all('a', attrs={'class': 'title-2'})

    my = []

    i = 0

    re1 = '(\\/)'  # Any Single Character 1
    re2 = '.*?'  # Non-greedy match on filler
    re3 = '(C)'  # Any Single Word Character (Not Whitespace) 1

    # 使用link抓資料

    for div in productDivs:
        print(end='')
        my.append(str(div['href']))
        #print(div['href'])

    # getitems("index.php?action=product_sort&prod_sort_uid=611")

    for ref in my:
        getitems(str(ref))

    #for item in myitems:
    #    print(item)

    writetocsv()

    '''
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

def getitems(url: str):

    myurl = base_url + url
    # printf("url: %s\n", myurl)
    try:
        html = urlopen(myurl, timeout=10).read().decode('utf-8')
    except Exception as e:
        print(e)
        sys.exit(-1)
    soup = BeautifulSoup(html, features='lxml')

    prdt_names = []
    prdt_prices = []

    productDivs = soup.find_all('div', attrs={'class': 'search-product-title'})
    productPriceDivs = soup.find_all('div', attrs={'class': 'price price_color'})
    for div in productDivs:
        # print(div)
        prdt_name = div.find_all('h2')

        for p in prdt_name:
            # print(p.get_text())
            prdt_names.append(str(p.get_text()))

    for div in productPriceDivs:
        mystr = str(div.get_text())
        # print(div.get_text())
        # print(mystr.split("$")[1])
        prdt_prices.append(str("$"+mystr.split("$")[1]))

    '''
    i = 0
    for p in prdt_names:
        print("prdt_names[%d]: " % i, end='')
        print(p)
        i = i + 1

    i = 0
    for p in prdt_prices:
        print("prdt_price[%d]: " % i, end='')
        print(p)
        i = i + 1
    '''

    if len(prdt_names) == len(prdt_prices):
        for i in range(0, len(prdt_names) - 1, 1):
            #myitems.append([prdt_names[i], prdt_prices[i]])
            item = [prdt_names[i], prdt_prices[i]]
            myitems.append(item)
            #myitems.append('\n')
            #writetocsv(myitems)
            #printf("%s, %s \n", prdt_names[i], prdt_prices[i])

    #writetocsv()


def printf(format, *args):
    sys.stdout.write(format % args)

'''
def writetocsv(data):
    if bool(data):
        with open(output_csv, "a", newline='') as csv_file:
            writer = csv.writer(csv_file, delimiter=',')
            # print("CALL IT")
            # writer.writerow(['品名', '價格'])
            # for line in data:
            # print(line)

            writer.writerow(data)
'''


def writetocsv():
    if bool(myitems):
        with open(output_csv, "a", newline='') as csv_file:
            writer = csv.writer(csv_file, delimiter='\n')
            # print("CALL IT")
            writer.writerow(['品名, 價格'])
            # for line in data:
            # print(line)
            writer.writerow(myitems)



def readfromcsv():
    i = 0
    with open(output_csv, newline='') as myFile:
        reader = csv.reader(myFile)
        for row in reader:
            # print("data[%d]: " % i, end='')
            # print(row)
            i = i + 1


def checkfile():
    if os.path.isfile(output_csv):
        os.remove(output_csv)


# 精簡html tag語法
def cleanhtml(raw_html):
    say = str(raw_html)
    cleanr = re.compile('<.*?>')
    cleantext = re.sub(cleanr, '', say)
    return cleantext


def csv_to_xlsx_pd():
    mycsv = pd.read_csv(output_csv, encoding='utf-8')
    mycsv.to_excel(output_xls, sheet_name='data')


# 進入點
if __name__ == '__main__':
    checkfile()
    getinfo()
    csv_to_xlsx_pd()
