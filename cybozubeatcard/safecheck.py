#coding:UTF-8
import web
import os
import sqlquery
import json
import apiresponser
from sae.taskqueue import Task, TaskQueue

class SafeCheck:
    def __init__(self):
        self.app_root = os.path.dirname(__file__)
        self.templates_root = os.path.join(self.app_root, 'templates')
        self.render = web.template.render(self.templates_root)

    def GET(self):
        self.runBatch()

    def POST(self):
        pass

    def runBatch(self):
        # sqlquery.writeLog('try to run task')
        # try:
        queue = TaskQueue('safecheck')
        queue.add(Task('/safecheckrun', 'safe parm'))
        # except Exception, e:
        #     sqlquery.writeLog("queue error is: " + str(e))