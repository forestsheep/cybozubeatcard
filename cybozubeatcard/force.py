#coding:UTF-8
import web
import os
import sqlquery
import json
import apiresponser
from sae.taskqueue import Task, TaskQueue

class Force:
    def __init__(self):
        self.app_root = os.path.dirname(__file__)
        self.templates_root = os.path.join(self.app_root, 'templates')
        self.render = web.template.render(self.templates_root)

    def GET(self):
        self.runBatch()

    def POST(self):
        pass

    def runBatch(self):
        rows = sqlquery.getApiHistory()
        if len(rows) == 0:
            queue = TaskQueue('batchgrn')
            usersString = apiresponser.getBeatCardUsers()
            sqlquery.writeLog('emergency Beat: ' + usersString)
            usersDict = json.loads(usersString)
            usersList = usersDict.get(u'users')
            for userDict in usersList:
                reqUserDict = dict()
                reqUserDict['loginName'] = eval(repr(userDict.get(u'loginName'))[1:])
                reqUserDict['loginPassWord'] = eval(repr(userDict.get(u'loginPassWord'))[1:])
                queue.add(Task('/batchaccess', json.dumps(reqUserDict)))