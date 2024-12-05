#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/10/31 11:06
# @Author  : xingyue
# @File    : allInOne.py

from base import SaoDangFb
from const import catch_exception
import  time,threading
import os,json

class eight(SaoDangFb):
    def __init__(self, level, user, passwd, num):
        super(eight, self).__init__(user, passwd, num)
        self.level = level
    def muster(self):
        #所有将领数量
        muster=self.action(c='muster', m='index',page= 1,perpage=999)['list']
        return muster
    def reset(self):
        self.action(c='eight_diagram', m='reset_point')
        self.action(c='eight_diagram', m='level_index', level=self.level)  # level：八卦等级，分为1,2,3重

    def eight_index(self):
        print '八卦首页'
        now_level = self.action(c='eight_diagram', m='index')['now_level']
        print 'now_level',now_level
        if now_level == 0: 
            level_index = self.action(c='eight_diagram', m='level_index', level=self.level)
        else:
            level_index = self.action(c='eight_diagram', m='level_index', level=now_level)
        return level_index,now_level

    def pk(self):
        self.action(c='eight_diagram', m='pk', level=self.level)

    @catch_exception
    def matrix(self):
        #出征将领
        genral_dict = {}
        matrix_index = self.action(c='matrix', m='index')
        general = matrix_index['general']
        for k, v in general.items():
            name = v['name']
            genral_dict[name] = v['id']
        return genral_dict

    @catch_exception
    def use_matrix(self, mid=4):
        # boss固定4
        print self.action(c='matrix', m='use_matrix', mid=mid)

    @catch_exception
    def update_matrix(self, uid1, uid2, uid3, uid4, uid5, mid=2):
        genral_info = self.matrix()
        lists2 = '%s,%s,%s,-1,%s,-1,-1,%s,-1' % (
            genral_info[uid1],
            genral_info[uid2],
            genral_info[uid3],
            genral_info[uid4],
            genral_info[uid5],
        )
        lists4 = '%s,-1,%s,-1,%s,-1,%s,-1,%s' % (
            genral_info[uid1],
            genral_info[uid2],
            genral_info[uid3],
            genral_info[uid4],
            genral_info[uid5],
        )
        if mid == 2:
            self.action(c='matrix', m='update_matrix', list=lists2, mid=mid)
        elif mid == 4:
            self.action(c='matrix', m='update_matrix', list=lists4, mid=mid)

    @catch_exception
    def use_case(self,mid=4,case=1):
        formdata = {
            "case": case,
            "mid":mid,
            "token": self.token
        }
        result = self.action(c='matrix',m=self.get__function_name(),body=formdata)
        return  result

    @catch_exception
    def case_index(self,case=1):
        formdata = {
            "case": case,
            "token": self.token
        }
        result = self.action(c='matrix',m=self.get__function_name(),body=formdata)
        return  result

@catch_exception
def run(user,apass, addr,mid,level):
    ei = eight(num=addr, user=user, passwd=apass, level=level)
 #获取当前阵法信息
    matrixcase = ei.get_act()['matrixcase']
    case_index = ei.case_index(case=matrixcase)
    usercase = case_index['case']
    #ei.p(usercase)
    ei.use_matrix(mid)  # 使用固定阵法
    index,now_level = ei.eight_index()
    #ei.p(index)
    reset_times = int(index['reset_times'])
    point = int(index['cost']['point'])
    print '%s 八卦等级 %s 当前位置%s 重置八卦次数%s'%(user,now_level,point,reset_times)
   
    if point == 9 and reset_times == 1:
        ei.reset()
    elif point != 9 and reset_times >= 1:
        for i in range(12):
            index, now_level = ei.eight_index()
            point = index['cost']['point']
            print point
            ei.pk()
    else:
        print '已经通关没有次数了'
        exit(1)
    for i in range(12):
        index, now_level = ei.eight_index()
        point = index['cost']['point']
        print user,point
        ei.pk()
    re = ei.use_case(mid=usercase['mid'],case=usercase['matrixcase'])
    ei.p(re)
   # ei.use_matrix(4)
s1 = threading.Semaphore(3)
def main(user,apass, addr,mid,level):
    try:
        s1.acquire()
        run(user,apass, addr,mid,level)
    finally:
        s1.release()
if __name__ == '__main__':
    filepath = os.path.dirname(os.path.abspath(__file__))
    cont = ['new.txt']#,'alluser.txt']
   # cont = ['jiang.txt']#,'alluser.txt']
    for t in cont:
        with open('%s/users/%s'%(filepath,t),'r') as f:
            for i in f:
                if i.strip() and not i.startswith('#'):
                        name = i.split()[0]
                        passwd = i.split()[1]
                        addr = i.split()[2]
                        mid = i.split()[3]
                        level = i.split()[4]
                        t1 = threading.Thread(target=main, args=(name, passwd, addr,mid,level))
                        t1.start()

