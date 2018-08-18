import requests
from bs4 import BeautifulSoup
import time
urls = ['http://python.org',
        'http://python.org',
        'http://python.org',
        'http://python.org',
        'http://python.org']
startTime = time.time()
for url in urls:
    re = requests.get(url)
    soup = BeautifulSoup(re.text, 'lxml')
    As = soup.find_all('a')
    for a in As:
        try:
            print(a)
        except:
            print("----------------------------------Error------------------------------------")
finishTime = time.time()
print(finishTime - startTime)
