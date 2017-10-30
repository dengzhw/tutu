# _*_ coding:utf-8 _*_
import pymysql  # python3连接数据库的模块pymysql
import threading

Lock = threading.Lock()


class DBSingleton(object):
    # 定义静态变量实例
    __instance = None

    def __init__(self):
        self.connect = pymysql.connect(
            user="root",
            password="1332925",  # 连接数据库，不会的可以看我之前写的连接数据库的文章
            port=3306,
            host="127.0.0.1",
            db="mydb",
            charset="utf8"
        )
        self.con = self.connect.cursor()

        print("数据库创建成功")

    def __new__(cls, *args, **kwargs):
        if not cls.__instance:
            try:
                Lock.acquire()
                # double check
                if not cls.__instance:
                    cls.__instance = super(DBSingleton, cls).__new__(cls, *args, **kwargs)
            finally:
                Lock.release()
        return cls.__instance

    def queryActionByUrl(self, url, type):
        table_name = type + "_tb"
        row_count = self.con.execute(
            "select * from " + table_name + "  where url = '%s'".format(url)
        )
        rows = self.con.fetchone()
        print("select result:" + str(row_count) + " ----" + str(rows))
        if row_count == 0:
            print("Item Not in db: %s" % url)
            return True
        else:
            print("Item already stored in db: %s" % url)

            return False

    def inserAction(self, item, type):
        table_name = type + "_tb"
        try:
            print("开始存储到数据库")
            if type == 'article':
                print("article开始存储到数据库")
                self.con.execute(
                    "insert into " + table_name + "  (url,title,subtitle,icon,type,comefrom,hotmark,content,image_url) values (%s,%s,%s,%s,%s,%s,%s,%s,%s)",
                    (item['url'],
                     item['title'],
                     item['subtitle'],
                     item['icon'],
                     item['type'],
                     item['comefrom'],
                     item['hotmark'],
                     item['content'],
                     item['image_url']
                     )
                )
            else:
                self.con.execute(
                    "insert into " + table_name + "  (url,title,subtitle,content,imgurls,type) values (%s, %s,%s,%s, %s,%s)",
                    (item['url'],
                     item['title'],
                     item['subtitle'],
                     item['content'],
                     item['image_url'],
                     item['type'])
                )
            print("数据库执行完成")
            result = self.con.fetchone()
            print("select result:" + str(result))
            self.connect.commit()
            print("数据库提交执行完成")
            print("Item already Insert in db: %s" % item)
            return True
        except Exception as e:
            print("Item Insert Fiald in db: %s" % item)
            self.connect.rollback()
            return False

    def queryData(self, table_name, pagecount, pageSize):
        querysql = "SELECT * FROM " + table_name + " limit %d,%d" % ((pagecount-1)*pageSize, pageSize)
        self.con.execute(querysql)
        rowsInfo = self.con.fetchall()
        return rowsInfo

    def closedb(self):
        self.con.close()
        self.connect.close()
