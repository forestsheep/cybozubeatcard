#coding:UTF-8
import web
import os
import sqlquery
import json
import request
import time
from com.boccaro.network.email import easymail

class SafeCheckRun:
    def __init__(self):
        self.app_root = os.path.dirname(__file__)
        self.templates_root = os.path.join(self.app_root, 'templates')
        self.render = web.template.render(self.templates_root)

    def GET(self):
        data = web.input()
        s = str(data)

    def POST(self):
        inputString = web.data()
        now = time.localtime(time.time())
        bt = int(time.strftime('%H%M', now))
        dbdataTuple = ()
        if 830 < bt and bt <= 910:
            dbdataTuple = sqlquery.getBeatCardUsersStatus(900)
        elif 910 < bt and bt <= 2300:
            dbdataTuple = sqlquery.getBeatCardUsersStatus(930)
        for i in range(len(dbdataTuple)):
            mail = dbdataTuple[i][0]
            if mail == None:
                pass
            elif len(mail) == 0:
                pass
            else:
                sqlquery.writeLog(mail + str(dbdataTuple[i][1]))
                self.sendWarningMail(mail, dbdataTuple[i][1])

    def sendWarningMail(self, mailString, successInt):
        try:
            e = easymail.EasyMail()
            e.mailto_list = ['forestsheep911@163.com', mailString]
            e.mail_host = "smtp.163.com"  # 设置服务器
            e.mail_user = "forestsheep911@163.com"  # 用户名
            e.mail_pass = "911911f911"  # 口令 
            e.mail_postfix = "163.com"  # 发件箱的后缀
            e.mail_sender_name = u'高高兴兴上班社团'
            if successInt == 1:
                e.mail_subject = u'哒咔成功'
                e.mail_context = u'尽情的享受悠闲的早晨吧。'
            else:
                e.mail_subject = u'糟糕今天哒咔失败了'
                e.mail_context = u'赶快找点补救办法吧，譬如：找人代打，祈祷别人装了chrome插件已帮你打好，等等。'
            e.send()
        except Exception, e:
            sqlquery.writeLog(str(e))
