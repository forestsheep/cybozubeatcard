# coding: UTF-8
"""
Created on 2014-9-25

@author: bxu
"""
import smtplib
from email.mime.text import MIMEText
from email.header import Header


def send_mail_test():
    e = EasyMail()
    e.mailto_list = ['forestsheep911@163.com'] 
    e.mail_host = "smtp.163.com"  # 设置服务器
    e.mail_user = "forestsheep"  # 用户名
    e.mail_pass = "xxx"  # 口令 
    e.mail_postfix = "163.com"  # 发件箱的后缀
    e.mail_subject = "subject"
    e.mail_context = 'abcdefghijklmnopqrstuvwxyz'
    e.send()


class EasyMail(object):
    mailto_list = None
    mail_host = None
    mail_sender_name = None
    mail_user = ''
    mail_pass = ''
    mail_postfix = ''
    mail_subject = ''
    mail_context = ''
    ssl_port = None

    def __init__(self):
        pass
    
    def send(self):
        if self.send_mail(self.mailto_list, self.mail_subject, self.mail_context):
            print 'mail send successed'
        else:
            print 'mail send failed'
        
    def send_mail(self, to_list, sub, content):
        if "@" in self.mail_user:
            me = self.mail_user
        else:
            me = self.mail_user + "@" + self.mail_postfix
        if self.mail_sender_name is not None:
            me = ("%s<" + me + ">") % (Header(self.mail_sender_name, 'utf-8'),)
        msg = MIMEText(content, _subtype='plain', _charset='utf-8')
        msg['Subject'] = sub
        msg['From'] = me
        msg['To'] = ";".join(to_list)
        try:
            if self.ssl_port is None:
                server = smtplib.SMTP()
                server.connect(self.mail_host)
                server.starttls()
            else:
                server = smtplib.SMTP_SSL()
                server.connect(self.mail_host + ":" + str(self.ssl_port))
            server.login(self.mail_user, self.mail_pass)
            server.sendmail(me, to_list, msg.as_string())
            server.close()
            return True
        except Exception, e:
            print str(e)
            return False
