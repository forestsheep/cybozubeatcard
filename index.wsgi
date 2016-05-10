# coding: UTF-8
import os

import sae
import web

from cybozubeatcard.weixinInterface import WeixinInterface
from cybozubeatcard.api import Api
from cybozubeatcard.force import Force
from cybozubeatcard.batchaccess import BatchAccess
from cybozubeatcard.safecheck import SafeCheck
from cybozubeatcard.safecheckrun import SafeCheckRun

urls = (
    '/', 'Hello',
    '/weixin', 'WeixinInterface',
    '/api', 'Api',
    '/force', 'Force',
    '/batchaccess', 'BatchAccess',
    '/safecheck', 'SafeCheck',
    '/safecheckrun', 'SafeCheckRun'
)

app_root = os.path.dirname(__file__)
templates_root = os.path.join(app_root, 'templates')
render = web.template.render(templates_root)

class Hello:
   def GET(self):
        return ("hello")

app = web.application(urls, globals()).wsgifunc()
application = sae.create_wsgi_app(app)