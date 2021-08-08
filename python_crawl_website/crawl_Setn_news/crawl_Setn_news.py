news_links =['6', '7', '34', '2','4','5','41']
news_categories=['政治','科技','運動','產經','生活','國際','社會']

news_links =['6', '41']
news_categories=['政治','社會'] # ,'證卷','娛樂','文化','兩岸'

base_url = "https://www.setn.com"
middle_url = "ViewAll.aspx?PageGroupID="


import requests
import re
from bs4 import BeautifulSoup
import time
import pandas as pd
from datetime import datetime, timedelta
from selenium import webdriver 

def get_news_target_date( target_date ):   
    print("Target date:", target_date)

    links=[]
    titles=[]
    dates=[]
    contents=[]
    categories=[]
    item_id=[]
    photo_links=[]

    for i, url_short_name in enumerate( news_links ):        
        full_url = base_url + "/"  + middle_url + url_short_name
        #print("get pages from url:", full_url)

        # print("get pages from url:", full_url)
        print(full_url)
        
        req = requests.get(full_url)
        page = BeautifulSoup(req.text, 'lxml')  
        

        items = page.findAll('div',{'class':"col-sm-12 newsItems"})
        print("run Crawl")

        serial_no = 1
        #for item in items:
        for j, item in enumerate(items):  #針對每一篇項目 抓其細節
            # print(item)   
        
            # 排除穿插廣告 
            try:                           
                date = item.find('time').text
                news_time = datetime.strptime(date, '%m/%d %H:%M')   
                news_time = news_time.replace(year = datetime.today().year)
                
                if news_time > datetime.today():
                    news_time = news_time.replace(year = datetime.today().year -1)
                
                # 排除穿插廣告 

            except:
                #print('date error: skip this news:',item)
                print('date error: skip this news')
                continue
        
            # 排除日期不是今天
            '''if target_date != news_time.date():
                #print(news_time.date())
                continue'''
        
            try:
                # title
                title = item.find('a', {'class': "gt"}).text            
                #\u3000
                title = re.sub('\u3000', " ", title)
                print(title)
                
                # news link
                # item.find('div',{"class":"col"}).find('a').get('href')

                # news link
                link = item.find('a', {'class': "gt"}).get('href')
                link =  base_url + link

                '''
                # photo link
                try:
                    photo_link = item.find('img').get('src')
                except:
                    photo_link = ''
                # print("photo link:", photo_link)  
                '''
                photo_link = ''
                

                # item id
                tstr = news_time.strftime("%Y%m%d")

                # print("crawl content:")
                # There are some words we don't like to analyze, They should be removed.
                page = BeautifulSoup(requests.get( link).text,'lxml')
                
                content_page = page.find('div',{'id':"Content1"})
                
                '''
                for element in content_page.findAll('div', class_="article-hash-tag"):
                    element.decompose()     CNA處理方式(不適用) '''
                
                cont = content_page.text
                cont = re.sub('記者\w*／\w*報導','', cont)
                cont = re.sub('▲\w*','', cont) 
                cont = re.sub('（\w*／\w*）','', cont) 
                cont = re.sub('\n','', cont) 
                
            except:
                print("error on crawling news content:", link)
                continue  


            titles.append(title)
            links.append(link)
            dates.append(news_time.date())
            categories.append(news_categories[i])  #類別名稱紀錄起來
            photo_links.append(photo_link)
            contents.append(cont)

            item_id.append(news_links[i] + "_" + tstr + "_" + str(serial_no))
            serial_no += 1

            time.sleep(2)  # 遵守爬蟲禮節，請小睡一下
            
        print("處理完畢類別:",news_categories[i], ",total items:", serial_no) 
    
    # zip data
    data = zip(item_id, titles,categories,contents,links,dates, photo_links)
    df = pd.DataFrame(list(data), columns=['item_id','title','category','content','link','date','photo_link'])
    print(target_date,"爬取新聞數:",df.shape[0])
    
    return df

def saveData(data):
    data.to_csv("setn_news.csv", sep="|", index=False)

if __name__ == "__main__":
    today = datetime.today()
    data = get_news_target_date(today)
    saveData(data)
