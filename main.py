# coding: UTF-8

import os
import web
from cybozubeatcard.weixinInterface import WeixinInterface
from cybozubeatcard.api import Api
from cybozubeatcard.apitest import ApiTest
from cybozubeatcard.updateuser import UpdateUser
from cybozubeatcard.getallusers import Getallusers
from cybozubeatcard.safecheckrun import SafeCheckRun
from com.boccaro.base import logg

urls = (
    '/msn', 'index',
    '/weixin', 'WeixinInterface',
    '/api', 'Api',
    '/api/test', 'ApiTest',
    '/api/updateuser', 'UpdateUser',
    '/api/getallusers', 'Getallusers',
    '/safecheckrun', 'SafeCheckRun'
)

class index:
    def GET(self):
        return "Hello, world!"

if __name__ == "__main__":
    logg.init(os.path.dirname(__file__))
    app = web.application(urls, globals())
    app.run()