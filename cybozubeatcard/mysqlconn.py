# coding: UTF-8

import MySQLdb
import sae.const

def getConn():
    conn=MySQLdb.connect(host=sae.const.MYSQL_HOST, user=sae.const.MYSQL_USER, passwd=sae.const.MYSQL_PASS, db=sae.const.MYSQL_DB, port=int(sae.const.MYSQL_PORT), charset='utf8')
    return conn

def getCursor(conn):
    cursor=conn.cursor()
    return cursor

def select(selectQueryString, param):
    try:
        conn = getConn()
        cursor = getCursor(conn)
        cursor.execute(selectQueryString, param)
        return cursor.fetchall()
    except MySQLdb.Error,e:
        pass
    finally:
        cursor.close()
        conn.close()

def execute(executeQueryString, param):
    try:
        conn = getConn()
        cursor = getCursor(conn)
        n = cursor.execute(executeQueryString, param)
        return n
    except MySQLdb.Error,e:
        pass
    finally:
        cursor.close()
        conn.close()
