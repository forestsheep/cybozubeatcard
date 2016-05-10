# coding: UTF-8

import web
from cybozubeatcard.weixinInterface import WeixinInterface
from cybozubeatcard.api import Api

urls = (
    '/msn', 'index',
    '/weixin', 'WeixinInterface',
    '/api', 'Api'
)

class index:
    def GET(self):
        return "Hello, world!"

if __name__ == "__main__":
    app = web.application(urls, globals())
    app.run()