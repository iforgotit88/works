import numpy as np
#from google_images_download import google_images_download
#import pandas as pd
import requests as rq
import re
from bs4 import BeautifulSoup
import myString
import urllib.request
from urllib.parse import unquote, quote
import os
import time
try: 
	from googlesearch import search 
except ImportError: 
	print("No module named 'google' found") 


ScientificName = myString.getPlantSName()
Order = myString.getPlantOrder()


def webForWikipedia(plantName, myDictionary):
    url = ""
    wikiURL = "https://zh.wikipedia.org/wiki/"
    needSite = "zh.wikipedia.org"
    urlList = getNeedURL(plantName + " 植物 ", needSite)
    values = {"flower" : "花", "tree" : "樹", "bamboo" : "竹"}
    
    for theurl in urlList:
        strurl = unquote(theurl)
        if strurl[len(wikiURL) + 1] == plantName:
            print("1")
            print(theurl)
            print(strurl)
            url = theurl
            break
        if strurl.find(needSite) > -1 and strurl.find(values["flower"]) > -1:
            print("2")
            print(theurl)
            print(strurl)
            url = theurl
        elif strurl.find(needSite) > -1 and strurl.find(values["tree"]) > -1:
            print("3")
            print(theurl)
            print(strurl)
            url = theurl
        elif strurl.find(needSite) > -1 and strurl.find(values["bamboo"]) > -1:
            print("4")
            print(theurl)
            print(strurl)
            url = theurl
        elif strurl.find(needSite) > -1 and strurl.find(plantName) > -1 and not(url):
            print("5")
            print(theurl)
            print(strurl)
            url = theurl

    try:
        response = rq.get(url) # 用 requests 的 get 方法把網頁抓下來
        response.encoding = response.apparent_encoding
        html_doc = response.text # text 屬性就是 html 檔案
        soup = BeautifulSoup(html_doc, "lxml") # 指定 lxml 作為解析器
    except:
        return None

    parts = soup.find_all("td")
    part_word = []

    #從wiki抓取屬與科即可
    #returnTitles = ["Order", "Genus"]
    returnTitles = ["Order", "Genus", "Species", "name"]
    titleStrings = ["科：", "屬：", "種：", "學名"]

    newDictionary = {}
    for i in range(len(returnTitles)):
        newDictionary[returnTitles[i]] = []

    for part in parts:
        part_word.extend(part.find_all("span"))


    check = False 
    index = 0
    for part in part_word:
        part = str(part)
        #part = "".join(part.split())
        part = part.replace("\n", "")
        part = delWord(part)
        part = part.replace("  "," ")

        if part == "":
            continue
 
        if check:
            if index > 2:
                newDictionary[returnTitles[3]].append(part)
                break
            newDictionary[returnTitles[index]].extend(part.split(" "))
            check = False
            index = index + 1 
        if part.find(titleStrings[index]) > -1 or index == 3:
            check = True
    
    myDictionary[Order] = newDictionary[returnTitles[0]]
    myDictionary[Order].extend(newDictionary[returnTitles[1]])
    myDictionary[ScientificName] = newDictionary[returnTitles[3]]
    return myDictionary 


def webForPicture(plantName):
    '''
    response = google_images_download.googleimagesdownload()
    arguments = {"keywords": plantName,
                 "limit": 20,
                 "print_urls": True}
    paths = response.download(arguments)
    print("paths : ", paths)
    '''

    url = 'https://www.google.com.tw/search?q=' + plantName + ' &rlz=1C2CAFB_enTW617TW617&source=lnms&tbm=isch&sa=X&ved=0ahUKEwictOnTmYDcAhXGV7wKHX-OApwQ_AUICigB&biw=1128&bih=960'

    photolimit = 1 

    headers = {'User-Agent': 'Mozilla/5.0'}

    response = rq.get(url,headers = headers) #使用header避免訪問受到限制

    soup = BeautifulSoup(response.content, 'html.parser')

    items = soup.find_all('img')

    folder_path = myString.getPicture()

    if (os.path.exists(folder_path) == False): #判斷資料夾是否存在
        os.makedirs(folder_path) #Create folder

    exceptcount = 0
    getCount = 0
    for index , item in enumerate (items):
        if (item and getCount < photolimit ):
            try:
                html = rq.get(item.get('src')) # use 'get' to get photo link path , requests = send request
                #img_name = folder_path + str(index + 1) + '.png'
            except:
                exceptcount += 1
                continue

            img_name = folder_path + plantName + '.png'
            print("Create new picture : ", img_name)
            getCount += 1

            with open(img_name,'wb') as file: #以byte的形式將圖片數據寫入
                file.write(html.content)
                file.flush()

            file.close() #close file

            print('第 %d 張' % (getCount))

            time.sleep(1)
        if getCount > photolimit:
            break

    print("picture exceptCount : ", exceptcount)


def delWord(word, startWord = "<", endWord = ">"):
    startIndex = -1
    endIndex = -1
    
    for i in range(len(word)):
        if word[i] == startWord:
            startIndex = i
            continue
        if word[i] == endWord and startIndex > -1:
            endIndex = i
            processWord = ""
            processWord = word[:startIndex] + word[endIndex + 1:]
            word = processWord
            break
    if startIndex == -1 or endIndex == -1:
        return word
    else:
        return delWord(word, startWord, endWord)


def getInformationFromWeb(url, keywords = []):
    try:
        response = rq.get(url) # 用 requests 的 get 方法把網頁抓下來
        response.encoding = response.apparent_encoding
        html_doc = response.text # text 屬性就是 html 檔案
        #soup = BeautifulSoup(response.text, "lxml") # 指定 lxml 作為解析器
        soup = BeautifulSoup(html_doc, "lxml") # 指定 lxml 作為解析器
        #posts = soup.find("div")
    except:
        return None 

    parts = soup.find_all("div")
    part_word = []
    for part in parts:
        part_word.extend(part.find_all("p"))

    return_part_word = []
    for part in part_word:
        part = str(part)
        #part = "".join(part.split())
        part = part.replace("\n", "")
        part = delWord(part)
        part = part.replace("  "," ")
        if isinstance(keywords, list):
            for keyword in keywords:
                checkText = part.find(keyword)
                if not checkText == -1:
                    return_part_word.append(part)
                    break
        else:
            checkText = part.find(keywords)
            if not checkText == -1:
                return_part_word.append(part)
    return return_part_word


def getNeedURL(plantName, searchParam = ""):
    if searchParam:
        query = plantName + " " + searchParam
    else:
        query = plantName
    print(query)
    #searchList = search(query, tld="co.in", lang="zh-TW", stop = 10, pause=2) 
    searchList = search(query, lang="zh-TW", stop = 5, pause=2) 
    return searchList


def getNeedEngURL(plantName, searchParam = ""):
    if searchParam:
        query = plantName + " " + searchParam
    else:
        query = plantName
    print(query)
    #searchList = search(query, tld="co.in", lang="zh-TW", stop = 10, pause=2) 
    searchList = search(query, stop = 3, pause=2) 
    return searchList


if __name__ == "__main__":
    #aa = []
    #print(webForWikipedia("山茶", aa))
    webForPicture("百日草")
    #webForPicture("Zinnia")

