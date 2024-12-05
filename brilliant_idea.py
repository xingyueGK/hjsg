#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/9/26 13:55
# @Author  : xingyue
# @File    : country_celery.py

#锦囊妙计
from task.base import SaoDangFb
from utils import mylog
import datetime
import traceback
import logging
log = mylog.MyLog(logname='jinnang.log',level=logging.DEBUG)
import os,threading
from Queue import Queue

class brilliant_idea(SaoDangFb):
    def index(self):
        index = self.action(c='brilliant_idea',m='index')
        return index

    def pick(self,dispatch_id):
        formdata= {
            "dispatch_id":dispatch_id
        }
        index = self.action(c='brilliant_idea', m='pick',body=formdata)
        return index

    def support(self, duty_id):

        index = self.action(c='brilliant_idea', m='support', duty_id=duty_id)
        return index
    def autopick(self):
        index = self.index()
        #领取奖励
        try :
            #个人
            log.info('领取个人奖励')
            individual = index['list']['individual']
            for item in individual:
                if item.has_key('dispatch_cd') :
                    if int(item['dispatch_cd']) == 0:
                        log.info('准备领取%s' % item['name'])
                        formdata = {
                            "dispatch_id": item['dispatch_id']
                        }
                        status = self.action(c='brilliant_idea', m='pick',body=formdata)
                        if status['status'] ==1:
                            log.info('领取%s成功'%item['name'])
                        else:
                            log.info('领取失败%s'%self.p(status))
            #团队team
            team = index['list']['team']
            log.info('领取团队奖励')
            for item in team:
                if item.has_key('dispatch_cd'):
                    if int(item['dispatch_cd']) == 0:
                        log.info('准备领取%s'%item['name'])
                        formdata = {
                            "dispatch_id": item['dispatch_id']
                        }
                        status= self.action(c='brilliant_idea', m='pick', body=formdata)
                        if status['status'] ==1:
                            log.info('领取%s成功'%item['name'])
                        else:
                            log.info('领取失败%s'%self.p(status))
        except KeyError as e:
            log.error(e)
            print e


    def dispatch_preview(self,duty_id):
        resurl = self.action(c='brilliant_idea', m='dispatch_preview', duty_id=duty_id)
        return resurl

    def renovate(self,idea_type=1):
        #刷新
        formdata = {
            "idea_type": idea_type,
        }
        resurl = self.action(c='brilliant_idea', m='renovate', body=formdata)
        return resurl
    def dispatch(self,idea_type,duty_id,gid1,gid2,gid3):
        #个人
        formdata = {
            "idea_type": idea_type,
            "duty_id": duty_id,
            "gid1": gid1,
            "gid2": gid2,
            "gid3": gid3,
        }
        resurl = self.action(c='brilliant_idea', m='dispatch', body=formdata)
        return resurl
    def team_dispatch(self,idea_type,duty_id,gid1,gid2,support_uid,support_gid):
        #团队
        formdata = {
            "idea_type": 2,
            "duty_id": duty_id,
            "gid1": gid1,
            "gid2": gid2,
            "support_uid":support_uid,
            "support_gid":support_gid
        }
        log.debug('team_dispatch_formdata %s'%formdata)
        resurl = self.action(c='brilliant_idea', m='dispatch', body=formdata)
        return resurl
    def auto_dispatch(self):
        log.info('打开锦囊首页')
        index = self.index()
        try:
            list= index['list']
            #个人锦囊
            individual = list['individual']
            quality_num = 0
            #统计当前任务有多少白色任务，如果都是白色的任务就刷新一下任务
            for item in individual:
                quality =int(item['quality'])
                if quality ==1:
                    quality_num+=1
            if quality_num ==6 :
                self.renovate(idea_type=1)
            for item in individual:
                if item.has_key('dispatch_cd'):
                    #已经被派遣
                    t=str(datetime.timedelta(seconds=item['dispatch_cd']))
                    name = item['name']
                    log.info('个人锦囊任务 %s剩余时间%s'%(name,t))
                else:
                    #
                    pr=self.dispatch_preview(item['id'])
                    #派遣条件
                    condition = pr['duty_info']['condition']
                    name = pr['duty_info']['name']
                    log.info("个人锦囊任务：%s,派遣条件:%s"%(name,condition))
                    #魔将列表
                    devil = pr['list']['devil']
                    #遍历所有魔将，查看是否有符合要求的
                    dispatch_flag=False #表示未成功派遣
                    for i in devil:
                        if i['name'] == condition:
                            r = self.dispatch(item['quality'],item['id'],gid1=i['generalid'],gid2='undefined',gid3='undefined')
                            if r['status'] ==1:
                                log.info('个人锦囊任务：%s,派遣成功'%name)
                                dispatch_flag=True
                    # 一战列表
                    famous =pr['list']['famous']
                    if not dispatch_flag:
                        for f in famous:
                            if f['name'] == condition:
                                r = self.dispatch(item['quality'], item['id'], gid1=f['generalid'], gid2='undefined',
                                              gid3='undefined')
                                if r['status'] == 1:
                                    log.info('个人锦囊任务：%s,派遣成功' % name)
                                    dispatch_flag = True

            # 团队锦囊
            team = list['team']
            quality_num = 0
            # 统计当前任务有多少白色任务，如果都是白色的任务就刷新一下任务
            for item in team:
                quality = int(item['quality'])
                if quality == 1:
                    quality_num += 1
            if quality_num == 6:
                log.info('团队锦囊刷新')
                self.renovate(idea_type=2)
            for item in team:
                name = item['name']
                if item.has_key('dispatch_cd'):
                    #已经被派遣
                    t=str(datetime.timedelta(seconds=item['dispatch_cd']))
                    log.info('团队锦囊任务%s 剩余时间%s'%(name,t))
                else:
                    #派遣预览general_name1，general_name2，general_name3
                    pr=self.dispatch_preview(item['id'])
                    #派遣条件
                    condition = pr['duty_info']['condition']
                    log.info("团队锦囊任务%s 派遣条件:%s" % (name, condition))
                    condition_l = condition.split('，')#将领获取有多少个condition: "卧龙诸葛，冢虎仲达"
                    log.info('debud%s'%condition_l)
                    #组成gid列表
                    """
                    general1: "249"
                    general2: "425"
                    general3: "0"
                    """
                    #gl = [pr['duty_info']['general1'],pr['duty_info']['general2'],pr['duty_info']['general3']]

                    if len(condition_l) == 2:#两个英雄的
                        log.info('开始2个英雄团队任务')
                        #任务名字
                        team_name = pr['duty_info']['name']

                        #魔将列表
                        devil = pr['list']['devil']
                        #遍历所有魔将，查看是否有符合要求的
                        dispatch_flag=False #表示未成功派遣
                        gl = [pr['duty_info']['general1'], pr['duty_info']['general2']]
                        log.info('gl%s'%gl)
                        for i in devil:
                            log.debug('if compare->%s:%s'%(i['generalid'],gl))
                            if i['generalid'] in gl:#表示有符合要求的英雄
                                log.info('找到符合英雄')
                                #获取支持列表
                                support = self.support(item['id'])
                                log.debug('support:%s'%support)
                                gid1 = i['generalid']
                                print '11111',gid1
                                print 'remove',gl.remove(gid1)#移除列表里有的英雄，

                                for support_list in support['list']:
                                    if support_list['generalid']== gl[0] :#获取需要支持的英雄
                                        log.info('团队匹配成功')
                                        stauts = self.team_dispatch(item['quality'],item['id'],gid1=i['generalid'],gid2='undefined',
                                                           support_uid=support_list['uid'],support_gid=support_list['generalid'])
                                        dispatch_flag=True
                                        if stauts['status'] ==1:
                                            log.info('%s 派遣成功'%item['name'])
                                            break
                        # 一战列表
                        famous =pr['list']['famous']
                        if not dispatch_flag:
                            for f in famous:
                                if f['generalid'] in gl:  # 表示有符合要求的英雄
                                    log.info('魔将派遣成功')
                                    # 获取支持列表
                                    support = self.support(item['id'])
                                    log.debug('support:%s' % support)
                                    gid1 = f['generalid']
                                    gl.remove(gid1)  # 移除列表里有的英雄，
                                    for support_list in support['list']:
                                        if support_list['generalid'] == gl[0]:  # 获取需要支持的英雄
                                            log.info('开始团队派遣')
                                            s = self.team_dispatch(item['quality'], item['id'], gid1=f['generalid'],
                                                               gid2='undefined',
                                                               support_uid=support_list['uid'],support_gid=support_list['generalid'])
                                            if s['status'] ==1:
                                                log.info('团队任务%s 派遣成功'%team_name)
                                                break
                                            else:
                                                log.info('团队任务%s 派遣失败%s' % (team_name,s))
                    else:#3个英雄的
                        pass
        except Exception as e:
            print 'str(Exception):\t', str(Exception)
            print 'str(e):\t\t', str(e)
            print 'repr(e):\t', repr(e)
            print 'e.message:\t', e.message
            print 'traceback.print_exc():';
            traceback.print_exc()
            log.error(e)
def run(user, apass, addr,lockpwd):
    action = brilliant_idea(user, apass, addr)
    action.autopick()
    action.auto_dispatch()


if __name__ == '__main__':
    q = Queue()
    filepath = os.path.dirname(os.path.abspath(__file__))
    # cont =  ['user.txt','21user.txt','autouser.txt','alluser.txt']
    # cont = ['149cnm.txt', '149dgj.txt', '149gx1.txt', '148gx.txt','149xx.txt',
    #         '149xb.txt', '149lwzs.txt']
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

