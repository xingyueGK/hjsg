#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2024/11/19 12:19
# @Author  : yuege
# @File    : 基础登录



from task.base import SaoDangFb
import time
import  os,configparser
from logging.handlers import RotatingFileHandler
import logging
import random

config= configparser.ConfigParser()
config_file = '%s/conf/conf.ini' % (os.path.dirname(os.path.abspath(__file__)))

config.read(config_file,encoding='utf-8')
class ContextFilter(logging.Filter):

    username = 'USER'
    addr = 'ADDR'

    def filter(self, record):
        record.addr = self.addr
        record.username = self.username
        return True

def my_listener(event):
    if event.exception:
        print('The job crashed :(') # or logger.fatal('The job crashed :(')
    else:
        print('The job worked :)')



class MyLog(object):
    def __init__(self,level=logging.INFO,logpath=None, logname='mylog.log'):
        if logpath:
            if not os.path.exists(logpath):
                os.makedirs(logpath)
                self._log = os.path.join(logpath, logname)
            else:
                self._log = os.path.join(logpath, logname)
        else:
            self._log = logname

        self.filter_ = ContextFilter()
        self.logger = logging.getLogger(__name__)
        # 这为清空当前文件的logging 因为logging会包含所有的文件的logging
        logging.Logger.manager.loggerDict.pop(__name__)
        self.logger.handlers = []
        # 然后再次移除当前文件logging配置
        self.logger.removeHandler(self.logger.handlers)
        self.logger.addFilter(self.filter_)
        self.logger.setLevel(level)
        self.format = logging.Formatter(
            '%(asctime)s %(filename)s[line:%(lineno)d] [%(username)s:%(addr)s] %(levelname)s %(message)s')



    def console(self,level,message):
        ch = logging.StreamHandler()
        ch.setFormatter(self.format)

        fh = RotatingFileHandler(self._log, mode='a', maxBytes=1024 * 1024 * 1024, backupCount=3, encoding='utf-8')
        fh.setFormatter(self.format)
        self.logger.addHandler(fh)
        self.logger.addHandler(ch)
        if level == 'info':
            self.logger.info(message)
        elif level == 'debug':
            self.logger.debug(message)
        elif level == 'warning':
            self.logger.warning(message)
        elif level == 'error':
            self.logger.error(message)
        # 这两行代码是为了避免日志输出重复问题
        self.logger.removeHandler(ch)
        self.logger.removeHandler(fh)
        # 关闭打开的文件
        fh.close()

    def debug(self, message):
        self.console('debug', message)

    def info(self, message):
        self.console('info', message)

    def warning(self, message):
        self.console('warning', message)

    def error(self, message):
        self.console('error', message)



class Hjsg(SaoDangFb):
    def __init__(self,user, passwd, num,log,lockpwd=None):
        super(Hjsg,self).__init__(user, passwd, num)
        self.log = log
        self.lockpwd = lockpwd
    def unlock(self, pwd):
        return self.action(c='member', m='resource_unlock', pwd=pwd)
    def action(self, body=0, **kwargs):
        """动作参数m={'index':'获取基础账号密码等信息',‘get_monster_list’：“获取副本怪物列表信息”}
        """
        action_data = kwargs
        try:
            # 每个请求降级一下太快了
            time.sleep(random.uniform(0, 1))
            postresult = self.post_url(body, action_data)
            serverinfo = postresult.json(encoding="UTF-8")
            if serverinfo == 403:
                self.log.error('您已失去登录状态，请重新登录！')
                time.sleep(3)
                # 重新初始化
                self.token = self.get_token(self.num, self.user, self.passwd)
                postresult = self.post_url(body, action_data)
                serverinfo = postresult.json(encoding="UTF-8")
            try:
                status = int(serverinfo['status'])
                if status == 1 or status == 0:
                    return serverinfo
                elif status == 101:
                    #有准备锁，进行解锁
                    resutl = self.unlock(self.lockpwd)
                    if resutl['status'] == -1:
                        #解锁失败
                        return False
                    else:
                        #解锁后重新调用一次
                        self.action(body=0, **kwargs)
                else:
                    try:
                        self.log.error(serverinfo['msg'])
                    except KeyError as e:
                        self.log.error(serverinfo['message'])
            except Exception as e:
                pass
            return serverinfo
        except Exception as e:
            self.log.error('请求异常')