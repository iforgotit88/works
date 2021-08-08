# Get some news categories
news_links =['politic', 'technologynews','sports', 'money', 'star', 'life', 'world', 'society', 'chinese']
news_categories=['政治','科技','運動','產經','娛樂','生活','國際','社會','兩岸']

#test
news_links =['politic', 'technologynews']
news_categories=['政治','科技']

base_url = 'https://www.chinatimes.com'
end_url = '/total?chdtv'


import requests
import re
from bs4 import BeautifulSoup
import time
import pandas as pd
from datetime import datetime, timedelta
from selenium import webdriver 

def get_news_target_date( target_date ):
    
    # 驅動程式置放於中文路徑可能會報錯
    #chrome_path = "../chromedriver89.exe"
    chrome_path = "../chromedriver92.exe"
    
    # Chrome顯示出來
    driver = webdriver.Chrome(chrome_path)
    
    global end_url
    
    print("Target date:", target_date)

    links=[]
    titles=[]
    dates=[]
    contents=[]
    categories=[]
    item_id=[]
    photo_links=[]

    for i, url_short_name in enumerate( news_links ):        
        full_url = base_url + "/" + url_short_name + end_url
        #print("get pages from url:", full_url)

        # print("get pages from url:", full_url)

        driver.get(full_url)
        time.sleep(2)

        page_number = 0
        while True:
            try:
                print("browse頁次:", page_number+1)

                #driver.find_element_by_id("SiteContent_uiViewMoreBtn").click()
                end_url = f'/total?page={page_number + 2}&chdtv'
                
                full_url = base_url + "/" + url_short_name + end_url
                
                print(full_url)
                
                driver.get(full_url)
                
                page_number += 1
                time.sleep(2)
                # 今天新聞應該只會出現在前三頁 若要爬取最近幾天其中的某一天則需要全部翻頁
                if (page_number>2):
                    break
            except:
                break
        print("total pages:",page_number)

        page = BeautifulSoup(driver.page_source,'html.parser')     
        

        # items = page.find('ul',{'id':"myMainList"}).findAll('li') #兩岸新聞改版成myMainList_Style2
        # 20200527 又改版
        items = page.find('section',{"class":"article-list"}).findAll('li')
        print("run Crawl")

        serial_no = 1
        #for item in items:
        for j, item in enumerate(items):  #針對每一篇項目 抓其細節
            # print(item)
        
        
        
            # 排除穿插廣告 
            try:
                # date
                date = item.find('div',{"class":"col"}).find('time').get('datetime')
                news_time = datetime.strptime(date, '%Y-%m-%d %H:%M')              
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
                title = item.find('div',{"class":"col"}).find('a').text
                print(title)

                # news link
                # item.find('div',{"class":"col"}).find('a').get('href')

                # news link
                link = item.find('a').get('href')
                link = base_url + link
                #print(link)

                # photo link
                try:
                    photo_link = item.find('img').get('src')
                except:
                    photo_link = ''
                # print("photo link:", photo_link)  


                # item id
                tstr = news_time.strftime("%Y%m%d")

                # print("crawl content:")
                # There are some words we don't like to analyze, They should be removed.
                page = BeautifulSoup(requests.get( link ).text,'lxml')
                content_page = page.find('div',{'class':"article-body"})
                for element in content_page.findAll('div', class_="promote-word"):
                    element.decompose()

                for element in content_page.findAll('div', class_="article-hash-tag"):
                    element.decompose()

                cont = content_page.text
                cont = re.sub('\n', "", cont)
                cont = re.sub('\(中時新聞網\)', "", cont)
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
            
        print("處理完畢類別:",news_categories[i],",total pages:" ,page_number, ",total items:", serial_no) 
    
    # zip data
    data = zip(item_id, titles,categories,contents,links,dates, photo_links)
    df = pd.DataFrame(list(data), columns=['item_id','title','category','content','link','date','photo_link'])
    print(target_date,"爬取新聞數:",df.shape[0])
    
    return df

def saveData(data):
    data.to_csv("china_news.csv", sep="|", index=False)


if __name__ == "__main__":
    today = datetime.today()
    data = get_news_target_date(today)
    saveData(data)


