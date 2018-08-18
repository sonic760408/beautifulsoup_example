from bs4 import BeautifulSoup
from urllib.request import urlopen
import re
import sys
import csv
import os

base_url = "http://www.te-chang.com/"
output_csv = "techang.csv"


# 德昌
def getinfo():
    # his = ["/item/%E7%BD%91%E7%BB%9C%E7%88%AC%E8%99%AB/5162711"]
    his = []

    url = base_url + ""

    # 取得網址
    try:
        html = urlopen(url, timeout=10).read().decode('utf-8')
    except Exception as e:
        print(e)
        sys.exit(-1)
    soup = BeautifulSoup(html, features='lxml')
    # print("URL: ", end='')
    # print(soup.find('headNav').get_text())

    # 网络爬虫     url:

    # find valid urls
    # sub_urls = soup.find_all("a", {"target": "_top", "href": re.compile("/TinTin/EC*")})

    #get links
    a = soup.find_all('a', attrs={'class': ''})
    mylinks = []

    for item in a:
        re1 = '(goods\\.php)'  # Fully Qualified Domain Name 1

        rg = re.compile(re1, re.IGNORECASE | re.DOTALL)
        m = rg.search(str(item))
        if m:
            mylinks.append(str(item['href']))

    #for item in mylinks:
        # print(item)

    i = 0

    for ref in mylinks:
        # print(ref)
        getitems(str(ref))
        # print("%d: " % i, end='')
        # print(ref)
        # i = i + 1


def getitems(url: str):
    myurl = base_url + url
    # printf("url: %s\n", myurl)
    html = []
    try:
        html = urlopen(myurl, timeout=10).read().decode('utf-8')
    except Exception as e:
        print(e)
        # sys.exit(1)

    soup = BeautifulSoup(html, features='lxml')

    prdt_names = []
    prdt_prices = []

    productDivs = soup.find_all('div', attrs={'class': 'ti'})
    productPriceDivs = soup.find_all('span', attrs={'class': 'red'})
    for div in productDivs:
        # print(div)
        prdt_name = div.find_all('a')

        for p in prdt_name:
            # print(p.get_text())
            prdt_names.append(str(p.get_text()))

    for div in productPriceDivs:
        mystr = str(div.get_text())
        # print(div.get_text())
        if bool(mystr):
            # print(mystr.split("$")[1])
            try:
                prdt_prices.append(str("$" + mystr.split("$")[1]))
            except IndexError as e:
                prdt_prices.append(str(mystr))
                # print(mystr)
                # print(e)

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

    if len(prdt_names) == len(prdt_prices):
        for i in range(0, len(prdt_names) - 1, 1):
            items = [prdt_names[i], prdt_prices[i]]
            writetocsv(items)
            # printf("%s, %s \n", prdt_names[i], prdt_prices[i])


def printf(format, *args):
    sys.stdout.write(format % args)


def writetocsv(data):
    if bool(data):
        with open(output_csv, "a", newline='') as csv_file:
            writer = csv.writer(csv_file, delimiter=',')
            # for line in data:
            # print(line)
            writer.writerow(data)


# 精簡html tag語法
def cleanhtml(raw_html):
    say = str(raw_html)
    cleanr = re.compile('<.*?>')
    cleantext = re.sub(cleanr, '', say)
    return cleantext


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


# 進入點
if __name__ == '__main__':
    checkfile()
    getinfo()
