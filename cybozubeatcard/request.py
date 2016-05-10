# encoding: UTF-8
'''
Created on 2015-4-9

@author: bxu
'''

import urllib2
import cookielib
import datetime
import sqlquery

def grnLiteLoginArray(namepw):
    if namepw != None and len(namepw) == 2:
        loginName = namepw[0]
        pw = namepw[1]
        r =  grnliteLogin(loginName, pw)
        sqlquery.writeLog(loginName + ' accessed')
    else:
        return false

def grnliteLogin(loginName, pw):
    '''
    @summary: 访问grnlite
    @return: 如果成功则返回True
    '''

    url = 'https://grn.cybozu.net.cn/cgi-bin/cbgrn/grn.cgi/index?c=28zd4&_account='
    url = url + loginName + '&_password=' + pw
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookielib.CookieJar()))
    f = opener.open(url)
    resString = f.read()
    f.close()
    if ('<title>社員ポータル</title>' in resString
        or '<title>门户</title>' in resString
        or '<title>Portal</title>' in resString):
        return True
    else:
        return False

def grnliteLoginCheck():
    url = 'https://grn.cybozu.net.cn/cgi-bin/cbgrn/grn.cgi/index?c=28zd4&_account=bxu&_password=911911f911'
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookielib.CookieJar()))
    res = opener.open(url)
    grnTime = res.info().getheader('Date')
    d = datetime.datetime.strptime(grnTime, '%a, %d %b %Y %H:%M:%S GMT')
    now =  datetime.datetime.now()
    return str(d - now) + '\n' + str(now -d)

