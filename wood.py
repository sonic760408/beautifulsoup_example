from bs4 import BeautifulSoup
from urllib.request import urlopen
import re
import sys
import csv
import os
import logging

base_url = "https://www.woodpecker.com.tw"
output_csv = "wood.csv"
sub_url = "/0/default/asc/"
logger = logging.getLogger(__name__)

# 啄木鳥
def getinfo():
    # his = ["/item/%E7%BD%91%E7%BB%9C%E7%88%AC%E8%99%AB/5162711"]
    his = []

    myurl = base_url + ""

    # 取得網址
    try:
        html = urlopen(myurl, timeout=10).read().decode('utf-8')
    except Exception as e:
        logger.error('ERR: %s, website: %s', e, myurl)
        sys.exit(1)

    soup = BeautifulSoup(html, features='lxml')
    # print("URL: ", end='')
    # print(soup.find('headNav').get_text())

    # 网络爬虫     url:

    # find valid urls
    # sub_urls = soup.find_all("a", {"target": "_top", "href": re.compile("/TinTin/EC*")})

    productDivs = soup.find_all('div', attrs={'class': 'center_area'})

    my = []

    i = 0

    re1 = '.*?'  # Non-greedy match on filler
    re2 = '(www\\.woodpecker\\.com\\.tw)'  # Fully Qualified Domain Name 1

    for div in productDivs:
        # print(div)
        uls = div.find_all('ul', attrs={'id': 'nav2'})
        for ul in uls:
            lis = ul.find_all('li')
            for li in lis:
                link = li.find('a')
                txt = link['href']

                rg = re.compile(re1 + re2, re.IGNORECASE | re.DOTALL)
                m = rg.search(txt)
                if m:
                    # print("%d: " % i, end='')
                    # print(ref['href'])
                    my.append(str(txt))
                    # i = i + 1
            i = 0

        for ref in my:
            getitems(str(ref))
            # print("%d: " % i, end='')
            # print(ref)
            # i = i + 1

        # 使用link抓資料


def getitems(url: str):
    myurl = url
    # print("url: %s" % myurl)

    # 取得網址
    try:
        html = urlopen(myurl, timeout=10).read().decode('utf-8')
    except Exception as e:
        logger.error('ERR: %s, website: %s', e, myurl)
        return

    soup = BeautifulSoup(html, features='lxml')

    pages = []

    # get all nexturl

    select = soup.find_all('div', attrs={'class': 'page_select_area'})
    for item in select:
        my = item.find('div', attrs={'class': 'left_area'})
        str1 = my.text

        start = str1.find('[共:')
        end = str1.find(' 筆]')

        if start != -1 & end != -1:
            total = str1[start+3:end]
            # print("total: %d" % int(total))
            for i in range(0, int(total), 20):
                if i != 0:
                    pages.append(str(myurl + sub_url + str(i)))
                else:
                    pages.append(str(myurl + sub_url))

        else:
            print("not found")

    for item in pages:
        # print(item)
        getpageitems(item)

    '''    
    productDivs = soup.find_all('div', attrs={'class': 'goods_pic_area2'})
    #print(productDivs)
    for div in productDivs:
        # print(div)
        prdt_name = div.find_all('img', attrs={'class': 'go1'})

        prdt_price = div.find_all('div', attrs={'class': 'goods_price_area'})
        for p in prdt_name:
            #print(p['title'])
            prdt_names.append(str(p['title']))

        for p in prdt_price:
            #print(p.get_text())
            prdt_prices.append(str(p.get_text()))

    if len(prdt_names) == len(prdt_prices):
        for i in range(0, len(prdt_names) - 1, 1):
            items = [prdt_names[i], prdt_prices[i]]
            writetocsv(items)
    '''


def getpageitems(url: str):
    
    prdt_names = []
    prdt_prices = []

    myurl = url
    # print("url: %s" % myurl)

    # 取得網址
    try:
        html = urlopen(myurl, timeout=10).read().decode('utf-8')
    except Exception as e:
        logger.error('ERR: %s, website: %s', e, myurl)
        return

    soup = BeautifulSoup(html, features='lxml')

    productDivs = soup.find_all('div', attrs={'class': 'goods_pic_area2'})
    #print(productDivs)
    for div in productDivs:
        # print(div)
        prdt_name = div.find_all('img', attrs={'class': 'go1'})

        prdt_price = div.find_all('div', attrs={'class': 'goods_price_area'})
        for p in prdt_name:
            #print(p['title'])
            prdt_names.append(str(p['title']))

        for p in prdt_price:
            #print(p.get_text())
            prdt_prices.append(str(p.get_text()))

    if len(prdt_names) == len(prdt_prices):
        for i in range(0, len(prdt_names) - 1, 1):
            items = [prdt_names[i], prdt_prices[i]]
            writetocsv(items)



def printf(format, *args):
    sys.stdout.write(format % args)


def writetocsv(data):
    if bool(data):
        with open(output_csv, "a", newline='') as csv_file:
            writer = csv.writer(csv_file, delimiter=',')
            # for line in data:
            # print(line)
            writer.writerow(data)


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


def logconfig():
    # 基礎設定
    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                        datefmt='%y-%m-%d %H:%M:%S')
    '''
    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                        datefmt='%y-%m-%d %H:%M:%S',
                        handlers=[logging.FileHandler('my.log', 'w', 'utf-8'), ])
    '''

    # 定義 handler 輸出 sys.stderr
    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    # 設定輸出格式
    formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
    # handler 設定輸出格式
    console.setFormatter(formatter)
    # 加入 hander 到 root logger
    logging.getLogger('').addHandler(console)

# exists

# 進入點
if __name__ == '__main__':
    logconfig()
    checkfile()
    getinfo()
