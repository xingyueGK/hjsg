#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/9/17 18:27
# @Author  : xingyue
# @File    : test.py


def condition():
    # level 3 ['神黄权','神陆抗'] [['神卢植','神刘璋'],['神文丑','神董卓']]
    a = ['神黄权', '神陆抗']
    b = [['神卢植', '神刘璋'], ['神文丑', '神董卓']]
    condition = [(i, k[0], k[1]) for i in a for k in b]


    # genral_info = self.matrix()
    # for k, v in genral_info.items():
    #     pass
#
# condition()
# y = set(['h', 'a','c', 'm',1])
# z= set(['a', 'h', 'm','c','a'])


import redis
import datetime
import time

# a = "2018-10-10 23:40:00"
#
# import time
# timeArray = time.strptime(a, "%Y-%m-%d %H:%M:%S")
#
# timeStamp = int(time.mktime(timeArray))
# print timeStamp
#
# pool=redis.ConnectionPool(host='127.0.0.1',port=6379,db=0)
# r = redis.StrictRedis(connection_pool=pool)
#
# print r.expireat('231', timeStamp)
def a():
    a = 12
    def b():
        print a
        return a
    return b

a()()