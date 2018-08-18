import requests
from bs4 import BeautifulSoup
import re

HTML_PARSER = "html.parser"
ROOT_URL = 'https://www.norbelbaby.com.tw/TinTin/'
LIST_URL = 'https://www.woodpecker.com.tw/product/index/%E6%B4%BB%E5%8B%95%E7%89%B9%E5%8D%80'

SPACE_RE = re.compile(r'\s+')

#取得丁丁藥品資訊
def get_item_list():
    list_req = requests.get(LIST_URL)
    if list_req.status_code == requests.codes.ok:
        soup = BeautifulSoup(list_req.content, HTML_PARSER)
        # shop_links_a_tags = soup.find_all('div', attrs={'div': '店名'})
        shop_links_a_tags = soup.find_all('div', class_="goods_title_area")
        price_tags = soup.find_all('div', class_="goods_price_area")
        shop_links = []
        price_links = []
        merge_links = []

        for i in range(0, len(shop_links_a_tags) - 1, 1):
            mystr = str(cleanhtml(shop_links_a_tags[i])) + ", " \
                    + str(cleanhtml(price_tags[i]))
            merge_links.append(mystr)
            print(mystr)

        '''
        for link in shop_links_a_tags:
            #print(link)
            if link is not None:
                mylink = cleanhtml(link)
            else:
                mylink = ''
            shop_links.append(link)
            # strip_tags(link)
            if mylink is not None:
                print(mylink)
            else:
                print("NONE")

        for price in price_tags:
            if price is not None:
                myprice = cleanhtml(price)
            else:
                myprice = ''
                price_links.append(price)
            # strip_tags(link)
            if myprice is not None:
                print(myprice)
            else:
                print("NONE")
        '''
    else:
        print("ERROR")

# 精簡html tag語法
def cleanhtml(raw_html):
    say = str(raw_html)
    cleanr = re.compile('<.*?>')
    cleantext = re.sub(cleanr, '', say)
    return cleantext

# 進入點
if __name__ == '__main__':
    get_item_list()
