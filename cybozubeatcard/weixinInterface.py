#coding:UTF-8
import hashlib
import web
import lxml
from lxml import etree
import time
import os
import sqlquery
import cmd

class WeixinInterface:

    def __init__(self):
        self.app_root = os.path.dirname(__file__)
        self.templates_root = os.path.join(self.app_root, 'templates')
        self.render = web.template.render(self.templates_root)

    def GET(self):
        data = web.input()      # 获取输入参数
        signature = data.signature
        timestamp = data.timestamp
        nonce = data.nonce
        echostr = data.echostr
        token="saefgerfsv323fasdfev3q4gfdf"             # 自己的token
        list=[token,timestamp,nonce]    # 字典序排序
        list.sort()
        sha1=hashlib.sha1()             # sha1加密算法
        map(sha1.update, list)
        hashcode=sha1.hexdigest()
        if hashcode == signature:       # 如果是来自微信的请求，则回复echostr
            return echostr              # print "true"
        else:
            return "not from weixin"

    def POST(self):
        str_xml=web.data()
        xml=etree.fromstring(str_xml)
        msgType=xml.find("MsgType").text
        fromUser=xml.find("FromUserName").text
        toUser=xml.find("ToUserName").text
        content=''
        if msgType == 'event':
            event=xml.find("Event").text
            if event == 'subscribe':
                return self.render.reply_text(fromUser,toUser,int(time.time()), u'欢迎关注。我们的宗旨是“高高兴兴上班”。输入help或者?获得帮助信息。')
        elif msgType == 'text':
            try:
                content=xml.find("Content").text
            except Exception, e:
                return
            finally:
                pass

        # 对content进行trim
        content = content.strip()
        sayString = u''
        try:
            sayString = cmd.execute(fromUser, content)
        except Exception,e:
            sayString = str(e)
        return self.render.reply_text(fromUser,toUser,int(time.time()), sayString)