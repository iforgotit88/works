import pymysql
import myString 

dbUser = myString.getDBUser()
dbPass = myString.getDBPass()
dbName = myString.getDBName()
myport = myString.getDBPort()
myHost = myString.getDBHost()

nameDB = myString.getNameDB() 
phDB = myString.getPhDB()
moistureDB = myString.getMoistureDB()
temperatureDB = myString.getTempuratureDB()
sunlightDB = myString.getSunlightDB()

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

def addPlantName(plantName, fileName = nameDB):
    #要回傳的
    plantDictionary = {ID : 0,
                    ChineseName : [],
                    EnglishName : [],
                    ScientificName : [],
                    Order : []}
                    
    #方便讀取字典
    titleStrings = ["中文名稱", "英文名稱", "學名", "科名", "只是防止出錯用的"]
    dictionaryString = [ChineseName, EnglishName, ScientificName, Order]
    #資料庫新增的標籤
    dbInsertString = "cname,ename,sname,oname"
    dbInsertFormatString = "%s,%s,%s,%s"
    f = open(fileName, "r")
    nameList = f.read()

    index2 = 0

    nameList = nameList.split("\n")
    #用來記錄優先度的list，如：有中文名稱一樣的為主，而別名相同的優先度再後
    returnList = []
    for name in nameList:
        #csv以逗號分隔
        checkList = name.split(",")
        plantDictionary = {ID : 0,
                    ChineseName : [],
                    EnglishName : [],
                    ScientificName : [],
                    Order : []}
        
        index2 += 1
        index = 0
        plantDictionary[ID] = index2
        for addItem in checkList:
            if addItem == titleStrings[0] : continue
            if addItem == titleStrings[index + 1]:
                index = index + 1
                continue
            plantDictionary[dictionaryString[index]].append(addItem)

        for thetitle in dictionaryString:
            while "" in plantDictionary[thetitle]:
                plantDictionary[thetitle].remove("")

        for item in dictionaryString:
            x = ""
            for item2 in plantDictionary[item]:
                x = x + item2 + ","
            x = x[:-1]
            plantDictionary[item] = x

        print(plantDictionary)

        dbInsert(plantDictionary, plantDictionary[ID], dbInsertString, dbInsertFormatString)

    f.close()
    #表示沒找到，長度才會等於0
    if len(returnList) == 0:
        return plantDictionary


def additem(updateType, fileName, dbName = dbName, domain = myHost, user = dbUser, passwd = dbPass, port = myport):
    #開啟資料庫連線
    conn = pymysql.connect(host = domain, port = port, user = dbUser, passwd = dbPass, db = dbName)
    conn.select_db(dbName)
    #獲取遊標
    cursor=conn.cursor()

    f = open(fileName, "r")
    itemList = f.read()
    itemList = itemList.split("\n")
    for item in itemList:
        check = item.split(",")
        if len(check) < 2 or check[0].find('"') > -1:
            continue
        updateCheck = False
        updateList = []
        sql = 'select * from plant where ename = "' + check[0] + '";'
        cursor.execute(sql)
        while 1:
            res = cursor.fetchone()
            if not res :
                break
            else:
                sql = "update plant set " + updateType + " = '" + check[1] + "' where id = " + str(res[0])
                #更新一條資料
                update=cursor.execute(sql)
                updateCheck = True

        if updateCheck:
            continue

        sql = 'select * from plant where ename like "%' + check[0] + '";'
        cursor.execute(sql)
        while 1:
            res = cursor.fetchone()
            if not res :
                break
            else:
                sql = "update plant set " + updateType + " = '" + check[1] + "' where id = " + str(res[0])
                #更新一條資料
                update=cursor.execute(sql)
                updateCheck = True

        if updateCheck:
            continue

        sql = 'select * from plant where ename like "' + check[0] + '%";'
        cursor.execute(sql)
        while 1:
            res = cursor.fetchone()
            if not res :
                break
            else:
                sql = "update plant set " + updateType + " = '" + check[1] + "' where id = " + str(res[0])
                #更新一條資料
                update=cursor.execute(sql)
                updateCheck = True
    f.close()

    cursor.close()
    conn.commit()
    conn.close()


def dbInsert(plantDictionary, plantID, insertString, insertFormatString, dbName = dbName, domain = myHost, user = dbUser, passwd = dbPass, port = myport):
    #開啟資料庫連線
    conn = pymysql.connect(host = domain, port = port, user = dbUser, passwd = dbPass, db = dbName)
    conn.select_db(dbName)
    #獲取遊標
    cursor=conn.cursor()
    #另一種插入資料的方式，通過字串傳入值
    sql="insert into plant (" + insertString + ") values( " + insertFormatString + ")"
    cursor.execute(sql,(plantDictionary[ChineseName],plantDictionary[EnglishName],plantDictionary[ScientificName],plantDictionary[Order]))

    cursor.close()
    conn.commit()
    conn.close()
    print('sql insert執行成功')


if __name__ == "__main__":
    addPlantName("")
    additem(pH, phDB)
    additem(temperature, temperatureDB)
    additem(moisture, moistureDB)
    additem(sunlight, sunlightDB)
