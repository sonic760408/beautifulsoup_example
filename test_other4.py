# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals

import urllib.request
import time
from datetime import datetime
from bs4 import BeautifulSoup

TXF_NAME = '電子期'
TE_NAME = '臺指期'
TF_NAME = '金融期'
TA_NAME = '臺指50期'

targets = set()
targets.add(TXF_NAME)
targets.add(TE_NAME)
targets.add(TF_NAME)
targets.add(TA_NAME)

quotes = dict()

url = 'http://info512.taifex.com.tw/Future/FusaQuote_Norl.aspx'


class Quote(object):

    def __init__(self):
        self.name = None
        self.trade_time = None
        self.trade_price = None
        self.change = None
        self.open = None
        self.high = None
        self.low = None

    def __str__(self):
        res = list()

        res.append(self.name)
        res.append(self.trade_time.strftime("%H:%M:%S"))
        res.append(self.trade_price)
        res.append(self.change)
        res.append(self.open)
        res.append(self.high)
        res.append(self.low)
        return str(res)

while True:

    #  應該要限制在有交易的時間內執行 ， 但為了示範起見 ， 使用無窮迴圈 。

    html_data = urllib.request.urlopen(url).read()
    soup = BeautifulSoup(html_data, 'html.parser')

    rows = soup.find_all('tr', {"class": "custDataGridRow", "bgcolor": "White"})

    for row in rows:
        # print(row)

        items = row.find_all('td')

        name = items[0].a.text.strip()
        #print(name)
        # if name any in targets:
        if any(s in name for s in targets):

            quote = Quote()
            quote.name = name
            if items[6] is not None:
                if items[6] != '--':
                    try:
                        float(items[6].font.text.replace(',', ''))
                    except ValueError:
                        quote.trade_price = "--"
                    else:
                        quote.trade_price = float(items[6].font.text.replace(',', ''))
                else:
                    quote.trade_price = "--"
            else:
                quote.trade_price = "--"

            if items[7] is not None:
                if items[7] != '--':
                    try:
                        float(items[7].font.text.replace(',', ''))
                    except ValueError:
                        quote.change = "--"
                    else:
                        quote.change = float(items[7].font.text.replace(',', ''))
                else:
                    quote.change = "--"
            else:
                quote.change = "--"

            if items[10] is not None:
                if items[10] != '--':
                    try:
                        quote.open = float(items[10].font.text.replace(',', ''))
                    except ValueError:
                        quote.open = "--"
                    else:
                        quote.open = float(items[10].font.text.replace(',', ''))
                else:
                    quote.open = "--"
            else:
                quote.open = "--"

            if items[11] is not None:
                if items[10] != '--':
                    try:
                        quote.high = float(items[11].font.text.replace(',', ''))
                    except ValueError:
                        quote.high = "--"
                    else:
                        quote.high = float(items[10].font.text.replace(',', ''))
            else:
                quote.high = "--"

            if items[12] is not None:
                if items[12] != '--':
                    try:
                        quote.low = float(items[12].font.text.replace(',', ''))
                    except ValueError:
                        quote.low = "--"
                    else:
                        quote.low = float(items[12].font.text.replace(',', ''))
            else:
                quote.low = "--"

            if items[14] is not None:

                try:
                    quote.trade_time = datetime.strptime(items[14].font.text, "%H:%M:%S")
                except ValueError:
                    quote.trade_time = datetime.strptime("00:00:00", "%H:%M:%S")
                else:
                    quote.trade_time = datetime.strptime(items[14].font.text, "%H:%M:%S")
            else:
                quote.trade_time = datetime.strptime("00:00:00", "%H:%M:%S")

            #print(quote.trade_time)
            '''
                quote.open = float(items[10].font.text.replace(',', ''))
                quote.high = float(items[11].font.text.replace(',', ''))
                quote.low = float(items[12].font.text.replace(',', ''))
                
            quote.trade_price = float(items[6].font.text.replace(',', ''))
            quote.change = float(items[7].font.text)
            quote.trade_time = datetime.strptime(items[14].font.text, "%H:%M:%S")
            quote.open = float(items[10].font.text.replace(',', ''))
            quote.high = float(items[11].font.text.replace(',', ''))
            quote.low = float(items[12].font.text.replace(',', ''))
            
            '''
            quotes[name] = quote
            print(quote)

    #  根據取得的報價判斷條件 ， 條件自訂 。

    #  條件符合時通知使用者 ， 如何通知 ？

    time.sleep(5)
