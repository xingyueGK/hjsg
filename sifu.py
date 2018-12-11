#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/11/7 17:53
# @Author  : xingyue
# @File    : sifu.py

import requests
import time
import json
import  sys
import  redis
reload(sys)
sys.setdefaultencoding('utf-8')
headers = {
    'Accept-Encoding':'gzip, deflate',
    'Accept-Language':'zh-CN,zh;q=0.8',
    'Connection':'keep-alive',
    'Upgrade-Insecure-Requests':'1',
    'Content-Type':'application/json',
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'
}

class TokenErr(Exception):
    pass


class SaoDangFb(object):
    def  __init__(self,user,passwd,num):
        #随机请求参数
        self.num = num
        self.user = user
        self.passwd = passwd
        self.rand = int(time.time()*1000)
        self.token_uid = '210000353508'
        self.token = self.get_token(self.num, self.user, self.passwd)
        #POST基础URL地址
        self.url = 'http://s{0}.game.shaline8.com:8101/index.php?v=0&channel=150&lang=zh-cn&token={1}&token_uid={2}&rand={3}&'.format(self.num,self.token,self.token_uid,self.rand)
    @staticmethod
    def get_token(num, user, passwd):
        url = 'http://s{num}.game.shaline8.com:8101/index.php?c=login&&m=user&u={user}&p={passwd}&v=2018083101&token=&channel=11&lang=zh-cn&rand=150959405499450'.format(
            num=num, user=user, passwd=passwd)
        pool = redis.ConnectionPool(host='localhost', port=6379,db=0)
        _redis = redis.StrictRedis(connection_pool=pool)
        try:
            if _redis.hget(num,user):
                token = _redis.hget(num,user)
                login = 'http://s{num}.game.shaline8.com:8101/index.php?c=member&m=index&v=0&token={token}&channel=150&lang=zh-cn&rand=150959405499450'.format(
                    num=num, token=token)
                r = requests.get(login)
                if r.text == '403':
                    raise TokenErr('token expire')
                else:
                    return token
            else:
                raise TokenErr('token expire')
        except TokenErr:
                try:
                    result= requests.get(url).json()
                    if result['status'] == 1:
                        token = result['token']
                        _redis.hset(num,user,token)
                        return token
                    else:
                        print user,'账号密码不对'
                        exit(2)
                except Exception as e:
                    print e

    def post_url(self,data):
        self.data = ''
        for k,v in data.items():
            self.data += '&%s=%s'%(k,v)
        self.url = 'http://s%s.game.shaline8.com:8101/index.php?%s&v=2017111501&v=2017111501&channel=11&imei=NoDeviceId&platform=android&lang=zh-cn&token=%s&token_uid=%s&rand=%s' % (
            self.num, self.data, self.token, self.token_uid, self.rand)
        keep_request = True
        while keep_request:
            try:
                r = requests.post(self.url,headers=headers,timeout=20)
                keep_request = False
                if r.status_code != 200:
                    r = requests.post(self.url, headers=headers,timeout=20)
                    return r.json(encoding="UTF-8")
                else:
                    return r.json( encoding="UTF-8")
            except Exception as e:
                print e
                time.sleep(0.3)
    def action(self,**kwargs):
        """动作参数m={'index':'获取基础账号密码等信息',‘get_monster_list’：“获取副本怪物列表信息”}
        """
        action_data = kwargs
        serverinfo = self.post_url(action_data)
        return serverinfo
    def saodang(self, num=12):  # 攻击小兵
        memberindex = self.action(c='member', m='index')
        missionlevel = int(memberindex['missionlevel'])
        missionsite = int(memberindex['missionsite'])
        missionstage = int(memberindex['missionstage'])
        map = self.action(c='map', m='get_mission_list')
        exit_code = 1
        if exit_code == 1:
            for level in range(missionlevel, num):  # 遍历每一个图
                print '开始攻击第 %s 个图' % level
                self.action(c='map', m='get_scene_list', l=level)

                site = len(self.action(c='map', m='get_scene_list', l=level)['list']) + 1
                for i in range(missionstage, site):  # 遍历关卡图次数
                    print '关卡', i
                    status = 1
                    for id in range(1, 11):  # 遍历10个小兵
                        try:
                            # 获取首杀状态，1为首杀，-1为已经击杀
                            first = self.action(c='map', m='mission', l=level, s=i, id=id)['info']['first']
                        except KeyError as e:
                            continue
                        if first == 1 and status == 1:  #
                            status = self.action(c='map', m='action', l=level, s=i, id=id)['status']
                            print status
                            if first == 1 and status == -5:
                                print '退出'
                                exit_code = 2
                                return exit_code
                        else:
                            print '已经击杀'
        else:
            print 'dabuduole'
            return
if __name__ == '__main__':
    action = SaoDangFb('jinlaikankan','12345678',1)
    action.saodang(12)
