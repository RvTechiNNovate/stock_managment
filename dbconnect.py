from pymysql import *
def getCon():
    con=connect(host='localhost',user='root',password='root',port=3306,database='stock')
    return con
