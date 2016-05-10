# coding: UTF-8
'''
Created on 2015-4-8

@author: bxu
'''
import time
'''
日期转化
输入4位数字代表今年的某月某日
输入8位数字代表某年某月某日
'''
def dateFormat(dateString):
    try:
        outputDate = None
        if len(dateString) <= 4:
            now = time.localtime(time.time())
            nowyear= now.tm_year
            outputDate = time.strptime(str(nowyear) + dateString, "%Y%m%d")
        else:
            outputDate = time.strptime(dateString, "%Y%m%d")
        rtnString = time.strftime("%Y-%m-%d", outputDate)
        return rtnString
    except Exception, e:
        raise
