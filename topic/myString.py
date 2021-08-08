dbUser = "root"
dbPass = "GW32jw2gAKTJ"
dbName = "scrap_db"
dbPort = 3310
dbHost = "localhost"

nameDB = r"myDB\name.csv"
phDB = r"myDB\ph.csv"
moistureDB = r"myDB\moisture.csv"
tempuratureDB = r"myDB\temperature.csv"
sunlightDB = r"myDB\sunlight.csv"
pictureTitle = r"myDB\picture\ "
#dictionaryName = {"中文名稱": "ChineseName", "英文名稱":"EnglishName", "學名":"ScientificName", "科名":"order", "別名":"OtherName"}
dictionaryName = {"中文名稱": "cname", "英文名稱":"ename", "學名":"sname", "科名":"oname", "別名":"other"}
dictionaryInformation = {"溫度":"temperature", "濕度":"moisture", "ph值":"pH", "日照":"sunlight", "照片":"picture"}
titleStrings = ["中文名稱", "英文名稱", "學名", "科名", ["別名", "別稱"], "只是防止出錯用的"]


def getNameDB():
    return nameDB


def getPhDB():
    return phDB


def getMoistureDB():
    return moistureDB


def getTempuratureDB():
    return tempuratureDB


def getPicture():
    #因為\" 會被視為字串，需要以空間來區間
    return pictureTitle[:-1]


def getSunlightDB():
    return sunlightDB


def getPlantCName():
    return dictionaryName["中文名稱"]


def getPlantEName():
    return dictionaryName["英文名稱"]


def getPlantSName():
    return dictionaryName["學名"]


def getPlantOrder():
    return dictionaryName["科名"]


def getPlantOName():
    return dictionaryName["別名"]


def getTemperatureName():
    return dictionaryInformation["溫度"]


def getMoistureName():
    return dictionaryInformation["濕度"]


def getPhName():
    return dictionaryInformation["ph值"]


def getSunlightName():
    return dictionaryInformation["日照"]


def getPictureName():
    return dictionaryInformation["照片"] 


def getTitleStrings():
    return titleStrings


def getDBUser():
    return dbUser

def getDBPass():
    return dbPass

def getDBName():
    return dbName 

def getDBPort():
    return dbPort

def getDBHost():
    return dbHost
if __name__ == "__main__":
    print(getPicture())
