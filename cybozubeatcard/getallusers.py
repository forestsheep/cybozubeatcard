#coding:UTF-8
import web
import json
import sqlite3
from com.boccaro.base import logg


class Getallusers:
    def __init__(self):
        pass


    def GET(self):
        logg.info("get all users")
        try:
            conn = sqlite3.connect("test.db")
            c = conn.cursor()
            sql = 'SELECT loginname, pw FROM users WHERE loginname != \'\''
            c.execute(sql)
            users_dict = dict()
            users_dict['users'] = list()
            for row in c:
                auser = dict()
                auser['loginname'] = row[0]
                auser['pw'] = row[1]
                users_dict['users'].append(auser)
            return json.dumps(users_dict, ensure_ascii=False, indent=4)
        except Exception, ex:
            logg.warn('type:    ' + str(type(ex)) + '    msg:    ' + str(ex))
        finally:
            conn.close()

    def POST(self):
        return "请使用GET"
        