# 11 news categories
news_links =['aipl', 'ait', 'aspt', 'asc', 'aie', 'amov','ahel','aopl','asoc','acul','acn']
news_categories=['政治','科技','運動','證卷','產經','娛樂','生活','國際','社會','文化','兩岸']
base_url = 'https://www.cna.com.tw/list/'


#import
import requests
import re
from bs4 import BeautifulSoup
import time
import pandas as pd
from datetime import datetime, timedelta


def crawlNews():
    links = []
    titles = []
    dates = []
    contents = []
    categories = []
    item_id = []
    photo_links = []

    for i, url_short_name in enumerate(news_links):  #針對每一類 共有11類

        full_url = base_url + url_short_name + '.aspx'
        print(full_url)
        req = requests.get(full_url)
        page = BeautifulSoup(req.text, 'lxml')

        # 抓新聞列表
        items = page.find('ul', {'id': re.compile("jsMainList\w*")}).findAll('li')

        serial_no = 1
        for j, item in enumerate(items):  #針對每一篇項目 抓其細節
            title = item.find('h2').text  #抓標題
            print(title)
            link = item.find('a').get('href')  #抓連結
            #print(link)
            dt = item.find('div', {'class': "date"}).text  #抓日期時間
            #print(dt)
            titles.append(title)
            links.append(link)
            categories.append(news_categories[i])  #類別名稱紀錄起來

            # 抓時間 當中有夾帶廣告 沒有時間欄位，可以判斷之並將之跳離這一筆!
            # 排除穿插廣告
            try:
                dt = item.find('div', {'class': "date"}).text  #抓日期時間
                # 排除穿插廣告
                news_time = datetime.strptime(dt, '%Y/%m/%d %H:%M')
            except:
                print('skip this item:', dt)
                print(link)
                continue

            dates.append(news_time.date())

            # item id
            t = datetime.strptime(dt, '%Y/%m/%d %H:%M')
            tstr = t.strftime("%Y%m%d")

            item_id.append(news_links[i] + "_" + tstr + "_" + str(serial_no))
            serial_no += 1

            try:
                if item.find('img').has_attr('data-src'):
                    photo_link = item.find('img').get('data-src')
                else:
                    photo_link = item.find('img').get('src')
                #print(photo_link)
            except:
                photo_link = ''

            photo_links.append(photo_link)

            # There are some words we don't like to analyze, They should be removed.
            page = BeautifulSoup(requests.get( link ).text,'lxml')
            cont = page.find('div',{'class':"paragraph"}).text
            cont = re.sub('（中央社記者\w*）','', cont) # 去除不要的文字
            cont = re.sub('（編輯：.*','', cont) 
            cont = re.sub('（譯者：.*','', cont) 
            cont = re.sub('（中央社\w*）','', cont) 
        
            contents.append(cont)
            time.sleep(2)  # 遵守爬蟲禮節，請小睡一下
    data = zip(item_id, dates, categories, titles, contents, links, photo_links)
    return data

def saveData(data):
    df = pd.DataFrame(list(data), columns=['item_id','date','category','title','content','link','photo_link'])
    df.to_csv("cna_news_200.csv", sep="|", index=False)

if __name__ == '__main__':
    data = crawlNews()
    saveData(data)
