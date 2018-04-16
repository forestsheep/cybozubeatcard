# coding: UTF-8
'''
Created on 2015-4-8

@author: bxu
'''
import hashlib
import datetime
import request
import rex
import re
# import sqlquery
import util
import sqlite3

def execute(wid, content):
    sayString = u'不能识别您的信息，请输入?或者??查询命令格式。'
    cmdRes = rex.commando(content)
    if cmdRes[0] == 113:
        return cmdRegUnqId(wid, cmdRes[1])
    if cmdRes[0] == 114:
        return cmdSeeAlive()
    if cmdRes[0] == 115:
        return cmdPause(wid)
    # if cmdRes[0] == 101:
    #     return cmdInputTempLoginName(wid, cmdRes[1])
    # if cmdRes[0] == 102:
    #     return cmdInputTempPassword(wid, cmdRes[1])
    # if cmdRes[0] == 103:
    #     return cmdVerifyLoginInfo(wid)
    # if cmdRes[0] == 104:
    #     return cmdSetDakaTime(wid, cmdRes[1])
    # if cmdRes[0] == 105:
    #     return cmdSetEnable(wid, cmdRes[1])
    # if cmdRes[0] == 106:
    #     return cmdHit(wid, cmdRes[1])
    # if cmdRes[0] == 107:
    #     return cmdMiss(wid, cmdRes[1])
    # if cmdRes[0] == 108:
    #     return cmdRemove(wid, cmdRes[1])
    # if cmdRes[0] == 109:
    #     return myPlan(wid)
    # if cmdRes[0] == 110:
    #     return weekPlan(wid)
    # if cmdRes[0] == 111:
    #     return info(wid)
    # if cmdRes[0] == 112:
    #     return cmdSetMail(wid, cmdRes[1])
    # if cmdRes[0] == 201:
    #     return getWeixinIdshorten(wid)
    if cmdRes[0] == 900:
        return cmdHelp()
    if cmdRes[0] == 901:
        return cmdHelpMore()
    return sayString

'''
cmd 113
注册唯一ID
'''
def cmdRegUnqId(wid, id):
    if id is None or id.strip() == "":
        return 'id不能为空'
    conn = sqlite3.connect("test.db")
    c = conn.cursor()
    sqlup = 'UPDATE users SET id = ? WHERE wx_id = ?'
    sqlins = 'INSERT INTO users (wx_id, id) VALUES(?, ?)'
    try:
        c.execute(sqlup, (id, wid))
        if c.rowcount == 0:
            c.execute(sqlins, (wid, id))
        conn.commit()
        return '更新成功您的id是' + id
    except Exception, ex:
        exstr = str(ex)
        if exstr.find('users.id') != -1 and exstr.find('UNIQUE') != -1:
            return "输入的id已经被注册了。"
        return "出现错误请联系开发者。"
    finally:
        conn.close()


'''
cmd 114
查看存活客户端
'''
def cmdSeeAlive():
    conn = sqlite3.connect("test.db")
    c = conn.cursor()
    sql = 'SELECT last_used_id, count(*) FROM client WHERE (julianday(datetime(\"now\", \"localtime\")) - julianday(\"last_active_time\"))*24 < 1 GROUP BY last_used_id'
    try:
        c.execute(sql)
        if c.rowcount == 0:
            return '目前没有在线的终端'
        else:
            alive_amount = 0
            # 目前先不用返回具体谁在线，总台数即可
            # rtnStr = '目前现在的客户端如下：\n'
            for row in c:
                alive_amount += row[1]
            return '目前在线的终端有' + str(alive_amount) + '台'
    except Exception, ex:
        exstr = str(ex)
        if exstr.find('users.id') != -1 and exstr.find('UNIQUE') != -1:
            return "输入的id已经被注册了。"
        return "出现错误请联系开发者。\n" + exstr
    finally:
        conn.close()


'''
cmd 115
暂停或激活服务
'''
def cmdPause(wid):
    conn = sqlite3.connect("test.db")
    c = conn.cursor()
    sqlup = 'UPDATE users SET pause = (pause != 1) WHERE wx_id = ?'
    sqlse = 'SELECT pause FROM users WHERE wx_id = ?'
    try:
        c.execute(sqlup, [wid])
        if c.rowcount == 0:
            return '也许是您还没有注册，输入  id+空格+您的id  来注册'
        conn.commit()
        c.execute(sqlse, [wid])
        for row in c:
            if row[0] == 0:
                return '您的服务运行中'
            else:
                return '您暂停了服务'
    except Exception, ex:
        exstr = str(ex)
        return "出现错误请联系开发者。\n" + exstr
    finally:
        conn.close()
'''
cmd 101
把临时用户名输入数据库
'''
# def cmdInputTempLoginName(wid, loginName):
#     rows = sqlquery.saveTempLoginName(wid, loginName)
#     if rows > 0:
#         return '您的用户名更新成功！'
#     else:
#         return '更新失败，请重试。'
'''

cmd 102
把临时密码输入数据库
'''
# def cmdInputTempPassword(wid, pw):
#     rows = sqlquery.saveTempPassword(wid, pw)
#     if rows > 0:
#         return '您的密码更新成功！'
#     else:
#         return '更新失败，请重试。'


'''
cmd 103
验证用户名密码是否通过
'''
# def cmdVerifyLoginInfo(wid):
#     loginInfo = sqlquery.getTempLoginInfo(wid)
#     if len(loginInfo) == 0:
#         return '请确认您输入过用户名和密码'
#     else:
#         if (loginInfo[0][0] == None or loginInfo[0][1] == None):
#             return '请确认您输入过用户名和密码'
#         loginName = loginInfo[0][0]
#         pw = loginInfo[0][1]
#         isSuccess = request.grnliteLogin(loginName, pw)
#         if isSuccess:
#             sqlquery.setLoginInfoAndVerified(wid)
#             return u'登录信息验证成功！[微笑]您可以通过命令time设置时间，然后输入enable开启服务。'
#         else:
#             return u'登录信息验证失败[流泪]，请确认输入正确的用户名密码后重新验证。'

'''
cmd 104
设置打卡时间
'''
# def cmdSetDakaTime(wid, time):
#     if not(time == '900' or time == '930'):
#         return '您输入的格式有误，现在只接受900和930两种时间'
#     rows = sqlquery.setDakaTime(wid, time)
#     if rows > 0:
#         return '设置成功！[微笑]'
#     else:
#         return '设置失败，请确认您已经输入过用户名密码。[流泪]'

'''
cmd 105
设置开启/关闭
'''
# def cmdSetEnable(wid, switch):
#     rows = sqlquery.setEnable(wid, switch)
#     if rows > 0:
#         if switch:
#             return '服务开启[微笑]'
#         else:
#             return '服务关闭[睡]'
#     else:
#         return '设置失败，请确认您已经输入过用户名密码。[流泪]'

'''
cmd 106
用户自定义打卡
'''
# def cmdHit(wid, dateString):
#     try:
#         date = util.dateFormat(dateString)
#     except Exception, e:
#         return u'出错了，可能是日期格式不正确'
#     exceptRcd = sqlquery.getUesrExceptionDate(wid, date)
#     if exceptRcd != None and len(exceptRcd) > 0:
#         rows = sqlquery.updateUesrExceptionDate(wid, date, 1)
#         if rows > 0:
#             return u'您更新了：' + date + u'执行。'
#         else:
#             return u'不需要任何操作。'
#     else:
#         rows = sqlquery.insertUesrExceptionDate(wid, date, 1)
#         if rows > 0:
#             return u'您新增了：' + date + u'执行。'
#         else:
#             return u'不需要任何操作。'


'''
cmd 107
用户自定义不打卡
'''
# def cmdMiss(wid, dateString):
#     if re.compile(ur'^(?i)tom(orrow)*$').match(dateString):
#         return cmdMissTomorrow(wid)
#     try:
#         date = util.dateFormat(dateString)
#     except Exception, e:
#         return u'出错了，可能是日期格式不正确'
#     exceptRcd = sqlquery.getUesrExceptionDate(wid, date)
#     if exceptRcd != None and len(exceptRcd) > 0:
#         rows = sqlquery.updateUesrExceptionDate(wid, date, 0)
#         if rows > 0:
#             return u'您更新了：' + date + u'取消执行。'
#         else:
#             return u'不需要任何操作。'
#     else:
#         rows = sqlquery.insertUesrExceptionDate(wid, date, 0)
#         if rows > 0:
#             return u'您新增了：' + date + u'取消执行。'
#         else:
#             return u'不需要任何操作。'

'''
明天不打卡
'''
# def cmdMissTomorrow(wid):
#     today = datetime.date.today()
#     offset = datetime.timedelta(days=1)
#     tomorrow = str(today + offset)
#     exceptRcd = sqlquery.getUesrExceptionDate(wid, tomorrow)
#     # return 'no' + str(exceptRcd)
#     if len(exceptRcd) > 0:
#         rows = sqlquery.updateUesrExceptionDate(wid, tomorrow, 0)
#         if rows > 0:
#             return u'您更新了：' + tomorrow + u'取消执行。'
#         else:
#             return u'不需要任何操作。'
#     else:
#         rows = sqlquery.insertUesrExceptionDate(wid, tomorrow, 0)
#         if rows > 0:
#             return u'您新增了：' + tomorrow + u'取消执行。'
#         else:
#             return u'不需要任何操作。'

'''
cmd 108
'''
# def cmdRemove(wid, dateString):
#     try:
#         date = util.dateFormat(dateString)
#     except Exception, e:
#         return u'出错了，可能是日期格式不正确'
#     rows = sqlquery.deleteUesrExceptionDate(wid, date)
#     if rows > 0:
#         return u'您删除了：' + date + u'本条规则。'
#     else:
#         return u'不需要任何操作。'

'''
cmd 109
查看今年个人特例
'''
# def myPlan(wid):
#     rows = sqlquery.getPersonalPlanThisYear(wid)
#     if len(rows) > 0:
#         rtnString = u'您今年的个人特例：\n'
#         for row in rows:
#             rtnString += str(row[0])
#             rtnString += u'  出' if row[1] == 1 else u'  欠' + '\n'
#             return rtnString
#     else:
#         return u'您今年没有任何个人特例'

'''
cmd 110
查看本周计划（未来7天包括今天）
'''
# def weekPlan(wid):
#     rtnString = u'您未来7天的计划：\n'
#     today = datetime.date.today()
#     for i in range(0 ,7):
#         offset = datetime.timedelta(days=i)
#         targetDay = str(today + offset)
#         rows = sqlquery.getBeatCardUserByWid(wid, targetDay)
#         if len(rows) > 0:
#             rtnString +=  str(targetDay) + u'  出\n'
#         else:
#             rtnString +=  str(targetDay) + u'  欠\n'
#     return rtnString
'''
cmd 111
查看个人设定资料
'''
# def info(wid):
#     rtnString = u'您的个人设定资料：\n'
#     rows = sqlquery.getPersonalInfo(wid)
#     if len(rows) > 0:
#         name = rows[0][0]
#         pw = rows[0][1]
#         daka = rows[0][2]
#         enable = rows[0][3]
#         rtnString += u'用户名：' + name + '\n'
#         rtnString += u'密码：' + pw + '\n'
#         rtnString += u'打卡时间：'
#         if daka == 900:
#             rtnString += '9:00'
#         elif daka == 930:
#             rtnString += '9:30'
#         else:
#             rtnString += u'您还未设置打卡时间'
#         rtnString += '\n'
#         rtnString += u'服务状态：'
#         if enable == 1:
#             rtnString += u'开启'
#         else:
#             rtnString += u'关闭'
#     else:
#         rtnString = u'您还未设定任何信息'
#     return rtnString

'''
cmd 112
设置邮箱
'''
# def cmdSetMail(wid, mailString):
#     rtn = sqlquery.setMail(wid, mailString)
#     if rtn == 1:
#         return u'邮箱设置成功。'
#     else:
#         return u'邮箱毋须重复设置。'


'''
cmd 201
取得短身份码
'''
# def getWeixinIdshorten(wid):
#     base32 = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h',
#         'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p',
#         'q', 'r', 's', 't', 'u', 'v', 'w', 'x',
#         'y', 'z',
#         '0', '1', '2', '3', '4', '5']
#     m = hashlib.sha512()
#     m.update(wid)
#     hexStr = m.hexdigest()
#     hexStrLen = len(hexStr)
#     subHexLen = hexStrLen / 128
#     output = []
#     for i in range(0,subHexLen):
#         subHex = '0x'+hexStr[i*16:(i+1)*16]
#         res = 0x3FFFFFFF & int(subHex,16)
#         out = ''
#         for j in range(3):
#             val = 0x0000001F & res
#             out += (base32[val])
#             res = res >> 5
#         output.append(out)
#     rows = sqlquery.setShortId(output[0], wid)
#     rtnString = u'您的身份码是：\n'
#     rtnString += output[0] + '\n'
#     rtnString += u'切勿透露给其他人。'
#     return rtnString

'''
cmd 900
帮助
'''
def cmdHelp():
    s = u'命令帮助\n'
    s += u'注册唯一id：id + 空格 + 您的id\n'
    s += u'查看在线终端数量：alive 或 al\n'
    s += u'暂停或恢复服务：pause 或 p'
    # s += u'查看个人设定资料\n'
    # s += u'输入登录名：user + 空格 + 您的登录名\n'
    # s += u'输入密码：pw + 空格 + 您的密码\n'
    # # s += u'验证用户名密码：bind\n'
    # s += u'设定时间：time + 空格 + 900/930\n'
    # s += u'启动服务：enable 或 en\n'
    # s += u'停用服务：disable 或 dis\n'
    # s += u'设定某日出勤：hit + 空格 + 年月日8位数字或月日4位数字（默认今年）\n'
    # s += u'设定某日缺勤：miss + 空格 + 年月日8位数字或月日4位数字（默认今年）\n'
    # s += u'取消某日规则：remove + 空格 + 年月日8位数字或月日4位数字（默认今年）\n'
    # s += u'设置警告邮箱：mail + 空格 + 你的邮箱\n'
    # s += u'获取身份码：iam\n'
    # s += u'查看扩展命令：??'
    return s

'''
cmd 901
帮助
'''
def cmdHelpMore():
    s = u'目前没有扩展命令'
    # s = u'扩展命令\n'
    # s += u'明天缺勤：miss tom[orrow]\n'
    # s += u'列出今年个人特例计划：myplan\n'
    # s += u'列出未来7天出欠计划（综合了个人假，国定假，工作日。优先度从高到低）：weekplan\n'
    return s