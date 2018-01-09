# coding: UTF-8
'''
Created on 2015-4-8

@author: bxu
'''

import re

def commando(command):
    # 注册唯一标识ID
    ptnUnqID = re.compile(ur'^(?i)id\s*(.*)$')
    matchUnqID = ptnUnqID.match(command)
    if matchUnqID:
        return (113, matchUnqID.group(1))

    #输入用户名
    ptnInputLoginName = re.compile(ur'^(?i)user\s*(.*)$')
    matchInputLoginName = ptnInputLoginName.match(command)
    if matchInputLoginName:
        return (101, matchInputLoginName.group(1))

    #输入密码
    ptnInputLoginPw = re.compile(ur'^(?i)pw\s*(.*)$')
    matchInputLoginPw = ptnInputLoginPw.match(command)
    if matchInputLoginPw:
        return (102, matchInputLoginPw.group(1))

    #验证login信息
    # ptnLoginVerify = re.compile(ur'^(?i)bind\s*$')
    # matchLoginVerify = ptnLoginVerify.match(command)
    # if matchLoginVerify:
    #     return (103, matchLoginVerify.group(0))

    #设置时间
    ptnSetTime = re.compile(ur'^(?i)time\s*(.*)$')
    matchSetTime = ptnSetTime.match(command)
    if matchSetTime:
        return (104, matchSetTime.group(1))

    #设置开启
    ptnEnable = re.compile(ur'^(?i)en\s*$|^(?i)enable\s*$')
    matchEnable = ptnEnable.match(command)
    if matchEnable:
        return (105, True)

    #设置关闭
    ptnDisable = re.compile(ur'^(?i)dis\s*$|^(?i)disable\s*$')
    matchDisable = ptnDisable.match(command)
    if matchDisable:
        return (105, False)

    #用户自定义打卡
    ptnHit = re.compile(ur'^(?i)hit\s*(.*)$')
    matchHit = ptnHit.match(command)
    if matchHit:
        return (106, matchHit.group(1))

    #用户自定义不打卡
    ptnMiss = re.compile(ur'^(?i)miss\s*(.*)$')
    matchMiss = ptnMiss.match(command)
    if matchMiss:
        return (107, matchMiss.group(1))

    #取消用户自定义
    ptnRemove = re.compile(ur'^(?i)remove\s*(.*)$')
    matchRemove = ptnRemove.match(command)
    if matchRemove:
        return (108, matchRemove.group(1))

    #查看今年个人特例
    ptnMyplan = re.compile(ur'^(?i)myplan\s*$')
    matchMyplan = ptnMyplan.match(command)
    if matchMyplan:
        return (109, None)

    #查看本周计划
    if re.compile(ur'^(?i)weekplan\s*$').match(command):
        return (110, None)

    #查看个人信息
    if re.compile(ur'^(?i)info\s*$').match(command):
        return (111, None)

    #设置邮件
    match = re.compile(ur'^(?i)mail\s*(.*)$').match(command)
    if match:
        return (112, match.group(1))

    #取得短身份码
    if re.compile(ur'^(?i)iam\s*$').match(command):
        return (201, None)

    #帮助
    ptnHelp = re.compile(ur'^(?i)help|^\?$|^？$')
    matchHelp = ptnHelp.match(command)
    if matchHelp:
        return (900, None)

    #详细帮助
    ptnHelpMore = re.compile(ur'^\?\?$|^？？$')
    matchHelpMore = ptnHelpMore.match(command)
    if matchHelpMore:
        return (901, None)

    return (-1, None)