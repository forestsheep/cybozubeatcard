# encoding: utf-8
import os
import json
import sqlquery
import time
import urllib2
import request
from lxml import etree
import mailtest
from com.boccaro.network.email import easymail

def apiRoute(jsonObj):
    try:
        jb = json.loads(jsonObj)
        apiName = jb.get(u'api')
        if apiName == None:
            return u'api name is required.'
        elif apiName == u'getBeatCardUsers':
            userAgent = jb.get(u'userAgent')
            return getBeatCardUsers(userAgent)
        elif apiName == u'getBeatCardUsersTest':
            date = jb.get(u'date')
            if date == None:
                return u'date is required.'
            else:
                return getBeatCardUsersTest(date)
        elif apiName == u'holiday':
            return readHoliday_cybozush()
        elif apiName == u'timecheck':
            return timeCheck()
        elif apiName == u'forceBeat':
            return forceBeat()
        elif apiName == u'checkClient':
            return checkClient()
        elif apiName == u'getMyInfo':
            sid = jb.get(u'sid')
            return getMyInfo(sid)
        elif apiName == u'beatReport':
            usersList = jb.get(u'users')
            return beat_report(usersList)
        elif apiName == u'mail':
            mailtest.sendmail(u'testmail')
        else:
            return 'not found api.'
    except Exception, e:
        return str(e)
    pass

def getBeatCardUsers(userAgent):
    now = time.localtime(time.time())
    bt = int(time.strftime('%H%M', now))
    dbdataTuple = ()
    if 830 < bt and bt <= 910:
        dbdataTuple = sqlquery.getBeatCardUsers(900)
    elif 910 < bt and bt <= 940:
        dbdataTuple = sqlquery.getBeatCardUsers(930)
    # 如果没有，则返回用户里面是空的列表
    usersList = list()
    for i in range(len(dbdataTuple)) :
        userDict = dict()
        for j in range(len(dbdataTuple[i])):
            if j == 0:
                userDict['loginName'] = dbdataTuple[i][j]
            if j == 1:
                userDict['loginPassWord'] = dbdataTuple[i][j]
                usersList.append(userDict)
    responseDict = dict(users=usersList)
    responseString = json.dumps(responseDict)
    logDict = dict()
    if userAgent == None:
        logDict = dict(response = responseDict, userAgent = 'none')
    else:
        logDict = dict(response = responseDict, userAgent = userAgent)
    sqlquery.writeAccessLog(json.dumps(logDict))
    return responseString

def getBeatCardUsersTest(date):
    dbdataTuple = sqlquery.getBeatCardUsersTest(date)
    if len(dbdataTuple) == 0:
        return json.dumps(dict(users=list()))
    usersList = list()
    for i in range(len(dbdataTuple)) :
        userDict = dict()
        for j in range(len(dbdataTuple[i])):
            if j == 0:
                userDict['loginName'] = dbdataTuple[i][j]
            if j == 1:
                userDict['loginPassWord'] = dbdataTuple[i][j]
            if j == 2:
                userDict['time'] = dbdataTuple[i][j]
                usersList.append(userDict)
    responseDict = dict(users=usersList)
    return json.dumps(responseDict)

def readHoliday():
    url = 'https://cybozush.cybozu.cn/g/cbpapi/base/api'
    data = ''
    app_root = os.path.dirname(__file__)
    file = open(app_root + '/templates/holiday_request.txt')

    while 1:
        lines = file.readlines(100000)
        if not lines:
            break
        for line in lines:
            data += line

    headers = {'Host':'cybozush.cybozu.cn','User-Agent':'NuSOAP/0.7.3 (1.114)','X-Cybozu-Mobile-Android':'aaa','Content-Type':'application/soap+xml; charset=UTF-8','SOAPAction':'"BaseGetCalendarEvents"'}
    req = urllib2.Request(url, data, headers)
    response = urllib2.urlopen(req)
    rs = response.read()
    xml = etree.XML(rs)
    sqlquery.deleteConstHoliday()
    count = 0
    for r1 in xml:
        if r1.tag == '{http://www.w3.org/2003/05/soap-envelope}Body':
            for r2 in r1:
                if r2.tag == '{http://wsdl.cybozu.co.jp/base/2008}BaseGetCalendarEventsResponse':
                    for r3 in r2:
                        if r3.tag == 'returns':
                            for r4 in r3:
                                date = r4.get('date')
                                type1 = r4.get('type')
                                type2 = 0
                                if type1 == u'public_holiday':
                                    type2 = 0
                                elif type1 == u'public_workday':
                                    type2 = 1
                                sqlquery.updateHoliday(date, type2)
                                count += 1
    return str(count) + u'inserted.'

def readHoliday_cybozush():
    data = ''
    app_root = os.path.dirname(__file__)
    file = open(app_root + '/templates/cybozush_calendar_events.xml')

    while 1:
        lines = file.readlines(100000)
        if not lines:
            break
        for line in lines:
            data += line
    xml = etree.XML(data)
    sqlquery.deleteConstHoliday()
    count = 0
    for r1 in xml:
        if r1.tag == '{http://www.w3.org/2003/05/soap-envelope}Body':
            for r2 in r1:
                if r2.tag == '{http://wsdl.cybozu.co.jp/base/2008}BaseGetCalendarEventsResponse':
                    for r3 in r2:
                        if r3.tag == 'returns':
                            for r4 in r3:
                                date = r4.get('date')
                                type1 = r4.get('type')
                                type2 = 0
                                if type1 == u'public_holiday':
                                    type2 = 0
                                elif type1 == u'public_workday':
                                    type2 = 1
                                sqlquery.updateHoliday(date, type2)
                                count += 1
    return str(count) + u'inserted.'

def timeCheck():
    sqlquery.writeLog("cbc log")

def checkClient():
    rows = sqlquery.getApiHistory()
    if len(rows) > 0:
        return 'client has accessed a moment ago.'
    else:
        return 'client not accessed.'

def getMyInfo(sid):
    dbdataTuple = sqlquery.getPersonalInfoBySid(sid)
    if len(dbdataTuple) == 0:
        return json.dumps((json.dumps({})))
    infoDict = dict()
    for i in range(len(dbdataTuple[0])):
        if i == 0:
            infoDict['loginName'] = dbdataTuple[0][i]
        if i == 2:
            infoDict['beatTime'] = dbdataTuple[0][i]
        if i == 3:
            infoDict['enable'] = dbdataTuple[0][i]
    return json.dumps(infoDict)

def beat_report(users_list):
    if users_list is not None:
        for i in range(len(users_list)):
            user_dict = users_list[i]
            user_name_string = user_dict.get(u'loginName')
            success_bool = user_dict.get(u'success')
            sqlquery.insert_beat_report(user_name_string, success_bool)
            mailadd = sqlquery.get_mail(str(user_name_string))
            send_warning_mail(mailadd[0][0], success_bool)
        return u'report recived.'
    else:
        sqlquery.write_log('beatReport: usersList is None')
        return u'usersList is None.'


def send_warning_mail(mailto, success_int):
    try:
        e = easymail.EasyMail()
        e.mailto_list = [mailto]
        e.mail_host = "smtp.gmail.com"  # 设置服务器
        e.ssl_port = 465
        e.mail_user = "cybozushmobile@gmail.com"  # 用户名
        e.mail_pass = "cybozu123"  # 口令
        e.mail_postfix = "gmail.com"  # 发件箱的后缀
        e.mail_sender_name = u'高高兴兴上班社团'
        if success_int == 1:
            e.mail_subject = u'哒咔成功'
            e.mail_context = u'尽情的享受悠闲的早晨吧。'
        else:
            e.mail_subject = u'糟糕今天哒咔失败了'
            e.mail_context = u'赶快找点补救办法吧，譬如：自己用kunai打，找人代打，'
            e.mail_context += u'祈祷他人装了chrome插件已帮你打好，等等。'
        e.send()
    except Exception, e:
        sqlquery.writeLog(str(e))