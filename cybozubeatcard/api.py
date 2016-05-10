#coding:UTF-8
import web
import os
import json
import apiresponser

class Api:
    def __init__(self):
        self.app_root = os.path.dirname(__file__)
        self.templates_root = os.path.join(self.app_root, 'templates')
        self.render = web.template.render(self.templates_root)

    def GET(self):
        data = web.input()
        return str(data)

    def POST(self):
        jsonString = web.data()
        rtnString = 'normal'
        try:
            rtnString = apiresponser.apiRoute(jsonString)
        except Exception, e:
            rtnString = 'error'
        return rtnString