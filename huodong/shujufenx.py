# -*- coding:utf-8 -*-
from __future__ import unicode_literals
from task.base import SaoDangFb
import time, threading
import os, json, sys


reload(sys)
sys.setdefaultencoding('utf-8')


class fuben(SaoDangFb):
    def level(self):
        level = self.action(c='member', m='index')
        levelinfo = int(level['level'])
        return levelinfo

    def muster(self, level=40):  # 添加武将并出征
        # gid武将id，pid那个槽位训练获取
        caiid = ''
        liaoid = ''
        gid = ''
        practtice_info = self.action(c='practice', m='index')
        # 初期都是两个训练槽位，
        pid = practtice_info['place']['1']['id']
        self.action(c='practice', m='practice_stop ', pid=pid)  # 终止训练
        # 获取武将
        self.action(c='levelgift', m='index')
        wujiang_index = self.action(c='muster', m='index', page=1, perpage=999)['list']
        for k, v in wujiang_index.items():
            if v['name'] == '蔡文姬':  # 蔡文姬
                print '蔡文姬出征'
                self.action(c='muster', m='go_battle', gid=v['id'])
                self.action(c='matrix', m='index')
                caiid = v['id']
            elif v['name'] == '廖化':
                self.action(c='muster', m='go_battle', gid=v['id'])
                liaoid = v['id']
            elif v['name'] == '张昭':
                print '找到张昭'
                gid = v['id']
        lists = '0,%s,0,%s,0,0,0,0,0' % (gid, caiid)
        status = self.action(c='matrix', m='update_matrix', list=lists, mid=1)
        if status
        # 队武将突飞
        index_info = self.action(c='practice', m='index')
        # 训练武将，
        formdata = {
            "gid":gid,
            "pid":pid,
            "type":2
        }
        status = self.action(c='practice', m='practice_start', body=formdata)
        if status:
            print '开始训练'
        for k,v in index_info['list'].items():
            if v['name'] == '蔡文姬':
                freetimes = index_info['freetimes']  # 突飞卡
                isturn = index_info['list'][k]['isturn']  # 武将师是否到转生级别
                wjlevel = index_info['list'][k]['level']
                print '武将等级', wjlevel
                status = 1
                while status == 1 and freetimes != 0:  # 队伍将进行突飞
                    if int(isturn) == 1 and int(wjlevel) <= level:
                        print '武将转生'
                        print self.action(c='practice', m='turn', gid=gid)
                    self.action(c='practice', m='mop', times=100, gid=gid)
                    self.action(c='practice', m='mop', times=50, gid=gid)
                    self.action(c='practice', m='mop', times=10, gid=gid)
                    self.action(c='practice', m='mop', times=5, gid=gid)
                    index_info = self.action(c='practice', m='index')
                    freetimes = index_info['freetimes']
                    info = self.action(c='practice', m='go_leap', gid=gid)  # 武将突飞一次
                    status = info['status']

    def tufei(self, name, level):  # 对武将突飞
        try:
            gid = ''
            practtice_info = self.action(c='practice', m='index')
            # 初期都是两个训练槽位，
            pid = practtice_info['place']['1']['id']
            self.action(c='practice', m='practice_stop ', pid=pid)  # 终止训练
            wujiang_index = self.action(c='muster', m='index', page=1, perpage=999)['list']
            for k, v in wujiang_index.items():
                if v['name'] == name:  # 蔡文姬
                    print u'武将出征', name
                    result = self.action(c='muster', m='go_battle', gid=v['id'])
                    print result['status']
                    gid = v['id']
            status = 1
            index_info = self.action(c='practice', m='index')
            # 训练武将，
            self.action(c='practice', m='practice_start', gid=gid, pid=pid, type=2)
            freetimes = index_info['freetimes']  # 突飞卡
            for k, v in index_info['list'].items():
                if v['name'] == name:
                    isturn = v['isturn']  # 武将师是否到转生级别
                    wjlevel = v['level']
            print '武将等级', wjlevel
            print freetimes
            while status == 1 and freetimes != '0':  # 队伍将进行突飞
                print '武将突飞'
                if int(isturn) == 1 and int(wjlevel) <= level:
                    print '武将转生'
                    self.action(c='practice', m='turn', gid=gid)
                self.action(c='practice', m='mop', times=100, gid=gid)
                self.action(c='practice', m='mop', times=50, gid=gid)
                self.action(c='practice', m='mop', times=10, gid=gid)
                self.action(c='practice', m='mop', times=5, gid=gid)
                index_info = self.action(c='practice', m='index')
                freetimes = index_info['freetimes']
                info = self.action(c='practice', m='go_leap', gid=gid)  # 武将突飞一次
                status = info['status']

        except:
            pass

    def mapscene(self,level):  # 领取通关奖励
        self.action(c='map', m='get_scene_list', l=level, v=2018071801)
        self.action(c='map', m='get_newreward_index', levelid=1, v=2018071801)
        self.action(c='map', m='get_newreward', id=1, v=2018071801)
        self.action(c='map', m='get_newreward', id=2, v=2018071801)
        self.action(c='map', m='get_newreward', id=3, v=2018071801)
        self.action(c='map', m='get_newreward', id=4, v=2018071801)

    def zhengshou(self):  # 征收
        cishu = self.action(c='city', m='index')  # 获取银币征收次数,m=impose,执行征收
        cishu_count = cishu['times']
        if cishu_count != '0':  # 判断征收次数是否为0，不为0则进行全部征收
            for count in range(1, int(cishu_count) + 1):
                print '开始征收第 %d 次' % count
                time.sleep(0.5)
                self.action(c='city', m='impose')
        else:
            print '次数为0次'

    def join(self):  # 申请加入你是学姐国家
        # print self.action(c='country', m='search', name='%E6%98%AF%E4%BD%A0%E5%AD%A6%E5%A7%90')
        print self.action(c='country', m='apply', id=14900000000360, page=1)



    def general(self, tpye=1):  # 获取武将id和装备id,并返回输入获取的等级
        # 装备信息栏
        info = self.action(c='general', m='index')
        gid = info['list']['1']['id']  # 武将id
        etype1 = self.action(c='general', m='get_info', gid=gid, etype=1)['equipments']
        etype3 = self.action(c='general', m='get_info', gid=gid, etype=3)['equipments']  # 获取披风
        etype2 = self.action(c='general', m='get_info', gid=gid, etype=2)['equipments']  # 获取铠甲
        etype4 = self.action(c='general', m='get_info', gid=gid, etype=4)['equipments']
        eid = []  # 装备列表
        if info['list']['1']['eid1'] == 0 or info['list']['1']['eid1'] == "0":
            #判断是否穿戴装备
            if etype1:
                equipments1 = sorted(etype1.items(), key=lambda etype: etype[0])
                eid.append({"1": equipments1[0][1]['id']})  # 第一个就就是最好的装备
        else:
            eid.append({"1":info['list']['1']['eid1']['id']})
        if info['list']['1']['eid2'] == 0 or info['list']['1']['eid2'] == "0":
            if etype2:
                equipments2 = sorted(etype2.items(), key=lambda etype: etype[0])
                eid.append({"2": equipments2[0][1]['id']})
        else:
            eid.append({"2":info['list']['1']['eid2']['id']})
        if info['list']['1']['eid3'] == 0 or info['list']['1']['eid3'] == "0":
            if etype3:
                equipments3 = sorted(etype3.items(), key=lambda etype: etype[0])
                eid.append({"3": equipments3[0][1]['id']})
        else:
            eid.append({"3":info['list']['1']['eid3']['id']})
        if info['list']['1']['eid4'] == 0 or info['list']['1']['eid4'] == "0":
            if etype4:
                equipments4 = sorted(etype4.items(), key=lambda etype: etype[0])
                eid.append({"4": equipments4[0][1]['id']})
        else:
            eid.append({"4":info['list']['1']['eid4']['id']})

        return gid, eid

    def get_general(self):  # 获取武将信息
        general_index = self.action(c='general', m='index')
        return general_index

    def strengthen(self, id):  # 强化装备
        levelinfo = self.level()

        self.action(c='general', m='index')
        self.action(c='strengthen', m='index')
        id_info = self.action(c='strengthen', m='strengthen_info', id=id)
        newlevel = id_info['info']['level']  # 获取当前装备的强化等级
        print '当前等级', newlevel
        try:
            while int(newlevel) < levelinfo:
                strenthinfo = self.action(c='strengthen', m='strengthen_start', id=id, ratetype=0)
                newlevel = strenthinfo['newlevel']
                print '强化等级', newlevel
        except KeyError as e:
            print '已经强化到最高级', newlevel

    def equip(self, gid, eid, etype):  # 给武将穿戴装备
        self.action(c='general', m='equip', gid=gid, eid=eid, etype=etype)
    def unequip(self,gid, eid, etype):
        self.action(c='general', m='unequip', gid=gid, eid=eid, etype=etype,position=etype)
    def levelgift(self):  # 获取等级奖励
        res=self.action(c='levelgift', m='index')  # 打开奖励页面
        for item in res['list']:
            if item['type'] == 1:
                self.action(c='levelgift', m='get_reward', level=item['level'])  # 获取30级奖励

    def saodang(self, missionlevel,missionsite,missionstage,num=13):  # 攻击小兵

        exit_code = 1
        print 'saosang',missionlevel
        if exit_code == 1:
            for level in range(missionlevel, 13):  # 遍历每一个图
                print 'action  %s mission' % level
                result = self.action(c='map', m='get_scene_list', l=level)
                try:
                    site = len(result['list']) + 1
                except KeyError as e:
                    print e
                    self.p(result)
                    return
                for i in range(missionsite, site):  # 遍历关卡图次数
                    print 'site', i
                    status = 1
                    for id in range(missionstage, 11):  # 遍历10个小兵
                        try:
                            # 获取首杀状态，1为首杀，-1为已经击杀
                            first = self.action(c='map', m='mission', l=level, s=i, id=id)['info']['first']
                        except KeyError as e:
                            continue
                        if first == 1 and status == 1:  #
                            status = self.action(c='map', m='action', l=level, s=i, id=id)['status']
                            print status
                            if first == 1 and status == -5:
                                print 'exit'
                                exit_code = 2
                                return exit_code
                        else:
                            print 'alredy kill '
        else:
            print 'dabuduole'
            return

    def act_steadily(self):  # 节节高
        info = self.action(c='act_steadily', m='index')
        status = info['status']
        reward_cd = info['reward_cd']
        t = info['reward']['time']
        if reward_cd == 0 and status == 1:
            self.action(c='act_steadily', m='get_online_reward', t=t)
        elif reward_cd == 0 and status != 1:
            exit(2)
        else:
            print '%s分钟后领取,%s' % (reward_cd / 60, reward_cd)

            time.sleep(reward_cd + 1)
            self.action(c='act_steadily', m='get_online_reward', t=t)

    def morra(self):  # 节节高奖券
        status = 1
        while status == 1:
            info = self.action(c='act_steadily', m='morra', type=1)
            status = info['status']
        # 买突飞卡
        print self.action(c='act_steadily', m='get_score_reward', id=1)

    def mainquest(self):  # 领取所有活动奖励
        mainquest_info = self.action(c='mainquest', m='index')
        print '领奖'
        for i in mainquest_info['list']:
            if int(i['status']) == 1:  # 获取奖励
                self.action(c='mainquest', m='get_task_reward', id=i['task_id'])
                print '领取奖励', i['task_id']

    def qiandao(self):  # 签到
        # 领取连续登陆15天奖励，id:15，c:logined，m:get_reward
        print self.action(c='logined', m='index')

        print self.action(c='logined', m='get_reward', id=15)
        # 每日签到，所有动作就是c内容，m动作参数即可，包括领取vip工资，还有每日抽奖
        self.action(c='sign', m='sign_index')
        # c:vipwage，m:get_vip_wage，领取VIP每日奖励
        self.action(c='vipwage', m='get_vip_wage')

    def soul(self):  # 武将将魂
        site = [1, 2, 3, 4]
        sid = []
        gid = ''
        soulindex = self.action(c='soul', m='index')
        for i in soulindex['pack']['list']:
            sid.append(int(i['id']))
        for k, v in soulindex['general'].items():
            if v['name'] == '张昭':
                gid = int(v['id'])
        for i in range(4):
            self.action(c='soul', m='equip', gid=gid, sid=sid[i], site=site[i])

    def tujian(self, user):  # 图鉴
        result = self.action(c='equip_book', m='get_level_up', id=75)  # 橙装策防
        resultwf = self.action(c='equip_book', m='get_level_up', id=74)  # 橙装物防

        print '账号', user, '披风等级', result['now']['level'], '铠甲等级', resultwf['now']['level']
        if result['now']['level'] < "8":
            print '升级图鉴'
            self.action(c='equip_book', m='level_up', id=75)  # 升级图鉴
        if resultwf['now']['level'] < "8":
            self.action(c='equip_book', m='level_up', id=74)  # 升级图鉴

    def mingjiang(self):  # 升级张昭成就
        self.action(c='general_book', m='index', perpage=999)
        self.action(c='general_book', m='get_achievement_list', v=2018071801)
        self.action(c='general_book', m='levelup', id=176, v=2018071801)

    def zuoji(self):  # 首次购买坐骑并穿戴
        self.action(c='studfarm', m='action', new=1, id=3)
        pass

    def mapinfo(self):
        memberindex = self.action(c='member', m='index')
        missionlevel = memberindex['missionlevel']  # 当前势力
        missionsite = memberindex['missionsite']  # 有多少个关卡
        missionstage = memberindex['missionstage']  # 当前关卡
        print '第 %s 个图，%s 节点 ' % (missionlevel, missionstage)
        # print json.dumps(self.action(c='map', m='get_scene_list', l=missionlevel))

    def lottery(self):  # 每日抽奖
        # c=lottery，m=action
        # 获取每日抽奖次数
        self.numbers = self.action(c='lottery', m='index')['log']['info']['total_num']
        print '开始抽奖，剩余次数 %s' % self.numbers
        for num in range(self.numbers):
            self.action(c='lottery', m='action')
        print '抽奖结束'
    def discount_carnival(self):
        self.action(c='discount_carnival',m='sign_index')
        cash_cow_index=self.action(c='discount_carnival',m='cash_cow_index')
        shake_num = cash_cow_index['shake_num']
        fordata = {
            "num":shake_num
        }
        cash_cow_index = self.action(c='discount_carnival', m='shake',body=fordata)

if __name__ == '__main__':
    def act(user, apass, addr):
        action = fuben(user, apass, addr)
        if action.level() <170:
            action.saodang(25)


    with open('../users/haiyun.txt', 'r') as f:
        for i in f:
            if i.strip() and not i.startswith('#'):
                str = i.strip().split()[0]
                name = str
                passwd = i.strip().split()[1]
                addr = i.strip().split()[2]
                t1 = threading.Thread(target=act, args=(name, passwd, addr))
                t1.start()
                time.sleep(0.1)
