#coding:UTF-8
import web
import json
import sqlite3
import time
from com.boccaro.base import logg

class ClientInfo:
    def __init__(self):
        pass


    def GET(self):
        return "请使用PUT"


    def POST(self):
        return "请使用PUT"


    def PUT(self):
        conn = sqlite3.connect("test.db")
        c = conn.cursor()
        sqlup = 'UPDATE client SET last_active_time = ?, last_used_id = ?, report_times = report_times + 1, last_ver = ? WHERE serial = ?'
        sqlins = 'INSERT into client (serial, last_active_time, last_used_id, report_times, last_ver) values(?, ?, ?, ?, ?)'

        jsonString = web.data()
        try:
            jsonObj = json.loads(jsonString)
            ser = jsonObj.get(u'serial')
            lastid = jsonObj.get(u'last_used_id')
            lastver = jsonObj.get(u'last_ver')
            redict = dict()
            if ser is None:
                redict['success'] = False
                redict['msg'] = 'field #serial# is not found'
                return json.dumps(redict, ensure_ascii=False, indent=4)
            elif lastid is None:
                redict['success'] = False
                redict['msg'] = 'field #last_used_id# is not found'
                return json.dumps(redict, ensure_ascii=False, indent=4)
            c.execute(sqlup, (time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), lastid, lastver, ser))
            if c.rowcount == 0:
                c.execute(sqlins, (ser, time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), lastid, 1, lastver))
                if c.rowcount == 0:
                    redict['success'] = False
                    redict['msg'] = str(c.rowcount) + ' row inserted'
                    return json.dumps(redict, ensure_ascii=False, indent=4)
                conn.commit()
                redict['success'] = True
                redict['msg'] = str(c.rowcount) + ' row inserted'
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
        finally:
            conn.close()
