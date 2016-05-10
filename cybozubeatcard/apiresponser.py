# encoding: utf-8
import json
import sqlquery
import time
import urllib2
import request
from lxml import etree
from sae.taskqueue import Task, TaskQueue
import mailtest

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
            return beatReport(usersList)
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
                userDict['loginName'] = eval(repr(dbdataTuple[i][j])[1:])
            if j == 1:
                userDict['loginPassWord'] = eval(repr(dbdataTuple[i][j])[1:])
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
                userDict['loginName'] = eval(repr(dbdataTuple[i][j])[1:])
            if j == 1:
                userDict['loginPassWord'] = eval(repr(dbdataTuple[i][j])[1:])
            if j == 2:
                userDict['time'] = dbdataTuple[i][j]
                usersList.append(userDict)
    responseDict = dict(users=usersList)
    return json.dumps(responseDict)

def readHoliday():
    url = 'https://grn.cybozu.net.cn/cgi-bin/cbgrn/grn.cgi/cbpapi/base/api?c=28zd4'
    data = ''
    file = open('cybozubeatcard/templates/holiday_request.txt')

    while 1:
        lines = file.readlines(100000)
        if not lines:
            break
        for line in lines:
            data += line

    headers = {'Host':'grn.cybozu.net.cn','User-Agent':'NuSOAP/0.7.3 (1.114)','X-Cybozu-Mobile-Android':'aaa','Content-Type':'application/soap+xml; charset=UTF-8','SOAPAction':'"BaseGetCalendarEvents"'}
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
    file = open('cybozubeatcard/templates/cybozush_calendar_events.xml')

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
    return request.grnliteLoginCheck()

def forceBeat():
    queue = TaskQueue('batchgrn')
    usersString = getBeatCardUsers()
    sqlquery.writeLog(usersString)
    usersDict = json.loads(usersString)
    usersList = usersDict.get(u'users')
    for userDict in usersList:
        reqUserDict = dict()
        reqUserDict['loginName'] = eval(repr(userDict.get(u'loginName'))[1:])
        reqUserDict['loginPassWord'] = eval(repr(userDict.get(u'loginPassWord'))[1:])
        queue.add(Task('/batchaccess', json.dumps(reqUserDict)))

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

def beatReport(usersList):
    if usersList != None:
        for i in range(len(usersList)):
           userDict = usersList[i]
           userNameString = userDict.get(u'loginName')
           successBool = userDict.get(u'success')
           sqlquery.insertBeatReport(userNameString, successBool)
        return u'report recived.'
    else:
        sqlquery.writeLog('beatReport: usersList is None')
        return u'usersList is None.'
