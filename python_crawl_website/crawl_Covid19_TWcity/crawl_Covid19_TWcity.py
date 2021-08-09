area = ["北部","中南部","東部離島"]
city = [["新北市","台北市","桃園市","苗栗縣","基隆市","新竹縣","新竹市"], 
        ["彰化縣","台中市","南投縣","高雄市","台南市","屏東縣","雲林縣","嘉義縣","嘉義市"],
        ["宜蘭縣","花蓮縣","台東縣","澎湖縣","連江縣"]]
news_links = [
    "https://covid-19.nchc.org.tw/"
]

import requests
from bs4 import BeautifulSoup
import re

import pandas as pd
import numpy

def saveCityAndArea():
    df_dict = {}
    df_dict["area"] = area
    df_dict["city"] = city

    df = pd.DataFrame(zip(df_dict["area"],df_dict["city"]), columns=['area', 'city'])
    df.to_csv('city_Area.csv', sep='|', index=None)



def crawlNews():
    r = requests.get( news_links[0] , verify=False)
    page = BeautifulSoup(r.text, 'lxml')

    results = page.findAll('a',{'class':"btn btn-success btn-lg"})
    city_confirmeds = []
    for item in results:
        city = [item.text.split(" ")[0]]
        city_confirmed = item.text.split(" ")[1]
        city_confirmed = city_confirmed.split("+")
        if len(city_confirmed) == 1:
            # 表示沒值
            city_confirmed[0] = "".join(city_confirmed[0].split())
            city_confirmed.extend("0")
        elif len(city_confirmed) == 2:
            city_confirmed[1] = "".join(city_confirmed[1].split())
        city.extend(city_confirmed)
        
        city_confirmeds.append(city)

    #劃分區域
    df = pd.read_csv('city_Area.csv', sep='|')
    df_dict={}
    for idx, row in df.iterrows():
        df_dict[row['area']]= eval(row['city'])

    addCovid19 = {}
    list_area = list(df["area"])

    #整理資料
    df_dict = {}
    df_data = df.copy()

    for idx, row in df_data.iterrows():
        df_dict[row['area']]= eval(row['city'])
        addCovid19[row['area']] = []
    #print(df_dict)
    #print(list_area)
    #print(addCovid19)
            
    for city in city_confirmeds:  
        for area in list_area:
            if city[0] in  df_dict[area]:
                addCovid19[area].append(city)
    #完成 {"北部":[["新北"...]]}
    df_addconv = pd.DataFrame(list(addCovid19.items()), columns=['area', 'addConvid'])
    return df_addconv

def saveData(df):
    df.to_csv('covid19_TWcity_Area.csv', sep='|', index=None)


if __name__ == "__main__":
    saveCityAndArea()
    df = crawlNews()
    saveData(df)
