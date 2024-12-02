#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/9/10 10:37
# @Author  : xingyue
# @File    : task.py
#群雄争霸


from task.base import SaoDangFb
import time, threading
import os, json
from Queue import Queue
from huodong.meirihuodong import jaderabbit_receivespring
from task.hjsg import Hjsg,MyLog
import logging
import traceback



class task(Hjsg,jaderabbit_receivespring):

    def qiandao(self):  # 签到
        try:
            self.log.info('每日签到')
            # 领取连续登陆15天奖励，id:15，c:logined，m:get_reward
            self.action(c='logined', m='index')
            self.action(c='logined', m='get_reward', id=15)
            # 每日签到，所有动作就是c内容，m动作参数即可，包括领取vip工资，还有每日抽奖
            self.action(c='sign', m='sign_index')
            # c:vipwage，m:get_vip_wage，领取VIP每日奖励
            self.action(c='vipwage', m='get_vip_wage')
        except Exception as e:
            traceback.print_exc()
            self.log.error('玉兔迎春首页异常' + traceback.format_exc())
            return False
    def take_reward(self,id=1):  # 签到
        try:
            formdata ={
                "id":id
            }

            self.log.info('领取奖励')
            # 领取连续登陆15天奖励，id:15，c:logined，m:get_reward
            self.action(c='hero_fight', m='take_reward',body=formdata)

        except Exception as e:
            traceback.print_exc()
            self.log.error('玉兔迎春首页异常' + traceback.format_exc())
            return False

def run(user, apass, addr,pwd):
    log = MyLog(logname='task.log', level=logging.INFO)
    log.filter_.username = user
    log.filter_.addr = addr
    action = task(user, apass, addr,log)
    activity = action.get_act()
    level = action.level()
    if level > 169:
        action.take_reward()
if __name__ == '__main__':
    q = Queue()
    filepath = os.path.dirname(os.path.abspath(__file__))
    # cont = ['user.txt','21user.txt','autouser.txt','alluser.txt','gmhy.txt','gmhy147.txt','wunianjihua.txt','burenshi.txt']
    cont = ['xing.py']
    for t in cont:
        with open('%s/users/%s' % (filepath, t), 'r') as f:
            for i in f:
                if i.strip() and not i.startswith('#'):
                    name = i.split()[0]
                    passwd = i.split()[1]
                    addr = i.split()[2]
                    try:
                        lockpwd = i.split()[3]
                    except:
                        lockpwd = None
                    t1 = threading.Thread(target=run, args=(name, passwd, addr,lockpwd))
                    q.put(t1)
    while not q.empty():
        thread = []
        for i in xrange(5):
            try:
                thread.append(q.get_nowait())
            except Exception as e:
                print e
        for i in thread:
            i.start()
        for i in thread:
            i.join()