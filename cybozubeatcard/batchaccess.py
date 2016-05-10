#coding:UTF-8
import web
import os
import sqlquery
import json
import request

class BatchAccess:
    def __init__(self):
        self.app_root = os.path.dirname(__file__)
        self.templates_root = os.path.join(self.app_root, 'templates')
        self.render = web.template.render(self.templates_root)

    def GET(self):
        data = web.input()
        s = str(data)
        sqlquery.writeLog('batch access assembled' + s)

    def POST(self):
        inputString = web.data()
        try:
            jb = json.loads(inputString)
            loginName = jb.get(u'loginName')
            loginpw = jb.get(u'loginPassWord')
            isSucc = request.grnliteLogin(loginName, loginpw)
            sqlquery.writeLog(loginName + '  ' + str(isSucc))
        except Exception, e:
            return sqlquery.writeLog(str(e))

