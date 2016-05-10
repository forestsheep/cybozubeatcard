'''
Created on 2014-12-17

@author: bxu
'''
from random import Random
import string, random

class StringUtil(object):
    '''
    classdocs
    '''


    def __init__(self, params):
        '''
        Constructor
        '''
        pass
    
    
    @staticmethod
    def getRandomString(length):
        '''
        summary:get a random string by given length
        '''
        str = ''
        chars = 'AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz0123456789!@#$%^&*()-_+=[{]},.<>/?\|'
        clength = len(chars) - 1
        random = Random()
        for i in range(length):
            str+=chars[random.randint(0, clength)]
        return str
#         a = list(string.ascii_letters)
#         random.shuffle(a)
#         return ''.join(a[:length])
        pass