# encoding: utf-8
from com.boccaro.network.email import easymail
from com.boccaro.utils import stringutil

def sendmail(mailcontext):
    e = easymail.EasyMail()
    e.mailto_list = ['bxu@cybozu.net.cn', 'forestsheep@163.com', 'forestsheep911@163.com', 'forestsheep911@gmail.com']
    e.mail_host = "smtp.163.com"  # 设置服务器
    e.mail_user = "forestsheep911@163.com"  # 用户名
    e.mail_pass = "911911f911"  # 口令 
    e.mail_postfix = "163.com"  # 发件箱的后缀
    e.mail_subject = 'server mail test'
    e.mail_sender_name = u'才望子高高兴兴上班社团委员会'
    e.mail_context = mailcontext
    e.send()
    pass