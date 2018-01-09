#coding:UTF-8
import web
import json
import sqlite3
from com.boccaro.base import logg

class UpdateUser:
    def __init__(self):
        pass

    def GET(self):
        return "请使用POST"

        # return 'i recieved your get'

    def POST(self):
        jsonString = web.data()
        try:
            jsonObj = json.loads(jsonString)
            id = jsonObj.get(u'id')
            name = jsonObj.get(u'loginname')
            pw = jsonObj.get(u'pw')
            time = jsonObj.get(u'time')
            if id is None:
                return "field #id# not found."
            elif name is None:
                return "field #loginname# not found."
            elif pw is None:
                return "field #pw# not found."
            elif time is None:
                return "field #time# not found."
            
            conn = sqlite3.connect("test.db")
            c = conn.cursor()
            c.execute("update users set loginname = ?, pw = ?, time = ? where id = ?", (name, pw, time, id))
            if c.rowcount == 0:
                redict = dict()
                redict['success'] = 'false'
                redict['msg'] = '0 row effect'
                return json.dumps(redict, ensure_ascii=False, indent=4)
            conn.commit()
            redict = dict()
            redict['success'] = 'true'
            return json.dumps(redict, ensure_ascii=False, indent=4)

        except Exception, ex:
            logg.warn('type:    ' + str(type(ex)) + '    msg:    ' + str(ex))
            redict = dict()
            redict['type'] = str(type(ex))
            redict['msg'] = str(ex)
            return json.dumps(redict, ensure_ascii=False, indent=4)