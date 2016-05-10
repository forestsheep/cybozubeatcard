# coding: UTF-8

import MySQLdb


def getConn():
    conn=MySQLdb.connect(host='localhost', user='root', passwd='milk', db='test', port=3306,)
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
