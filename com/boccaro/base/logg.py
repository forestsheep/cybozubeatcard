# coding:UTF-8
import inspect
import json
import logging.config
import os


def init(approot):
    if not os.path.exists('log'):
        os.makedirs('log')
    config = json.load(open(os.path.join(approot, 'conf/logger.config')))
    logging.config.dictConfig(config)
    info('log init successful.')
    pass


def info_response(msg):
    logger = logging.getLogger('mylogger')
    logger.info(msg)
    pass


def info(msg):
    logger = logging.getLogger('mylogger')
    stack = inspect.stack()
    infodict = dict()
    infodict['method'] = stack[1][3]
    infodict['file'] = stack[1][1]
    infodict['line'] = stack[1][2]
    infodict['source code'] = stack[1][4]
    infodict['message'] = msg
    logger.info(json.dumps(infodict, ensure_ascii=False, indent=4))
    pass


def error(msg):
    logger = logging.getLogger('mylogger')
    stack = inspect.stack()
    infodict = dict()
    infodict['method'] = stack[1][3]
    infodict['file'] = stack[1][1]
    infodict['line'] = stack[1][2]
    infodict['source code'] = stack[1][4]
    infodict['message'] = msg
    logger.error(json.dumps(infodict, ensure_ascii=False, indent=4))
    pass


def debug(msg):
    logger = logging.getLogger('mylogger')
    stack = inspect.stack()
    infodict = dict()
    infodict['method'] = stack[1][3]
    infodict['file'] = stack[1][1]
    infodict['line'] = stack[1][2]
    infodict['source code'] = stack[1][4]
    infodict['message'] = msg
    logger.debug(json.dumps(infodict, ensure_ascii=False, indent=4))
    pass


def warn(msg):
    logger = logging.getLogger('mylogger')
    stack = inspect.stack()
    infodict = dict()
    infodict['method'] = stack[1][3]
    infodict['file'] = stack[1][1]
    infodict['line'] = stack[1][2]
    infodict['source code'] = stack[1][4]
    infodict['message'] = msg
    logger.warn(json.dumps(infodict, ensure_ascii=False, indent=4))
    pass


def critical(msg):
    logger = logging.getLogger('mylogger')
    stack = inspect.stack()
    infodict = dict()
    infodict['method'] = stack[1][3]
    infodict['file'] = stack[1][1]
    infodict['line'] = stack[1][2]
    infodict['source code'] = stack[1][4]
    infodict['message'] = msg
    logger.critical(json.dumps(infodict, ensure_ascii=False, indent=4))
    pass


