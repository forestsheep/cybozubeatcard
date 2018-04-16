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
            redict = dict()
            if id is None:
                redict['success'] = False
                redict['msg'] = 'field #id# is not found.'
                return json.dumps(redict, ensure_ascii=False, indent=4)
            elif name is None:
                redict['success'] = False
                redict['msg'] = 'field #loginname# is not found'
                return json.dumps(redict, ensure_ascii=False, indent=4)
            elif pw is None:
                redict['success'] = False
                redict['msg'] = 'field #pw# is not found'
                return json.dumps(redict, ensure_ascii=False, indent=4)
                return "field #pw# is not found."
            elif time is None:
                redict['success'] = False
                redict['msg'] = 'field #time# is not found'
                return json.dumps(redict, ensure_ascii=False, indent=4)
            
            conn = sqlite3.connect("test.db")
            c = conn.cursor()
            c.execute("update users set loginname = ?, pw = ?, btime = ? where id = ?", (name, pw, time, id))
            if c.rowcount == 0:
                redict['success'] = False
                redict['msg'] = '0 row effected'
                return json.dumps(redict, ensure_ascii=False, indent=4)
            conn.commit()
            redict['success'] = True
            redict['msg'] = str(c.rowcount) + ' row effected'
            return json.dumps(redict, ensure_ascii=False, indent=4)

        except Exception, ex:
            logg.warn('type:    ' + str(type(ex)) + '    msg:    ' + str(ex))
            redict = dict()
            redict['errtype'] = str(type(ex))
            redict['msg'] = str(ex)
            return json.dumps(redict, ensure_ascii=False, indent=4)