#coding:UTF-8
import mysqlconn

def savetest(wx_id, note):
    sql = 'insert into test(name, note) values(%s, %s)'
    prm = (wx_id, note)
    rows = mysqlconn.execute(sql, prm)
    return rows

def writeLog(logMessage):
    sql = 'insert into cbc_log(message) values(%s)'
    prm = [logMessage]
    rows = mysqlconn.execute(sql, prm)
    return rows

def writeAccessLog(logMessage):
    sql = 'INSERT INTO cbc_api_log(note) VALUES(%s)'
    prm = [logMessage]
    rows = mysqlconn.execute(sql, prm)
    return rows

def saveTempLoginName(wid, loginName):
    sql = 'insert into cbc_users(weixin_id, login_name) values(%s, %s) ON DUPLICATE KEY UPDATE login_name =%s'
    prm = (wid, loginName, loginName)
    rows = mysqlconn.execute(sql, prm)
    return rows

def saveTempPassword(wid, pw):
    sql = 'insert into cbc_users(weixin_id, login_pw) values(%s, %s) ON DUPLICATE KEY UPDATE login_pw =%s'
    prm = (wid, pw, pw)
    rows = mysqlconn.execute(sql, prm)
    return rows

# def getTempLoginInfo(wid):
#     sql = 'select login_name_temp, login_pw_temp from cbc_users where weixin_id = %s'
#     prm = (wid)
#     rows = mysqlconn.select(sql, prm)
#     return rows

# def setLoginInfoAndVerified(wid):
#     sql = 'update cbc_users set verified = true, login_name = login_name_temp, login_pw = login_pw_temp where weixin_id = %s'
#     prm = (wid)
#     rows = mysqlconn.execute(sql, prm)
#     return rows

def setVerified(wid, b):
    sql = 'update cbc_users set verified = %s where weixin_id = %s'
    prm = (b, wid)
    rows = mysqlconn.execute(sql, prm)
    return rows

def setEnable(wid, b):
    sql1 = 'select enable from cbc_users where weixin_id = %s and enable = %s'
    prm1 = (wid, b)
    rows1 = mysqlconn.select(sql1, prm1)
    if len(rows1) > 0:
        return 1
    sql2 = 'update cbc_users set enable = %s where weixin_id = %s'
    prm2 = (b, wid)
    rows2 = mysqlconn.execute(sql2, prm2)
    return rows2

def setDakaTime(wid, time):
    sql1 = 'select daka_time from cbc_users where weixin_id = %s and daka_time = %s'
    prm1 = (wid, time)
    rows1 = mysqlconn.select(sql1, prm1)
    if len(rows1) > 0:
        return 1
    sql2 = 'update cbc_users set daka_time = %s where weixin_id = %s'
    prm2 = (time, wid)
    rows2 = mysqlconn.execute(sql2, prm2)
    return rows2

def getUesrExceptionDate(wid, date):
    sql = 'SELECT * FROM cbc_except_day WHERE weixin_id = %s AND date = %s'
    prm = (wid, date)
    rows = mysqlconn.select(sql, prm)
    return rows

def updateUesrExceptionDate(wid, date, beat):
    sql = 'UPDATE cbc_except_day SET beat = %s WHERE weixin_id = %s AND date = %s'
    prm = (beat, wid, date)
    rows = mysqlconn.execute(sql, prm)
    return rows

def insertUesrExceptionDate(wid, date, beat):
    sql = 'INSERT INTO cbc_except_day(weixin_id, date, priority, beat ) VALUES(%s, %s, %s, %s)'
    prm = (wid, date, 20, beat)
    rows = mysqlconn.execute(sql, prm)
    return rows

def deleteUesrExceptionDate(wid, date):
    sql = 'DELETE FROM cbc_except_day WHERE weixin_id = %s AND date = %s'
    prm = (wid, date)
    rows = mysqlconn.execute(sql, prm)
    return rows

def getBeatCardUsers(time):
    sql = 'SELECT login_name, login_pw FROM cbc_users WHERE cbc_users.enable AND cbc_users.status = 1 AND cbc_users.daka_time = %s AND cbc_users.weixin_id IN (SELECT T1.weixin_id FROM(SELECT weixin_id FROM cbc_users WHERE DAYOFWEEK(curdate()) != 1 AND DAYOFWEEK(curdate()) != 7 AND (SELECT count(*) = 0 FROM cbc_except_day WHERE cbc_except_day.date=curdate() AND cbc_except_day.priority = 10 AND cbc_except_day.beat = 0) OR ((DAYOFWEEK(curdate()) = 1 OR DAYOFWEEK(curdate()) = 7) AND (SELECT count(*) = 1 FROM cbc_except_day WHERE cbc_except_day.date=curdate() AND cbc_except_day.priority = 10 AND cbc_except_day.beat = 1)) UNION (SELECT cbc_users.weixin_id FROM cbc_users, cbc_except_day WHERE cbc_users.weixin_id = cbc_except_day.weixin_id AND cbc_except_day.date = curdate() AND cbc_except_day.priority = 20 AND cbc_except_day.beat = 1))T1 WHERE T1.weixin_id NOT IN (SELECT cbc_users.weixin_id FROM cbc_users, cbc_except_day WHERE cbc_users.weixin_id = cbc_except_day.weixin_id AND cbc_except_day.date = curdate() AND cbc_except_day.priority = 20 AND cbc_except_day.beat = 0))'
    prm = [time]
    rows = mysqlconn.select(sql, prm)
    return rows

def getBeatCardUserByWid(wid, date):
    sql = 'SELECT * FROM cbc_users WHERE weixin_id = %s AND cbc_users.enable AND cbc_users.weixin_id IN (SELECT T1.weixin_id FROM(SELECT weixin_id FROM cbc_users WHERE DAYOFWEEK(%s) != 1 AND DAYOFWEEK(%s) != 7 AND (SELECT count(*) = 0 FROM cbc_except_day WHERE cbc_except_day.date=%s AND cbc_except_day.priority = 10 AND cbc_except_day.beat = 0) OR ((DAYOFWEEK(%s) = 1 OR DAYOFWEEK(%s) = 7) AND (SELECT count(*) = 1 FROM cbc_except_day WHERE cbc_except_day.date=%s AND cbc_except_day.priority = 10 AND cbc_except_day.beat = 1)) UNION (SELECT cbc_users.weixin_id FROM cbc_users, cbc_except_day WHERE cbc_users.weixin_id = cbc_except_day.weixin_id AND cbc_except_day.date = %s AND cbc_except_day.priority = 20 AND cbc_except_day.beat = 1))T1 WHERE T1.weixin_id NOT IN (SELECT cbc_users.weixin_id FROM cbc_users, cbc_except_day WHERE cbc_users.weixin_id = cbc_except_day.weixin_id AND cbc_except_day.date = %s AND cbc_except_day.priority = 20 AND cbc_except_day.beat = 0))'
    prm = (wid, date, date, date, date, date, date, date, date)
    rows = mysqlconn.select(sql, prm)
    return rows

def getBeatCardUsersTest(date):
    sql = 'SELECT login_name, login_pw, daka_time FROM cbc_users WHERE cbc_users.enable AND cbc_users.status = 1 AND cbc_users.weixin_id IN (SELECT T1.weixin_id FROM(SELECT weixin_id FROM cbc_users WHERE DAYOFWEEK(%s) != 1 AND DAYOFWEEK(%s) != 7 AND (SELECT count(*) = 0 FROM cbc_except_day WHERE cbc_except_day.date=%s AND cbc_except_day.priority = 10 AND cbc_except_day.beat = 0) OR ((DAYOFWEEK(%s) = 1 OR DAYOFWEEK(%s) = 7) AND (SELECT count(*) = 1 FROM cbc_except_day WHERE cbc_except_day.date=%s AND cbc_except_day.priority = 10 AND cbc_except_day.beat = 1)) UNION (SELECT cbc_users.weixin_id FROM cbc_users, cbc_except_day WHERE cbc_users.weixin_id = cbc_except_day.weixin_id AND cbc_except_day.date = %s AND cbc_except_day.priority = 20 AND cbc_except_day.beat = 1))T1 WHERE T1.weixin_id NOT IN (SELECT cbc_users.weixin_id FROM cbc_users, cbc_except_day WHERE cbc_users.weixin_id = cbc_except_day.weixin_id AND cbc_except_day.date = %s AND cbc_except_day.priority = 20 AND cbc_except_day.beat = 0))'
    prm = (date, date, date, date, date, date, date, date)
    rows = mysqlconn.select(sql, prm)
    return rows

def getBeatCardUsersStatus(time):
    sql = 'SELECT cbc_users.mail, cbc_beat_report.success FROM cbc_users, cbc_beat_report WHERE cbc_users.enable AND cbc_users.daka_time = %s AND cbc_users.login_name = cbc_beat_report.login_name AND DATE(cbc_beat_report.date_time) = curdate() AND cbc_users.weixin_id IN (SELECT T1.weixin_id FROM(SELECT weixin_id FROM cbc_users WHERE DAYOFWEEK(curdate()) != 1 AND DAYOFWEEK(curdate()) != 7 AND (SELECT count(*) = 0 FROM cbc_except_day WHERE cbc_except_day.date=curdate() AND cbc_except_day.priority = 10 AND cbc_except_day.beat = 0) OR ((DAYOFWEEK(curdate()) = 1 OR DAYOFWEEK(curdate()) = 7) AND (SELECT count(*) = 1 FROM cbc_except_day WHERE cbc_except_day.date=curdate() AND cbc_except_day.priority = 10 AND cbc_except_day.beat = 1)) UNION (SELECT cbc_users.weixin_id FROM cbc_users, cbc_except_day WHERE cbc_users.weixin_id = cbc_except_day.weixin_id AND cbc_except_day.date = curdate() AND cbc_except_day.priority = 20 AND cbc_except_day.beat = 1))T1 WHERE T1.weixin_id NOT IN (SELECT cbc_users.weixin_id FROM cbc_users, cbc_except_day WHERE cbc_users.weixin_id = cbc_except_day.weixin_id AND cbc_except_day.date = curdate() AND cbc_except_day.priority = 20 AND cbc_except_day.beat = 0))'
    prm = [time]
    rows = mysqlconn.select(sql, prm)
    return rows

def deleteConstHoliday():
    sql = 'DELETE FROM cbc_except_day WHERE cbc_except_day.priority = 10'
    prm = ()
    rows = mysqlconn.execute(sql, prm)

def updateHoliday(date, beat):
    sql = 'INSERT INTO cbc_except_day(date, priority, beat) VALUES (%s, 10, %s)'
    prm = (date, beat)
    rows = mysqlconn.execute(sql, prm)

def getPersonalPlanThisYear(wid):
    sql = 'SELECT date, beat FROM cbc_except_day WHERE weixin_id = %s and date >= curdate() and date < CONCAT(YEAR(curdate()) + 1, \'-01-01\')'
    prm = [wid]
    rows = mysqlconn.select(sql, prm)
    return rows

def getApiHistory():
    sql = 'SELECT * from cbc_api_log WHERE date_add(access_datetime , interval 25 minute) >= now()'
    prm = ()
    rows = mysqlconn.select(sql, prm)
    return rows

def getPersonalInfo(wid):
    sql = 'SELECT login_name, login_pw, daka_time, enable FROM cbc_users WHERE weixin_id = %s'
    prm = [wid]
    rows = mysqlconn.select(sql, prm)
    return rows

def getPersonalInfoBySid(sid):
    sql = 'SELECT login_name, login_pw, daka_time, enable FROM cbc_users WHERE sid = %s'
    prm = [sid]
    rows = mysqlconn.select(sql, prm)
    return rows

def setShortId(sid, wid):
    sql = " UPDATE cbc_users SET sid = %s WHERE weixin_id = %s"
    prm = (sid, wid)
    rows = mysqlconn.execute(sql, prm)

def insert_beat_report(loginName, success):
    sql = 'INSERT INTO cbc_beat_report(login_name, success) VALUES (%s, %s)'
    prm = (loginName, success)
    rows = mysqlconn.execute(sql, prm)
    return rows


def setMail(wid, mail):
    sql = 'UPDATE cbc_users set mail = %s where weixin_id = %s'
    prm = (mail, wid)
    rows = mysqlconn.execute(sql, prm)
    return rows


def get_mail(login_name):
    sql = 'SELECT mail FROM cbc_users WHERE login_name = %s'
    prm = [login_name]
    rows = mysqlconn.select(sql, prm)
    return rows
