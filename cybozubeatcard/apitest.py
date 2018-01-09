#coding:UTF-8
import web
import os
import json
import apiresponser
import sqlite3
from com.boccaro.base import logg

class ApiTest:
    def __init__(self):
        pass
        # self.app_root = os.path.dirname(__file__)
        # self.templates_root = os.path.join(self.app_root, 'templates')
        # self.render = web.template.render(self.templates_root)

    def GET(self):
        # data = web.input()
        # return str(data)
        # conn = sqlite3.connect('test.db')
        # c = conn.cursor()
        # c.execute("SELECT * from nihao")
        # ss = ''
        # for row in c:
        #     ss += str(row)
        #     logg.info(row);
        # return ss

        # return 'i recieved your get'
        pass

    def POST(self):
        jsonString = web.data()
        # try:
        #     jsonObj = json.loads(jsonString)
        #     name = jsonObj.get(u'username')
        #     if name == None:
        #         return "not found name"
        #     return name
        # except Exception, ex:
        #     return "something error."