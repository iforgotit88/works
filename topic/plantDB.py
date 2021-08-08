import myString
import pymysql


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

def getPlantName(plantName, dbName = dbName, domain = myHost, user = dbUser, passwd = dbPass, port = myport ):#, fileName = nameDB):
    #要回傳的
    plantDictionary = {ID : 0,
                    ChineseName : '',
                    EnglishName : [''],
                    ScientificName : [''],
                    Order : [''],
                    pH : '',
                    temperature : '',
                    moisture : '',
                    sunlight : '',
                    picture : ''}
                    
    #方便讀取字典
    titleStrings = ["中文名稱", "英文名稱", "學名", "科名", "只是防止出錯用的"]
    dictionaryString = [ID, ChineseName, EnglishName, ScientificName, Order, pH, temperature, moisture, sunlight, picture]

    #開啟資料庫連線，指定資料庫
    conn = pymysql.connect(host = domain, port = port, user = user, passwd = passwd)
    conn.select_db(dbName)
    #獲取遊標
    cursor=conn.cursor()
    #Search
    cursor.execute('SELECT * FROM plant where cname = "' + plantName + '";')
    while 1:
        res = cursor.fetchone()
        if not res :
            break
        for i, items in enumerate(res):
            if i <= 1 or i >= 5: 
                plantDictionary[dictionaryString[i]] = items
                continue
            items = items.split(",")
            strlist = []
            for item in items:
                strlist.append(item)

            plantDictionary[dictionaryString[i]] = strlist

    print(plantDictionary)

    cursor.close()#先關閉遊標
    conn.commit()
    conn.close()#再關閉資料庫連線
    print("success")
    return plantDictionary


def setPlantName(plantDictionary, dbName = dbName, domain = myHost, user = dbUser, passwd = dbPass, port = myport):#, fileName = nameDB):
    #開啟資料庫連線
    conn = pymysql.connect(host = domain, port = port, user = dbUser, passwd = dbPass, db = dbName)
    conn.select_db(dbName)
    #獲取遊標
    cursor=conn.cursor()
    #另一種插入資料的方式，通過字串傳入值
    sql="insert into plant (cname,ename,sname,oname) values(%s,%s,%s,%s)"
    cursor.execute(sql,(plantDictionary[ChineseName], ",".join(plantDictionary[EnglishName]), ",".join(plantDictionary[ScientificName]), ",".join(plantDictionary[Order])))

    cursor.close()
    conn.commit()
    conn.close()


def updatePlantName(plantDictionary, plantID, dbName = dbName, domain = myHost, user = dbUser, passwd = dbPass, port = myport):
    #開啟資料庫連線
    conn = pymysql.connect(host = domain, port = port, user = dbUser, passwd = dbPass, db = dbName)
    conn.select_db(dbName)
    #獲取遊標
    cursor=conn.cursor()
    #另一種插入資料的方式，通過字串傳入值
    sql="update plant set cname  = %s where id = " + str(plantID)
    cursor.execute(sql,(plantDictionary[ChineseName]))
    sql="update plant set ename  = %s where id = " + str(plantID)
    cursor.execute(sql,(",".join(plantDictionary[EnglishName])))
    sql="update plant set sname  = %s where id = " + str(plantID)
    cursor.execute(sql,(",".join(plantDictionary[ScientificName])))
    sql="update plant set oname  = %s where id = " + str(plantID)
    cursor.execute(sql,(",".join(plantDictionary[Order])))

    cursor.close()
    conn.commit()
    conn.close()
    print("update success")


def setTable(plantID, setType, setText, dbName = dbName, domain = myHost, user = dbUser, passwd = dbPass, port = myport):
    #開啟資料庫連線
    conn = pymysql.connect(host = domain, port = port, user = dbUser, passwd = dbPass, db = dbName)
    conn.select_db(dbName)
    #獲取遊標
    cursor=conn.cursor()
    #另一種插入資料的方式，通過字串傳入值
    sql="update plant set " + setType + " = %s where id = " + str(plantID)
    cursor.execute(sql,(setText))

    cursor.close()
    conn.commit()
    conn.close()
    print("update " + setType + " success")


def createDB(dbname = dbName, domain = myHost, user = dbUser, passwd = dbPass, port = myport):
    #開啟資料庫連線，不需要指定資料庫，因為需要建立資料庫 
    conn = pymysql.connect(host = domain, port = port, user = user, passwd = passwd)
    #獲取遊標
    cursor=conn.cursor()
    #建立pythonBD資料庫
    cursor.execute('CREATE DATABASE IF NOT EXISTS ' + dbname + ' DEFAULT CHARSET utf8 COLLATE utf8_general_ci;')
    cursor.close()#先關閉遊標
    conn.close()#再關閉資料庫連線
    print('建立' + dbname + '資料庫成功')


def createTable(dbName = dbName, domain = myHost, user = dbUser, passwd = dbPass, port = myport):
    #開啟資料庫連線
    conn = pymysql.connect(host = domain, port = port, user = dbUser, passwd = dbPass, db = dbName)
    #獲取遊標
    cursor=conn.cursor()
    print(cursor)

    #建立 plant表
    cursor.execute('drop table if exists plant')
    sql="""CREATE TABLE IF NOT EXISTS plant (
          id int(11) NOT NULL AUTO_INCREMENT,
          cname varchar(60) NOT NULL,
          ename varchar(60) NOT NULL,
          sname varchar(60) DEFAULT '',
          oname varchar(60) DEFAULT '',
          pH varchar(20) DEFAULT '',
          temperature varchar(20) DEFAULT '',
          moisture varchar(20) DEFAULT '',
          sunlight varchar(20) DEFAULT '',
          picture varchar(255) DEFAULT '',
          PRIMARY KEY (`id`)
        ) ENGINE=InnoDB  DEFAULT CHARSET=utf8 AUTO_INCREMENT=0"""

    cursor.execute(sql)

    cursor.close()#先關閉遊標
    conn.close()#再關閉資料庫連線
    print('建立資料表成功')


if __name__ == "__main__":
    #createTable()
    #plantDictionary = getPlantName("百日草")
    #setTable(plantDictionary[ID], pH, "2.5-4.1")
    #print(plantDictionary)
    #setTable(plantDictionary[ID], pH, "")
    #print(plantDictionary)
    
    #getSunlight("百日草")
    
    plantDictionary = {ID : 19,
                    ChineseName : "山茶",
                    EnglishName : ['camellia'],
                    ScientificName : [],
                    Order : ["山茶科", "Theaceae"],
                    pH : "4.5-5.5",
                    temperature : "10-16",
                    moisture : "21-40",
                    sunlight : "full sun",
                    picture : ""}
    setTable(plantDictionary[ID], pH, plantDictionary[pH])
    print(plantDictionary)
    #setPlantName(plantDictionary)
    #updatePlantName(plantDictionary, 463)
    
