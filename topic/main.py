import numpy as np
import json
import pandas as pd
import requests as rq
import re
import os
import myString
from pathlib import Path
import scrap
import plantDB as myDB
from bs4 import BeautifulSoup


temperatureTitle = myString.getTemperatureName()
moistureTitle = myString.getMoistureName()
phTitle = myString.getPhName()
sunlightTitle =  myString.getSunlightName()
pictureTitle = myString.getPicture()

ID = "ID"
ChineseName = myString.getPlantCName()
EnglishName = myString.getPlantEName()
ScientificName = myString.getPlantSName()
Order = myString.getPlantOrder()
#OtherName = myString.getPlantOName()

temperature = myString.getTemperatureName()
moisture = myString.getMoistureName()
pH = myString.getPhName()
sunlight = myString.getSunlightName()
picture = myString.getPictureName()

def findWord(text_list = [], find_word = [], except_word = [], period = 20, priority_word = [], sameWord = [], replaceTo = ""):
    answerList = []
    #print("findWord function : ", text_list)
    for text in text_list: # 找剛截下來的字串陣列
        text = str(text)
        formatReplace = ["~", "～", "到", "至", " to "]
        for needReplace in formatReplace:
            text = text.replace(needReplace, "-")

        #統一格式，如：氣溫、適溫、溫度.... 全部改成溫度
        if sameWord:
            for theWord in sameWord:
                text = text.replace(theWord, replaceTo)

        for word in find_word:   # 關鍵字陣列
            while True:
                checkAnswer = text.find(word)
                if checkAnswer > -1:  # 不是-1表示有找到
                    #print("except_word : ", except_word)
                    textStart, textEnd = wordStartToEnd(locate = checkAnswer, textLen = len(text), period = period)
                    # 選取要截取的段落
                    newText = text[textStart:textEnd]
                    for exceptWord in except_word: # 表示有不想截取的內容
                        checkAnswerAgain = newText.find(exceptWord)
                        if checkAnswerAgain > -1: #有找到不想截取的內容
                            newText = ""
                            break
                    #print("newText : ", newText)
                    #print(text[textStart:textEnd])
                    if newText:
                        answerList.append(newText)
                        p_min = int(len(newText) / 2) - 4
                        p_max = int(len(newText) / 2) + 4
                        #print("min : ", p_min, "max : ", p_max)
                        #print("except word of newText : ", newText[p_min : p_max])
                        except_word.append(newText[p_min : p_max]) # 除去重覆的字串
                    text = text[textEnd:]
                    #print("text : ", text)
                else:
                    break

    print("answerList : ", answerList)
    for p in priority_word:
        check = False
        for index, answer in enumerate(answerList):
            if answer.find(p) > -1:
                print("find it ! ", p)
                temp = answerList[0]
                answerList[0] = answer
                answerList[index] = temp
                check = True
                break
        if check:
            break

    print("find word answerList : ", answerList)
    return answerList


def wordStartToEnd(locate = 0, textLen = 0, period = 20):
    textStart = locate - period
    if textStart < 0: 
        textStart = 0
    textEnd = locate + period 
    if textEnd > textLen:
        textEnd = textLen
    return textStart, textEnd


def formatOutput(needFormatWord, removeWords = [], startWord = "", endWord = ""):
    for removeWord in removeWords: #清空文字以統一
        needFormatWord = needFormatWord.replace(removeWord, "")
    needFormatWord = startWord + needFormatWord + endWord
    return needFormatWord


def changeToCelsius(result):
    formatString = r'\d{1,2}'
    keyword = re.compile(formatString)
    strList = keyword.findall(result)
    f1 = int(strList[0])
    f1 = int((f1 - 32) * 5 / 9)
    f2 = int(strList[1])
    f2 = int((f2 - 32) * 5 / 9)
    result = str(f1) + "-" + str(f2)
    return result


def findTemperatureWord(text_list):
    result = ""
    formatString = [r'\d{1,2}-\d{1,2}°C', r'\d{1,2}-\d{1,2}℃', r'攝氏\d{1,2}-\d{1,2}', r'\d{1,2}°C-\d{1,2}°C', r'\d{1,2}℃-\d{1,2}℃',
    r'\d{1,2}-\d{1,2}°F', r'\d{1,2}-\d{1,2}℉', r'\d{1,2}°C-\d{1,2}°F', r'\d{1,2}℃-\d{1,2}℉'] #溫度的格式
    formatRemoveWord = ["攝氏", "℃", "°C", "華氏", "°F", "℉"]
    fahrenheitString = ["華氏", "°F", "℉"]

    #找出特定的格式(XX-XX°C) or (XX-XX°F)
    for text in text_list: # 找剛截下來的字串陣列
        text = str(text)
        for formatWord in formatString:
            keywords = re.compile(formatWord)
            findanswer = keywords.findall(text)
            if findanswer:
                result = findanswer[0]

                for fahrenheit in fahrenheitString:
                    if result.find(fahrenheit) > -1:
                        result = changeToCelsius(result)
                        break

                #統一格式
                result = formatOutput(result, removeWords=formatRemoveWord)
            if result:
                print("Temperature result = ", result)
                return result
    return result 


def findphWord(text_list):
    result = ""
    formatString = [r'\d{1,2}\.\d{1}-\d{1,2}\.\d{1}'] #濕度的格式
    #formatRemoveWord = ["%", " "]

    #找出特定的格式(X.X-X.X)
    for text in text_list: # 找剛截下來的字串陣列
        text = str(text)
        for formatWord in formatString:
            keywords = re.compile(formatWord)
            findanswer = keywords.findall(text)
            if findanswer:
                result = findanswer[0]
                #統一格式
                result = formatOutput(result)#, removeWords=formatRemoveWord)
            if result:
                print("pH Value result = ", result)
                return result

    #表示百分比分類沒找到
    formatString = [[ "strongly acidic", "strongly-acidic"], ["acidic"], ["neutral"], ["alkaline"]] #濕度的種類
    typeTitle = ["<5.5", "5.5-6.5", "6.5-7.5", ">7.5"]
    for text in text_list:
        text = str(text)
        for index, phType in enumerate(formatString):
            for typeString in phType:
                if text.find(typeString) > -1 and text.find("soil") > -1:
                    result = typeTitle[index]
                    print("pH Value result = ", result)
                    return result
    return result 


def findMoistureWord(text_list):
    result = ""
    formatString = [r'\d{1,2}%.{1,5}\d{1,2}%', r'\d{1,2}.{1,5}\d{1,2}%'] #濕度的格式
    formatRemoveWord = ["%", " "]

    #找出特定的格式(XX%-XX%)
    for text in text_list: # 找剛截下來的字串陣列
        text = str(text)
        for formatWord in formatString:
            keywords = re.compile(formatWord)
            findanswer = keywords.findall(text)
            if findanswer:
                result = findanswer[0]
                #統一格式
                result = formatOutput(result, removeWords=formatRemoveWord)
            if result:
                print("moisture result = ", result)
                return result

    #表示百分比分類沒找到
    formatString = [["extremely-dry", "extremely dry"],[ "dry-drained", "well-drained", "dry drained", "well drained"], ["moist"], ["wet"]] #濕度的種類
    typeTitle = ["1-20", "21-40", "41-60", "61-80"]
    for text in text_list:
        text = str(text)
        for index, moistureType in enumerate(formatString):
            for typeString in moistureType:
                if text.find(typeString) > -1 and text.find("soil") > -1:
                    result = typeTitle[index]
                    print("moisture result = ", result)
                    return result
    return result 


def findSunlightWord(text_list, find_word, countList):
    # test
    for text in text_list: # 找剛截下來的字串陣列
        text = str(text)
        for index, word in enumerate(find_word):   # 關鍵字陣列
            if text.find(word) > -1:
                countList[index] += 1
    return countList


def findTheKeyWord(plantName, search_Param, theKeyType, find_word = [], except_word = [], period = 60, priority_word = [], sameWord = [], replaceTo = ""):
    countList = []
    for i in range(len(find_word)):
        countList.append(0)
    part_word = []
    getInformation = ""
    stringResult = ""
    
    if isinstance(plantName, list):
        for thename in plantName:
            urlList = scrap.getNeedEngURL(thename, search_Param)
        
            for theURL in urlList:
                #檢查網站內是否有要查找的關鍵字
                part_word = scrap.getInformationFromWeb(theURL, find_word)
                if part_word:
                    #查關鍵字
                    text_list = findWord(text_list = part_word, find_word = find_word, period = period, priority_word = priority_word, sameWord = sameWord, replaceTo = replaceTo)
                    if theKeyType == sunlightTitle:
                        #查哪個字出現最多次
                        countList = findSunlightWord(text_list = text_list, find_word = find_word, countList = countList)
                    elif theKeyType == moistureTitle:
                        stringResult = findMoistureWord(text_list = text_list)
                        if stringResult.replace(" ","") == "":
                            stringResult = ""
                        if stringResult:
                            break 
                    elif theKeyType == phTitle:
                        stringResult = findphWord(text_list = text_list)
                        if stringResult.replace(" ","") == "":
                            stringResult = ""
                        if stringResult:
                            break 
                    elif theKeyType == temperatureTitle:
                        stringResult = findTemperatureWord(text_list = text_list)
                        if stringResult.replace(" ","") == "":
                            stringResult = ""
                        if stringResult:
                            break 
    else:
        urlList = scrap.getNeedURL(plantName, search_Param)
    
        for theURL in urlList:
            #檢查網站內是否有要查找的關鍵字
            part_word = scrap.getInformationFromWeb(theURL, find_word)


            if part_word:
                #查關鍵字
                text_list = findWord(text_list = part_word, find_word = find_word, period = period, priority_word = priority_word, sameWord = sameWord, replaceTo = replaceTo)
                if theKeyType == sunlightTitle:
                    #查哪個字出現最多次
                    countList = findSunlightWord(text_list = text_list, find_word = find_word, countList = countList)
                elif theKeyType == moistureTitle:
                    stringResult = findMoistureWord(text_list = text_list)
                    if stringResult.replace(" ","") == "":
                        stringResult = ""
                    if stringResult:
                        break
                elif theKeyType == phTitle:
                    stringResult = findphWord(text_list = text_list)
                    if stringResult.replace(" ","") == "":
                        stringResult = ""
                    if stringResult:
                        break 
                elif theKeyType == temperatureTitle:
                    stringResult = findTemperatureWord(text_list = text_list)
                    if stringResult.replace(" ","") == "":
                        stringResult = ""
                    if stringResult:
                        break 

    if theKeyType == sunlightTitle:
        if max(countList) > 0:
            maxIndex = countList.index(max(countList))
            return find_word[maxIndex]
        else:
            return ""
    elif theKeyType == moistureTitle:
        print("(Moisture) stringResult : ", stringResult)
        return stringResult
    elif theKeyType == phTitle:
        print("(pH Value) stringResult : ", stringResult)
        return stringResult
    elif theKeyType == temperatureTitle:
        print("(Temperature) stringResult : ", stringResult)
        return stringResult


def getPlantName(plantName):
    titleStrings = myString.getTitleStrings()
    titleDictionary = [ChineseName, EnglishName, ScientificName, Order]
    myDictionary = {ID : 0,
                    ChineseName : "",
                    EnglishName : [''],
                    ScientificName : [''],
                    Order : ['']}
    myDictionary = myDB.getPlantName(plantName)
    
    #表示資料庫沒有資料
    if not myDictionary[ScientificName][0]:
        if myDictionary[ChineseName]:
            myDictionary = scrap.webForWikipedia(plantName, myDictionary)
            print("plantName function dictionary : ", myDictionary)
            
            if len(myDictionary[Order]) > 0:
                myDB.updatePlantName(myDictionary, myDictionary[ID])
            else:
                print("Scientific Name not found!")
        else:
            '''
            urllist = getNeedURL(plantName, "植物") 
            if len(getInformationFromWeb[urllist[0], ["植物", "花", "草", "樹", "茶"]) > 0:
                from googletrans import Translator
                translator = Translator()
                myDictionary[ChineseName] = plantName
                myDictionary[EnglishName] = translator.translate(plantName, dest = "en")
                myDictionary = scrap.webForWikipedia(plantName, myDictionary)
                myDB.updatePlantName(myDictionary, myDictionary[ID])
            '''
            print("目前無所查植物")

            return None
    return myDictionary


def getTemperatureInformation(plantDictionary):
    returnList = {temperatureTitle : ""}

    searchTextForChinese = ["溫度", "°C", "℃", "攝氏"]
    searchTextForEnglish = ["temperature", "Temperature"]
    temperatureTextofPriority = ["最適生長溫度", "最適溫度", "生長溫度","合適溫度", "適宜溫度", "合適的溫度", "適宜的"]
    sameWord = ["適溫", "氣溫"]
    temperatureTextofEnglishPriority = ["prefer"]

    #截資訊
    result = findTheKeyWord(plantDictionary[ChineseName], "適溫", theKeyType = temperatureTitle, find_word = searchTextForChinese, period = 15, priority_word = temperatureTextofPriority, sameWord = sameWord, replaceTo = "溫度")
    if not result:
        result = findTheKeyWord(plantDictionary[ScientificName], "temperature requirements", theKeyType = temperatureTitle, find_word = searchTextForEnglish, period = 50, priority_word = temperatureTextofEnglishPriority)

    if not result:
        result = findTheKeyWord(plantDictionary[EnglishName], "temperature requirements", theKeyType = temperatureTitle, find_word = searchTextForEnglish, period = 50, priority_word = temperatureTextofEnglishPriority)

    if result:
        returnList[temperatureTitle] = result
        myDB.setTable(plantDictionary[ID], temperature, result)

    if not returnList[temperatureTitle]:
        print("temperature Not Found!")
    return returnList[temperatureTitle]


def getPhInformation(plantDictionary): 
    returnList = {phTitle : ""}
    #ph值
    searchTextForChinese = ["ph", "pH"]
    searchTextForEnglish = ["ph", "pH"]

    #截資訊
    result = findTheKeyWord(plantDictionary[EnglishName], "pH requirements", theKeyType = phTitle, find_word = searchTextForEnglish, period = 80)
    if not result:
        result = findTheKeyWord(plantDictionary[ScientificName], "pH requirements", theKeyType = phTitle, find_word = searchTextForEnglish, period = 80)

    if not result:
        result = findTheKeyWord(plantDictionary[ChineseName], "pH值", theKeyType = phTitle, find_word = searchTextForChinese, period = 30)

    if result:
        returnList[phTitle] = result
        myDB.setTable(plantDictionary[ID], pH, result)

    if not returnList[phTitle]:
        print("pH Value Not Found!")
    return returnList[phTitle]


def getMoistureInformation(plantDictionary):
    returnList = {moistureTitle : ""}
    #Moisture
    searchTextForChinese = ["濕度"]
    searchTextForEnglish = ["moisture", "Moisture", "extremely-dry", "extremely dry", "dry-drained", "well-drained", "dry drained", "well drained", "moist", "wet"]

    #截資訊
    result = findTheKeyWord(plantDictionary[EnglishName], "moisture requirements", theKeyType = moistureTitle, find_word = searchTextForEnglish, period = 80)
    if not result:
        result = findTheKeyWord(plantDictionary[ScientificName], "moisture requirements", theKeyType = moistureTitle, find_word = searchTextForEnglish, period = 80)

    if not result:
        result = findTheKeyWord(plantDictionary[ChineseName], "濕度", theKeyType = moistureTitle, find_word = searchTextForChinese, period = 30)

    if result:
        returnList[moistureTitle] = result
        myDB.setTable(plantDictionary[ID], moisture, result)

    if not returnList[moistureTitle]:
        print("Moisture Not Found!")
    return returnList[moistureTitle]


def getSunlightInformation(plantDictionary):
    returnList = {sunlightTitle : ""}

    searchTextForChinese = ["全日照", "半日照", "陰蔽"] #"半陰", "陰蔽"]
    searchTextForEnglish = ["full sun", "partial shade", "full shade"]

    result = findTheKeyWord(plantDictionary[ScientificName], "sun requirements", theKeyType = sunlightTitle, find_word = searchTextForEnglish, period = 80)

    if not result:
        result = findTheKeyWord(plantDictionary[EnglishName], "sun requirements", theKeyType = sunlightTitle, find_word = searchTextForEnglish, period = 80)

    if not result:
        result = findTheKeyWord(plantDictionary[ChineseName], "日照", theKeyType = sunlightTitle, find_word = searchTextForChinese, period = 50)
        if result:
            result = searchTextForEnglish[searchTextForChinese.index(result)]

    if result:
        returnList[sunlightTitle] = result
        myDB.setTable(plantDictionary[ID], sunlight, result)

    if not returnList[sunlightTitle]:
        print("Sunlight Not Found!")
    return returnList[sunlightTitle]


def getPicture(plantName):
    picturePath = Path(pictureTitle + plantName + ".png")
    if not picturePath.exists():
        scrap.webForPicture(plantName)
    #return None
    return picturePath


def getInformation(plantName):
    returnList = {temperatureTitle:"", phTitle:"", moistureTitle: "" , sunlightTitle: ""}#, pictureTitle : ""} 
    #getName
    plantDictionary = getPlantName(plantName)
    if not plantDictionary:
        return None

    #Tempurature
    if plantDictionary[temperature]:
        returnList[temperatureTitle] = plantDictionary[temperatureTitle]
    else:
        returnList[temperatureTitle] = getTemperatureInformation(plantDictionary)

    #ph
    if plantDictionary[pH]:
        returnList[phTitle] = plantDictionary[pH]
    else:
        returnList[phTitle] = getPhInformation(plantDictionary) 
        plantDictionary[pH] = returnList[phTitle]

    #Moisture
    if plantDictionary[moisture]:
        returnList[moistureTitle] = plantDictionary[moisture]
    else:
        returnList[moistureTitle] = getMoistureInformation(plantDictionary) 
        plantDictionary[moisture] = returnList[moistureTitle]

    #sunlight
    if plantDictionary[sunlight]:
        returnList[sunlightTitle] = plantDictionary[sunlight]
    else:
        returnList[sunlightTitle] = getSunlightInformation(plantDictionary) 
        plantDictionary[sunlight] = returnList[sunlightTitle]

    #picture
    #returnList[pictureTitle] = getPicture(plantDictionary[ChineseName])

    print("returnList : ", returnList)
    return returnList


def webScrap(plantName):
    #主程式
    getNeedInfo = getInformation(plantName)
    returnJson = json.dumps(getNeedInfo)
    return returnJson
    #return getNeedInfo 


if __name__ == "__main__":
    plantName = input("查詢的植物：")
    myDictionary = {ID : 0,
                    ChineseName : "",
                    EnglishName : [''],
                    ScientificName : [''],
                    Order : [''],
                    pH : "",
                    temperature : "",
                    moisture : "",
                    sunlight : "",
                    picture : ""}
    if plantName == "":
        plantName = "百日草"
    print("搜尋：", plantName)
    #getPicture(plantName)
    info = webScrap(plantName = plantName)
    print(info)

