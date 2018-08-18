from bs4 import BeautifulSoup
from urllib.request import urlopen
import re
import random

base_url = "https://baike.baidu.com"
his = ["/item/%E7%BD%91%E7%BB%9C%E7%88%AC%E8%99%AB/5162711"]

url = base_url + his[-1]

# 取得網址
html = urlopen(url).read().decode('utf-8')
soup = BeautifulSoup(html, features='lxml')
print("URL: ", end='')
print(soup.find('h1').get_text(), '    url: ', his[-1])

# 网络爬虫     url:  /item/%E7%BD%91%E7%BB%9C%E7%88%AC%E8%99%AB/5162711

# find valid urls
sub_urls = soup.find_all("a", {"target": "_blank", "href": re.compile("/item/(%.{2})+$")})

if len(sub_urls) != 0:
    his.append(random.sample(sub_urls, 1)[0]['href'])
else:
    # no valid sub link found
    his.pop()

print("SUBLINK: ", end='') # no newline
print(his)

# ['/item/%E7%BD%91%E7%BB%9C%E7%88%AC%E8%99%AB/5162711', '/item/%E4%B8%8B%E8%BD%BD%E8%80%85']

his = ["/item/%E7%BD%91%E7%BB%9C%E7%88%AC%E8%99%AB/5162711"]

for i in range(20):
    url = base_url + his[-1]

    html = urlopen(url).read().decode('utf-8')
    soup = BeautifulSoup(html, features='lxml')
    print(i, soup.find('h1').get_text(), '    url: ', his[-1])

    # find valid urls
    sub_urls = soup.find_all("a", {"target": "_blank", "href": re.compile("/item/(%.{2})+$")})

    if len(sub_urls) != 0:
        his.append(random.sample(sub_urls, 1)[0]['href'])
    else:
        # no valid sub link found
        his.pop()

