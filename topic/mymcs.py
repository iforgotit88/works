import time  
import requests  
import json  
import random
from datetime import datetime

deviceId = "B1DTtaCcU"  
deviceKey = "1b731a830c6d2273ccaa2a0655defd69e9cf09f01efc7ef1dd8c74196baf844f"
#channel
datachannelId = "WaterHigh"
MCSURL = "163.18.42.232:3000"

def get_to_mcs(setTime = 0):
    #host = "http://api.mediatek.com"
    host = "http://163.18.42.232:3000"
    endpoint = "/api/devices/" + deviceId + "/datachannels/" + datachannelId + "/datapoints"
    
    url = host + endpoint
    #print("url : ", url)

    headers = {"Content-type": "application/json", "deviceKey": deviceKey}
    r = requests.get(url,headers=headers)
    #print(r.text)
    mcsjson = r.json()
    mcsjson = mcsjson['data']
    if len(mcsjson) > 2500:
        mcsjson = mcsjson[:2500]
    j = 0
    nowWaterLevel = ""
    while 1:
        nowWaterLevel = mcsjson[j]['values']
        nowWaterLevel = nowWaterLevel['value']
        if nowWaterLevel == " nan":
            j += 1
        else:
            if j > 0:
                print("最近值有錯誤！")
            break

    minDist = 60000
    select = []
    for item in mcsjson:
        if item['values']["value"] == " nan":
            continue

        dateformat = "%Y-%m-%dT%H:%M:%S"
        i = item['updatedAt']
        date = datetime.strptime(i[:-5], dateformat)
        date = date.timestamp()
        dist = abs(int(date) - int(setTime))
        if dist < minDist:
            minDist = dist
            select = item['values']["value"]
        else:
            break

    return(select, nowWaterLevel)


def getRain():
    today = datetime.now()
    startTime = datetime(today.year, today.month, today.day, 0, 0).timestamp()
    yesterdayHigh, todayHigh = get_to_mcs(startTime)
    print("今日水位 : ", todayHigh)
    print("昨日水位 : ", yesterdayHigh)
    rain = 0.0
    if todayHigh == " nan" or yesterdayHigh == " nan":
        print("Error")
        return None
    else:
        rain = float(todayHigh) - float(yesterdayHigh)
        print("降雨量 : " , rain)
        rain = {"rain":rain}
        returnJson = json.dumps(rain)
        return returnJson 


if __name__ == "__main__":
    getRain()

