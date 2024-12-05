#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/9/17 10:28
# @Author  : xingyue
# @File    : caikuang.py


import  time,threading
import os,json


from task.hjsg import Hjsg,MyLog
import logging
import traceback

class task(Hjsg):
    def getstar_level(self):
        mine = self.action(c='mine', m='single_index')
        p_level = int(mine['p_level'])
        if  19 <= p_level :
            star_level = 5
        elif 16 <= p_level < 19:
            star_level = 4
        elif 11 <= p_level < 16:
            star_level = 3
        elif 6 <= p_level < 11:
            star_level = 2
        else:
            star_level = 1
        return star_level
    def index(self,star_level=1,p=1):
        formdata = {
            "star_level":star_level,
            "p":p,
        }
        mineinfo = self.action(c='mine', m='single_mine_fix',body=formdata)
        return mineinfo
    def caikuang(self):
        star_level =  self.getstar_level()
        for i in range(star_level,1,-1):
            #采矿竞争不激烈，可以从最高位置开始
            mineinfo = self.index(star_level=star_level)
            dateline = mineinfo['dateline']
            log = mineinfo['log']
            if log:
                log_dateline = log['dateline']
                lasttime = int(dateline) - int(log_dateline)
                if lasttime > 14400:
                    self.log.info('矿满了准备收矿')
                    result  = self.action(c='mine', m='get_silver', s=mineinfo['log']['site'])
                    if result['status'] == 1 or result['status'] == 2:
                        self.log.info('矿收获成功，继续采矿')
                        mineinfo = mineinfo['list']
                        for l in mineinfo:
                            if l['status'] == 0:
                                status = self.action(c='mine', m='single_caikuang', star_level=star_level,p=l['page'], id=l['id'], t=l['type'])
                                if status:
                                    self.log.info('采矿成功')
                                    return  True
                                else:
                                    self.log.info('采矿失败')
                    else:
                        self.log.info('矿收货失败')
                        return False
                elif 14400-lasttime < 60:
                    self.log.info("正在开采中,等待%ss," % (14400 - lasttime))
                    time.sleep(14400-lasttime+1)
                    result = self.action(c='mine', m='get_silver', s=mineinfo['log']['site'])
                    if result['status'] == 1:
                        self.log.info('矿收获成功，继续采矿')
                        mineinfo = mineinfo['list']
                        for l in mineinfo:
                            if l['status'] == 0:
                                status = self.action(c='mine', m='single_caikuang', star_level=star_level, p=l['page'],
                                                     id=l['id'], t=l['type'])
                                if status:
                                    self.log.info('采矿成功')
                                    return True
                                else:
                                    self.log.info('采矿失败')
                else:
                    self.log.info("正在开采中,剩余%ss," % (14400 - lasttime))
                    return False
            else:
                mineinfo = mineinfo['list']
                for l in mineinfo:
                    if l['status'] == 0:
                        status = self.action(c='mine', m='single_caikuang',star_level=star_level, p=l['page'], id=l['id'], t=l['type'])
                        if status:
                            self.log.info('采矿成功')
                            return True
                        else:
                            self.log.info('采矿失败')
                            return False

if __name__ == '__main__':

    def act(user,apass,addr):
        log = MyLog(logname='caikuang.log', level=logging.INFO)
        log.filter_.username = user
        log.filter_.addr = addr
        action = task(user, apass, addr, log)
        action.caikuang()
    filepath = os.path.dirname(os.path.abspath(__file__))
    cont = ['autocaikuang.txt','21user.txt']
    for t in cont:
        with open('%s/users/%s'%(filepath,t),'r') as f:
            for i in f:
                if i.strip():
                    name = i.split()[0]
                    passwd = i.split()[1]
                    addr = i.split()[2]
                    t1 = threading.Thread(target=act, args=(name,passwd,addr))
                    t1.start()
