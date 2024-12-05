#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/9/10 10:37
# @Author  : xingyue
# @File    : task.py
import sys

from task.base import SaoDangFb
import time, threading
import os, json
from Queue import Queue
from huodong.meirihuodong import jaderabbit_receivespring,act11th_anniversary_lottery,luck_pk
from task.hjsg import Hjsg,MyLog
import logging
import traceback



class task(Hjsg,jaderabbit_receivespring,act11th_anniversary_lottery,luck_pk):
    def copies(self):
        # 扫荡副本需要传递的参数
        # id 是副本名字id ，self.role_info
        # diff_id是困难级别分别为1,2,3个级别
        # monster_id 是第几个怪物，1-10个，
        # times 扫荡的次数
        try:
            for id in range(1, 4):
                # 遍历三个副本，
                print '开始扫荡副本:%s' % id
                for diff_id in range(1, 4):
                    print '开始扫关卡:%s' % diff_id
                    # 遍历三个难度，普通，困难，英雄
                    # for monster_id in range(1,11): #此选项为攻击所有小怪
                    for monster_id in [3, 6, 9, 10]:  # 攻击精英怪
                        # 遍历十次小兵
                        print  "开始扫荡小兵"
                        try:
                            times = \
                                self.action(c="copies", m="get_monster_info", id=id, diff_id=diff_id,
                                            monster_id=monster_id,
                                            d="newequip")['info']['free_times']
                        except Exception as e:
                            print e
                        if times != '0':
                            self.action(c="copies", m="mop_up", id=id, diff_id=diff_id, monster_id=monster_id,
                                        d="newequip", times=int(times))
        except Exception as e:
            print e

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
            self.log.error('每日签到异常' + traceback.format_exc())
            return False

    def zhengshou(self):  # 征收
        print '征收'
        try:
            cishu = self.action(c='city', m='index')  # 获取银币征收次数,m=impose,执行征收
            cishu_count = cishu['times']
            if cishu_count != '0':  # 判断征收次数是否为0，不为0则进行全部征收
                for count in range(1, int(cishu_count) + 1):
                    print '开始征收第 %d 次' % count
                    time.sleep(0.5)
                    self.action(c='city', m='impose')
            else:
                print '次数为0次'
        except Exception as e:
            traceback.print_exc()
            self.log.error('征收异常' + traceback.format_exc())

    def hitegg(self):  # 砸蛋
        self.log.info('砸蛋')
        try:
            hitegg_cd = self.action(c='hitegg', m='index')  # 获取砸蛋首页面
            for i in range(3):
                cd = hitegg_cd['list'][i]['cd']
                if cd == 0:
                    self.log.info('砸蛋成功')
                    _id = i + 1
                    self.action(c='hitegg', m='hit_egg', id=_id)
                elif 120 > cd > 0:
                    time.sleep(cd)
                    self.log.info('砸蛋成功')
                    _id = i + 1
                    self.action(c='hitegg', m='hit_egg', id=_id)
        except Exception as e:
            traceback.print_exc()
            self.log.error('砸蛋异常' + traceback.format_exc())

    def island(self):  # 金银洞活动
        print '金银洞活动'
        try:
            # 获取当前攻击的次数和金银守护者5的状态，是否为攻击过，如果为1则为可以攻击，为0 则表示不可以
            count = self.action(c='island', m='get_mission', id=85)['info']['act']
            id_open = self.action(c='island', m='index')['list'][4]['openstatus']
            if count <= 10 and id_open != 1:
                for i in range(81, 86):  # 每日共计5次
                    self.action(c='island', m='pk', id=i)  # 共计金银洞
            id_open = self.action(c='island', m='index')['list'][4]['openstatus']
            if count <= 10 and id_open == 1:
                for i in range(5):
                    self.action(c='island', m='pk', id=85)  # 共计通过之后的最高金银洞5次
            else:
                print '今天已经攻击了10次不在攻打'
        except Exception as e:
            print e

    def countryboos(self):  # 国家boss
        now_time = time.strftime('%H:%M:%S')
        if '20:30:00' < now_time < '20:45:00':
            boss_info = self.action(c='countryboss', m='index')
            countdown = boss_info['countdown']
            powerup = boss_info['powerup']
            if powerup != 200:
                for i in range(10):
                    self.action(c='countryboss', m='powerup', gold=0)
            while countdown > 0:
                # 获取boss退出世界
                countdown = boss_info['countdown']
                self.action(c='countryboss', m='battle')
                time.sleep(61)
            if countdown == 0:
                self.action(c='countryboss', m='reward')  # reward领取奖励
        else:
            print '国家boos未开始'

    def worldboss(self):  # 世界boss领取
        # 银币鼓舞
        now_time = time.strftime('%H:%M:%S')
        if '20:00:00' < now_time < '20:15:00':
            boss_info = self.action(c='worldboss', m='index')
            countdown = boss_info['countdown']
            powerup = boss_info['powerup']
            if powerup != 200:
                for i in range(10):
                    self.action(c='worldboss', m='powerup', gold=0)
            while countdown > 0:
                # 获取boss退出世界
                countdown = boss_info['countdown']
                self.action(c='worldboss', m='battle')
                time.sleep(61)
            if countdown == 0:
                self.action(c='worldboss', m='reward')  # reward领取奖励
        else:
            print '世界boos未开始'

    def world_boss(self):
        try:
            self.log.info('攻打世界BOSS')
            result = self.action(c='world_boss',m='index')
            battle_times = int(result['battle_times'])
            self.log.info('现有次数%s'%battle_times)
            if battle_times >0:
                self.action(c='world_boss',m='battle_prepare')
                for i in range(battle_times):
                    action_result = self.action(c='world_boss', m='action')
                    if action_result['status']==1:
                        self.log.info('攻打成功')
                    else:
                        self.log.error(action_result['msg'])
                self.log.info('完成世界BOSS')
                self.action(c='world_boss',m='get_harm_reward')
            else:
                self.log.info('已完成世界BOSS')
                self.action(c='world_boss', m='get_harm_reward')
        except:
            traceback.print_exc()
            self.log.error('世界boos异常' + traceback.format_exc())
    def overseastrade(self):  # 海外贸易
        print '海外贸易'
        try:
            self.action(c='message', m='index')
            self.action(c='overseastrade', m='index')
            # 购买粮食，花费银币的，id=1为粮食，id2-5为花费元宝的玛瑙等
            self.action(c='overseastrade', m='buy_item', id=1)
            # 组队 ，检查是否有对， 有则加入，没有则创建 ，开始贸易
            # 1获取组队列表
            list_country = self.action(c='overseastrade', m='get_list_by_country', p=1)['list']
            if list_country:  # 如果列表不为空，说明有组
                # 自动加组贸易
                for k, v in list_country.items():  # 判断第一个角色有值没有，有责加入第二个，没有则加入第一个#需要time_id
                    if v['member1'] != '0':  # 如果不为0 则说明角色有人，加入另一个，
                        print '加入2'
                        self.id = v['id']
                        self.action(c="overseastrade", m='join_team', id=self.id, place=int(k), site=2, page=1)
                    else:
                        print '加入1'
                        self.id = v['id']
                        self.action(c="overseastrade", m='join_team', id=self.id, place=int(k), site=1, page=1)
                    # print list_country[k]['member1']
            else:
                # 加入贸易队伍，每页有四个框，为place：1-4，每个框有两个位置site:1-2，页数为page:1-10默认为1即可，
                self.action(c="overseastrade", m='join_team', id=0, place=4, site=2, page=1)
        except Exception as e:
            print e

    def lowtower(self):  # 将魂星路
        # 领取每日奖励
        self.log.info('低等级将魂星路')
        try:
            # 领取奖励
            self.action(c='tower', m='reward_info')
            self.action(c='tower', m='get_reward', type=3)
            index = self.action(c='tower', m='get_scene_list')
            for s in index['scene']:
                if s['openstatus'] == 1 and s['killed'] == 0:
                    #最后一个星域
                    scene = s['id']
                    item = self.tower_times = self.action(c='tower', m='get_mission_list', s=scene)
                    times = item['times']
                    for i in range(times):
                        item = self.tower_times = self.action(c='tower', m='get_mission_list', s=scene)
                        now_id = item['now']['id']
                        status = self.action(c='tower', m='pk', id=now_id)
                        times = item['times']
                        if status['status'] != 1 and times > 5:
                            self.action(c='tower', m='mop_up', id=int(now_id) - 1, times=5)
                        else:
                            self.action(c='tower', m='pk', id=int(now_id) - 1)
                    return None
            print '通关'
            scene = len(index['scene'])
            item = self.tower_times = self.action(c='tower', m='get_mission_list', s=scene)
            times = item['times']
            self.action(c='tower', m='get_mopup_price', id=174)
            self.action(c='tower', m='mop_up', id=174, times=times)

        except Exception as e:
            print e

    def tower(self):  # 将魂星路
        # 领取每日奖励
        self.log.info('高等级将魂星路')
        try:
            # 领取奖励
            buylist = [i for i in range(2, 24, 2)]
            result = self.action(c='tower',m='get_price')
            price = int(result['price'])
            if price in buylist:
                for i in  buylist[buylist.index(price):]:
                    self.action(c='tower', m='buy')
            self.action(c='tower', m='reward_info')
            self.action(c='tower', m='get_reward', type=3)
            index = self.action(c='tower', m='get_scene_list')
            for s in index['scene']:
                if s['openstatus'] == 1 and s['killed'] == 0:
                    #最后一个星域,高等级直接扫荡将魂
                    scene = s['id']
                    break
            try:
                item = self.tower_times = self.action(c='tower', m='get_mission_list', s=scene)
            except:
                scene = index['scene'][-1]['id']
                item = self.tower_times = self.action(c='tower', m='get_mission_list', s=scene)
            times = item['times']
            if times > 10:
                times = 10

            for l in item['list']:
                if l['killed'] ==1 and l['type'] == '2':
                    id = l['id']
                    get_mission_info= self.action(c='tower',m='get_mission_info',id=id)
                    try:
                        if get_mission_info['mission']['hero_soul']['name']:
                            break
                        else:
                            continue
                    except:
                        break
            self.action(c='tower', m='mop_up', id=id, times=times)
        except Exception as e:
            print e
    def business(self):  #
        self.log.info('通商')
        try:
            # 获取通商次数
            business_times = self.action(c='business', m='index')['times']
            if business_times>0:
                self.log.info('可用通商次数 %s' % business_times)
                for count in range(business_times):  # 执行通商次数
                    # 每次通商是需要输入通商id
                    self.log.info('开始第 %s 次通商' % count)
                    business_id = self.action(c='business', m='index')['trader'][0]['id']
                    self.action(c='business', m='go_business', id=business_id)
            else:
                self.log.info('已经完成通商')
                return True
            self.log.info('通商完成')
        except Exception as e:
            traceback.print_exc()
            self.log.error('通商异常' + traceback.format_exc())

    def generaltask(self):  # 每日神将之门
        self.log.info('每日神将')
        try:
            info = self.action(c='generaltask', m='index')  # 获取次数
            number = info['number']
            # 默认第一个将领
            gid = info['list'][0]['id']
            self.log.info('开始神将扫荡，共计 %s 次' % number)
            # 怪物id=255
            times = 0
            for count in range(int(number)):
                get_list = self.action(c='generaltask', m='get_list', p=0)
                # 获取当前id
                for i in get_list['list']:
                    if i['open'] == 1 and i['pass'] == 0:
                        id = int(i['id'])
                        status = self.action(type=0, id=id, gid=gid, c='generaltask', m='action')
                        if status != 1 and times < 3:
                            times += 1
                        elif times > 3:
                            id = int(get_list['list'][0]['id']) - 5
                            status = self.action(type=0, id=id, gid=gid, c='generaltask', m='action')
                        break

            self.log.info('神将10次扫荡完毕')
        except Exception as e:
            print e

    def sanctum(self):
        # 每日宝石领奖
        try:
            self.log.info('领取每日宝石奖励')
            self.action(c='sanctum', m='get_reward', type=1, multiple=0)
            index = self.action(c='sanctum', m='index')
            week = self.getWeek()  # 获取日期
            #开启魔域
            moyupasslist = [1,1,1,1,1]
            cmdcurrpasslist = [index['list'][str(i)]['pass'] for i in range(1,6)]

            if moyupasslist == cmdcurrpasslist :#是否开启魔域 1 为开启 0 未开启
                print '魔域开启'
                select_map = self.action(c='sanctum', m='select_map', l=6)
                times = select_map['times']
                all_stage = select_map['all_stage'] #全部通过关卡
                #open 状态 1 需要攻击 2 已打败 3 未开启
                stage = select_map['stage'] #当前关卡
                if all_stage == "1" and times != 0 :
                    # all_stage 为1 表示没有通过任何boss
                    if week == '4':
                        select_map = self.action(c='sanctum', m='select_map', l=1)
                        id = select_map['list'][9]['id']
                        self.action(c='sanctum', m='action', id=id, num=times)
                    elif week != '4':
                        select_map = self.action(c='sanctum', m='select_map', l=3)
                        if select_map['list'][0]['open'] ==1:
                            select_map = self.action(c='sanctum', m='select_map', l=1)
                            id = select_map['list'][8]['id']
                            self.action(c='sanctum', m='action', id=id, num=times)
                        else:
                            for item in select_map['list']:
                                if item['open'] == 1:
                                    id = int(item['id'] -1)
                                    self.action(c='sanctum', m='action', id=id, num=times)
                                    break
                elif all_stage != "1" and times != 0 :
                    if week == '8':
                        select_map = self.action(c='sanctum', m='select_map', l=6,s= int(all_stage) -1)
                        id = select_map['list'][9]['id']
                        self.action(c='sanctum', m='action', id=id, num=times)
                    elif week != '4':
                        select_map = self.action(c='sanctum', m='select_map', l=6)
                        if select_map['list'][0]['open'] ==1:
                            select_map = self.action(c='sanctum', m='select_map', l=6,s= int(all_stage) -1)
                            id = select_map['list'][8]['id']
                            self.action(c='sanctum', m='action', id=id, num=times)
                        else:
                            for item in select_map['list']:
                                if item['open'] == 1:
                                    id = int(item['id'] -1)
                                    self.action(c='sanctum', m='action', id=id, num=times)
                                    break
            else:
                self.log.info('未开启魔域')
                select_map = self.action(c='sanctum', m='select_map', l=1)
                times = select_map['times']
                all_stage = select_map['all_stage']  # 全部通过关卡次数
                if all_stage == "1" and times != 0: #一关没有通过
                    for item in select_map['list']:
                        if item['open'] ==1:
                            id = int(item['id']) -1
                            self.action(c='sanctum', m='action', id=id, num=times)
                            break
                elif all_stage != "1" and times != 0:
                    if week == '4':
                        select_map = self.action(c='sanctum', m='select_map', l=1,s= int(all_stage) -1)
                        id = select_map['list'][9]['id']
                        self.action(c='sanctum', m='action', id=id, num=times)
                    elif week != '4':
                        select_map = self.action(c='sanctum', m='select_map', l=3)
                        if select_map['list'][0]['open'] ==1:
                            # 状态为1表示已经通关到当前位置，
                            select_map = self.action(c='sanctum', m='select_map', l=3,s= int(all_stage) -1)
                            id = select_map['list'][8]['id']
                            self.action(c='sanctum', m='action', id=id, num=times)
                        else:
                            for item in select_map['list']:
                                Index = select_map['list'].index(item)
                                if item['open'] == 1:
                                    id = int(item['id']) -1
                                    self.action(c='sanctum', m='action', id=id, num=times)
                                    return  None
                                elif item['open'] != 1 and Index == 9:
                                    id = int(item['id']) - 1
                                    self.action(c='sanctum', m='action', id=id, num=times)
                                    return None
        except Exception as e:
            traceback.print_exc()
            self.log.error('四象圣域异常' + traceback.format_exc())

    def lottery(self,pwd):  # 每日抽奖
        self.unlock(pwd)
        self.log.info('开始每日元宝抽奖')
        try:
            yuanbao = int(self.get_act()['gold'])
            self.log.info('当前元宝为%s'%yuanbao)
        except:
            pass

        # c=lottery，m=action
        # 获取每日抽奖次数
        #查看是否为元宝抽奖
        #gettype 6 紫色石头 8 突飞卡  1 银币 2 是元宝
        try:
            index = self.action(c='lottery', m='index')
            self.numbers = index['log']['info']['total_num']
            if self.numbers == 0:
                self.log.info('今日已经完成抽奖')
                return True
            if self.numbers >6:#次数不足
                if int(index['list'][0]['gettype']) == 2:
                    self.log.info('当前为元宝抽奖')
                else:
                    self.log.info('不是元宝抽奖，刷新转盘')
                    for i in range(10):#刷新转盘
                        refresh = self.action(c='lottery',m='refresh')
                        if int(refresh['list'][0]['gettype']) == 2:
                            self.log.info('第%d次刷新到元宝'%(i+1))
                            break
            self.log.info('开始抽奖，剩余次数 %s' % self.numbers)
            for num in range(self.numbers):
                self.log.info('第%d次抽奖'%num)
                self.action(c='lottery', m='action')
            self.log.info('抽奖结束')

        except Exception as e:
            self.log.info('每日抽奖错误')
        try:
            time.sleep(0.5)
            newyuanbao = int(self.get_act()['gold'])
            gold = newyuanbao > yuanbao
            if gold:
                self.log.info('本次收益元宝%d'%gold)
            else:
                self.log.info('本次亏损元宝%d'%gold)
        except:
            pass
    def herothrone(self):  # 英雄王座
        self.log.info('英雄王座')
        try:
            vip = self.action(c='member', m='index')['vip']
            if int(vip) < 9:
                status = self.action(c='herothrone', m='index')['status']
                if status != 1:
                    return None
                for i in range(3):
                    self.action(c='herothrone', m='start')  # 开始王座
                    # 攻击:
                    while True:
                        flag = self.action(c='herothrone', m='action')['status']
                        if flag ==1:
                            self.log.info('攻击王座成功')
                        elif flag == -2:
                            self.log.error('攻击王座失败')
                            break
            else:
                self.action(c='herothrone', m='index')
                for i in range(3):
                    self.action(c='herothrone', m='start') # 开始王座
                    self.action(c='herothrone', m='end_battle')
                    self.action(c='herothrone', m='go_back')
        except Exception as e:
            print e

    def mount_stone(self):  # 符石副本
        self.log.info('符石副本')
        try:
            vip = self.action(c='member', m='index')['vip']
            if int(vip) < 9:
                index = self.action(c='mountstone_throne', m='index')
                status = index['status']
                print index
                if status != 1:
                    return None
                for i in range(3):
                    self.action(c='mountstone_throne', m='start')  # 开始王座
                    # 攻击:
                    while True:
                        flag = self.action(c='mountstone_throne', m='action')['status']
                        self.log.info('攻击符石副本')
                        if flag == -2:
                            break
            else:
                self.action(c='mountstone_throne', m='index')
                for i in range(3):
                    self.action(c='mountstone_throne', m='start')  # 开始王座
                    self.action(c='mountstone_throne', m='end_battle')  # 开始王座
                    self.action(c='mountstone_throne', m='go_back')  # 开始王座
        except Exception as e:
            print e

    def workshop(self):  # 玉石收集
        # 收取
        self.log.info('玉石收集')
        for i in range(1, 7):
            try:
                self.action(c='workshop', m='get_reward', s=i)
            except Exception as e:
                print e

    def exploit_tree(self):  # 木材收集
        print '木材收集'
        try:
            # exploit_stone，m:{gather收集,action，采集}site:1,第一个框,有三个
            for i in range(1, 10):
                self.action(c='exploit_tree', m='index')
                self.action(c='exploit_tree', m='gather', site=i)
                self.action(c='exploit_tree', m='action', site=i)
        except Exception as e:
            print e

    def exploit_stone(self):  # 石头收集
        self.log.info('石头收集')
        try:
            # exploit_stone，m:{gather收集,action，采集}site:1,第一个框,有三个
            for i in range(1, 10):
                self.action(c='exploit_stone', m='gather', site=i)
                self.action(c='exploit_stone', m='action', site=i)
        except Exception as e:
            print e

    def heaven(self):  # 通天塔每日奖励和扫荡
        self.log.info('通天塔每日奖励和扫荡')
        # 获取每日奖励
        try:
            index = self.action(c='heaven',m='index')
            id = index['index']
            self.action(c='heaven', m='get_reward')
            self.times = self.action(c='heaven', m='index')['times']
            if self.times:
                self.action(c='heaven', m='mop_up', id=id, times=self.times)
        except Exception as e:
            print e

    def arena(self):  # 每日演武榜
        self.log.info('演武榜')
        try:
            result = self.action(c='arena', m='index')
            if result['status'] ==2:
                self.log.info('领取演武榜积分奖励')
                result= self.action(c='arena', m='get_reward')
                if result['status'] == 1:
                    self.log.info('领取演武榜积分奖励成功')
                else:
                    self.log.info('领取演武榜积分奖励失败')
            else:
                self.log.info('演武榜积分奖励已经领取')
        except Exception as e:
            traceback.print_exc()
            self.log.error('演武榜异常' + traceback.format_exc())

    def zimap(self):  # 获取图片
        # levev:7,11，14是红色sh关卡s:1-9，id:6
        # 扫荡金色以上5-9
        # 获取次数nowmaxtimes
        for level in range(10, 11):  # 遍历每一个图
            # for level in range(14, 17):  # 遍历每一个图红色使用

            print '开始攻击第 %s 个图' % level
            site = len(self.action(c='map', m='get_scene_list', l=level)['list'])

            for i in range(site):  # 遍历关卡图次数
                print '攻击第 %s 个关卡' % (i + 1)
                for id in range(5, 10):  # 遍历5个小兵
                    # for id in range(4,9):#遍历5个小兵红色使用
                    # 判断当前次数是否为0次，如果为0 则不扫荡
                    if level == 8 and id != 4:
                        continue
                    times = self.action(c='map', m='mission', l=level, s=i + 1, id=id)['info']['nowmaxtimes']
                    # times = self.action(c='map', m='mission', l=level, s=i + 1, id=id)['info']['maxtimes']#红色天赋
                    print '剩余扫荡次数 %s' % times
                    if times != 0:
                        # print 'gongji',level,i+1,id,times
                        self.action(c='map', m='action', l=level, s=i + 1, id=id, times=times)

    def hongmap(self):  # 获取图片
        # levev:7,11，14是红色sh关卡s:1-9，id:6
        # 扫荡金色以上5-9
        # 获取次数nowmaxtimes
        # for level in range(8,11):#遍历每一个图
        for level in range(14, 17):  # 遍历每一个图红色使用

            print '开始攻击第 %s 个图' % level
            site = len(self.action(c='map', m='get_scene_list', l=level)['list'])

            for i in range(site):  # 遍历关卡图次数
                print '攻击第 %s 个关卡' % (i + 1)
                # for id in range(5,10):  # 遍历5个小兵
                for id in range(4, 9):  # 遍历5个小兵红色使用
                    # 判断当前次数是否为0次，如果为0 则不扫荡
                    try:
                        self.action(c='map', m='mission', l=level, s=i + 1, id=id)['info']
                    except KeyError:
                        continue

                    times = self.action(c='map', m='mission', l=level, s=i + 1, id=id)['info']['nowmaxtimes']
                    # times = self.action(c='map', m='mission', l=level, s=i + 1, id=id)['info']['maxtimes']#红色天赋
                    print '剩余扫荡次数 %s' % times
                    if times != 0:
                        # print 'gongji',level,i+1,id,times
                        self.action(c='map', m='action', l=level, s=i + 1, id=id, times=times)

    def guyu(self):  # 获取古玉购买
        self.action(c='actguyu', m='reward_index', id=22, num=1)


    def dice(self):  # 国家摇色子
        self.log.info('国家摇色子')
        try:
            #获取上周国家排名奖励
            self.action(c='dice', m='last_week_rank_reward')
            formdata = {
                "type":3
            }
            self.action(c='dice', m='get_last_week_reward',body=formdata)
            formdata2 = {
                "type": 2
            }
            self.action(c='dice', m='get_points_reward',body=formdata2)
            self.action(c='dice', m='get_last_week_reward',body=formdata2)
            formdata1 = {
                "type": 1
            }
            self.action(c='dice', m='get_points_reward',body=formdata1)
            self.action(c='dice', m='get_last_week_reward',body=formdata1)

            index = self.action(c='dice', m='dice_index')
            points = index['now_week']['points']
            times = int(index['now_week']['times'])
            if int(points) > 400:
                self.action(c='dice', m='get_reward', id=2)
            for i in range(times):
                self.action(c='dice', m='shake_dice')#摇色子

            self.action(c='dice', m='shake_dice')

        except Exception as e:
            print e
    def act_steadily(self):  # 节节高
        print '节节高'
        try:
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
            return True
        except Exception as e:
            return False

    def act_sword(self):  # 铸剑
        self.action(c='act_sword', m='start')
        info = self.action(c='act_sword', m='index')
        self.action(c='act_sword', m='get_rank_reward', type=1)
        self.action(c='act_sword', m='get_rank_reward', type=0)
        # print json.dumps(info)
        need_nums = int(info['need_nums'])
        nums = info['nums']
        print need_nums, nums
        # 收获
        if need_nums == nums:
            self.action(c='act_sword', m='index')
            time.sleep(0.5)
            self.action(c='act_sword', m='get_cast_reward')
            time.sleep(0.5)
            self.action(c='act_sword', m='index')
            self.action(c='act_sword', m='start')
        else:  #
            sleep_time = need_nums - int(nums)
            print sleep_time
            time.sleep(sleep_time * 50)
        # print self.action(c='act_sword',m='battle',touid='260000484980')

    def awaken_copy(self):  # 每日
        self.log.info('每日觉醒奖励')
        try:
            formdata= {
                "check":111,
                "times":5,
            }
            index = self.action(c='awaken_copy', m='index')
            index = self.action(c='awaken_copy', m='sweep',body=formdata)
            
            self.action(c='awaken_copy', m='every_reward_index')
            self.action(c='awaken_copy', m='get_every_reward', b=1)
            for item in index['point_info']:
                if item['button'] == 1:
                    check = item['check']
                    break
            # print check
            check_index = self.action(c='awaken_copy', m='check_index', check=check)
            # self.p(check_index)
            unions = [union['union'] for union in check_index['check_info']]
            now_point = int(check_index['info']['now_point'])
            setup = []  # 攻击步长三步为最佳
            points = unicode(len(unions))  # 总共点数
            setup3 = points
            # print '当前关卡 %s 总共点数 %s,最后一步%s 列表 %s'%(check,points,setup3,unions)
            for k in unions[0]:
                k = int(k)
                setup1 = k
                for v in unions[setup1 - 1]:
                    v = int(v)
                    for x in unions[v - 1]:
                        if setup3 in x:
                            setup2 = v
                            setup = [setup1, int(setup2), int(setup3)]
            if now_point in setup:
                current = setup.index(now_point) + 1
                point_list = setup[current:]
            else:
                point_list = setup
            for point in point_list:
                # 补血，battle每次都需要
                self.action(c='awaken_copy', m='save_blood', check=check, point=point)
                status = self.action(c='awaken_copy', m='battle', check=check, point=point)

            result = self.action(c='awaken_copy', m='reset_check')  # 每次打到最后都需要重置


        except Exception as e:
            print e

    def countrymine(self):  # 国家矿
        print '国家矿'
        try:
            mineinfo = self.action(c='countrymine', m='index')
            dateline = mineinfo['dateline']
            log = mineinfo['log']
            if log:
                log_dateline = log['dateline']
                lasttime = int(dateline) - int(log_dateline)
                print lasttime
                for i in range(8, 10):
                    mineinfo = self.action(c='countrymine', m='index', p=i)['list']
                    for l in mineinfo:
                        if l['status'] == 0:
                            self.action(c='countrymine', m='caikuang', p=i, id=l['id'], t=l['type'])
                            break
        except KeyError as e:
            print e, '没有加入国家，或是等级不够'

    def mouth_card(self):
        # 月卡奖励
        self.action(c='month_card', m='get_reward')

    def beauty(self):  # 铜雀台互动
        beatuy = ''
        self.log.info('铜雀台互动')
        try:
            t = self.get_attribute()
            if t == 'wuli':
                beatuy = 5
            else:
                beatuy = 4
            for i in range(3):
                self.action(c='beauty', m='active_action', beauty_id=beatuy, type=1)
        except Exception as e:
            print e

    def country(self):  # 每日国家奖励
        self.log.info('每日国家奖励')
        try:
            self.action(c='country', m='get_member_list')
            self.action(c='country', m='storage')
            status = self.action(c='country', m='get_salary')
            if status['status'] != 1:
                time.sleep(1)
                status = self.action(c='country', m='get_salary')
        except Exception as e:
            print e
    def countrysacrifice(self):  # 每日贡献
        self.log.info('国家每日贡献40')
        try:
            formdata = {
                "id":1
            }
            self.action(c='countrysacrifice', m='sacrifice_index')
            self.action(c='countrysacrifice', m='sacrifice_start',body=formdata)
        except Exception as e:
            print e

    def gongxian(self, num):  # 国家贡献
        self.log.info('国家贡献')
        try:
            result = self.action(c='country', m='get_member_list')
            if result['status'] == 1:
                self.action(c='country', m='storage')
                for i in range(num):
                    self.action(c='country', m='donate', type=1)
        except Exception as e:
            print e

    def cuju(self):  # 蹴鞠首页
        print '蹴鞠'
        try:
            index = self.action(c='act_kemari', m='index')
            for i in index['list']:
                if i['id'] == 2 and i['times'] != 0 and i['cd'] == 0:
                    self.action(c='act_kemari', m='action', type=2)
                elif i['id'] == 1 and i['times'] != 0 and i['cd'] == 0:
                    self.action(c='act_kemari', m='action', type=1)

            endtime = index['time'].split('-')[1]
            current_tiem = time.strftime("%m月%d日")
            if endtime == current_tiem:
                #购买奖券
                result = self.action(c='act_kemari', m='get_lottery')
                lottery_num = result['lottery_num']
                if lottery_num > 80:
                    for id in range(10,15):
                        self.action(c='act_kemari', m='action_lottery', id=id)
                else:
                    for id in range(1,8):
                        self.action(c='act_kemari', m='action_lottery', id=id)
        except Exception as e:
            print e

    def sanguo(self):  # 游历三国活动
        print '游历三国活动'
        try:
            travelindex = self.action(c='act_travel', m='index')  # 获取活动
            details = self.action(c='act_travel', m='action_travel')['details']  # 开始活动
            if travelindex['info']['free'] == 1:
                result = self.action(c='act_travel', m='action_dice')  # 掷骰子
            if travelindex['info']['points'] != 0:
                # #走路顺序list[4,2,3,5,8,9,10,11,12,13,14]
                plain = [1, 4, 2, 3, 5, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 21, 20, 21, 22, 19, 23, 27, 28, 25,
                         26,
                         29,
                         30]
                num = plain.index(int(details['current'])) + 1
                stats = self.action(c='act_travel', m='plain', point=plain[num])
        except Exception as e:
            print e

    def jisi(self):  # 新年活动
        print '新年祭祀'
        try:
            self.action(c='act_spring', m='index')
            index = self.action(c='act_spring', m='sacrifice_index')
            if index['price']['3']['1'] < "50":
                self.action(c='act_spring', m='sacrifice', type=3, resource_type=1)
            if index['price']['1']['1'] < "50":
                self.action(c='act_spring', m='sacrifice', type=1, resource_type=1)
                self.action(c='act_spring', m='sacrifice', type=1, resource_type=2)
            if index['price']['2']['1'] < "50":
                self.action(c='act_spring', m='sacrifice', type=2, resource_type=1)
                self.action(c='act_spring', m='sacrifice', type=2, resource_type=2)
        except Exception as e:
            print e

    def leigu(self):  # 擂鼓
        print '擂鼓'
        try:
            self.action(c='happy_guoqing', m='get_reward', type=1)
        except Exception as e:
            print e

    def chicken(self):
        self.log.info('金鸡')
        try:
            chenk = self.action(c='chicken', m='vip_index', v=2018021101)['reward']
            member = self.action(c='member', m='index')
            vip = member['vip']
            for l in chenk:
                # print vip,l['vip']
                if int(l['vip']) == int(vip):
                    self.action(c='chicken', m='get_vip_reward', id=l['id'])
                    break
        except Exception as e:
            print e

    def holiday(self):
        self.log.info('假日活动')
        try:
            self.action(c='act_holiday', m='index', v=2018021101)
            self.action(c='act_holiday', m='add_login_reward', v=2018021101)
        except Exception as e:
            print e

    def shenshu(self):  # 神树
        try:
            index = self.action(c='sacredtree', m='index')

            if int(index['time']) == 1:
                self.action(c='sacredtree', m='watering', type=1, v=2018021101)
            for i in range(5):
                index = self.action(c='sacredtree', m='index')
                cd = index['cd']
                levelup_exp = int(index['levelup_exp'])
                exp = int(index['exp'])
                if cd < 86400 and levelup_exp < 2000:
                    print '浇水'
                    self.action(c='sacredtree', m='watering', type=1, v=2018021101)
                else:
                    break
        except Exception as e:
            print e

    def yuanxiao(self):
        print '元宵'
        try:
            index = self.action(c='act_lantern', m='index', v=2018021101)
            if index['freetimes'] > 0:
                self.action(c='act_lantern', m='buy', lid=1, mid=1, v=2018021101)
                self.action(c='act_lantern', m='buy', lid=1, mid=2, v=2018021101)
                self.action(c='act_lantern', m='buy', lid=1, mid=3, v=2018021101)
        except Exception as e:
            print e

    def actjubao(self):
        print '聚宝'
        try:
            self.action(c='actjubao', m='index', v=2018042801)
            self.action(c='actjubao', m='action', type=1, v=2018042801)
            self.action(c='actjubao', m='reward_index', v=2018042801)
            self.action(c='actjubao', m='get_reward', id=1, v=2018042801)
        except Exception as e:
            print e

    def years_guard(self):  # 周年守护签到
        print '周年守护签到'
        try:
            self.action(c='years_guard', m='des_index')
            self.action(c='years_guard', m='sign_index')
        except Exception as e:
            print e

    def fukubukuro(self):  # 周年将签到,
        print '周年将签到'
        try:
            self.action(c='fukubukuro', m='index')
            self.action(c='fukubukuro', m='sign', type=1)
            # 合成签到将领
            self.action(c='fukubukuro', m='get_general', gid=360)
        except Exception as e:
            print e

    def drink(self):  # 每日饮酒
        self.log.info('每日饮酒')
        try:
            result= self.action(c='drink', m='index')
            if result['status']==1:
                result_go_drink = self.action(c='drink', m='go_drink', type=1)
            else:
                self.log.error("每日饮酒异常")
        except Exception as e:
            print e

    def gold_time(self):
        print '黄金时刻'
        self.action(c='gold_time', m='index')
        data = self.action(c='gold_time', m='sign_reward')
        for item in data['data']:
            if item['receive_status'] == 1:
                self.action(c='gold_time', m='receive_sign_reward', reward_id=item['id'])

    def assist_card(self):  # 助阵系统
        try:

            rest = self.action(c='assist_card', m='index')
            self.action(c='assist_copy', m='index')
            self.action(c='assist_copy', m='daily_reward_preview')
            self.action(c='assist_copy', m='get_daily_reward', gold_price=0)
            assist_conjure = self.action(c='assist_conjure', m='index')
            if assist_conjure['data']['const']['free_times'] == 1:
                # 每日免费抽奖
                self.action(c='assist_conjure', m='conjure', conjure_type=1)
            rest = self.action(c='assist_copy',m='index')

            t = self.get_attribute()
            if t == 'wuli':
                mission_id = 19
            else:
                mission_id = 23
            #if rest['data']['total_remain_times'] == 15 :
            #    self.action(c='assist_copy',m='sweep',mission_id= mission_id,times=10)
            #    self.action(c='assist_copy', m='sweep', mission_id=mission_id, times=5)
        except Exception:
            pass

    def drugrefresh(self):  # 经脉刷新
        self.action(c='drug', m='refresh')

    def drug(self):  # 经脉
        try:
            print '经脉购买'
            index = self.action(c='drug', m='index')
            shop_index = self.action(c='drug', m='shop_index')
            remain_freetimes = shop_index['remain_freetimes']
            print '%s 剩余刷新次数 %s' % (self.user, remain_freetimes)
            for i in range(remain_freetimes):
                for item in shop_index['list']:
                    # sub_type 为1 使用元宝购买  goods_type 为 82 暂时用不到的金丹 status 为1 是可以购买物品
                    if item['goods_type'] != "82" and item['sub_type'] != "1" and item['status'] == 1:
                        # 购买经脉
                        id = item['id']
                        reward_index = self.action(c='drug', m='reward_index', id=id)
                        if reward_index['status'] != 1:
                            time.sleep(1)
                            self.drug()
                            return
                self.drugrefresh()
        except Exception as e:
            print e

    def lucky_dice(self):  # 幸运骰子
        try:
            index = self.action(c='lucky_dice', m='index')
            free_times = index['free_times']
            print free_times
            for i in range(free_times):
                self.action(c='lucky_dice', m='farkle_dice')
            # 领取奖励
            index = self.action(c='lucky_dice', m='index')
            lucky_reward = index['lucky_reward']
            for item in lucky_reward:
                if item['status'] == 1:
                    id = item['id']
                    self.action(c='lucky_dice', m='get_lucky_reward', id=id)
        except Exception as e:
            print e

    def act_fight(self):  # 征战八方
        try:
            index = self.action(c='act_fight', m='index')
            for item in index['info']:
                if item['status'] == 1:
                    id = item['id']
                    self.action(c='act_fight', m='get_reward', id=id)
        except Exception as e:
            print e

    def break_egg(self):  # 砸金蛋
        try:
            index = self.action(c='break_egg', m='index')
            free_time = int(index['user_info']['free_time'])
            if free_time == 1:
                self.action(c='break_egg', m='go_break', type=1)
        except Exception as e:
            print e

    def japan(self):  # 征战东瀛
        try:
            citydict = {
                "city1": "100.00",
                "city2": "100.00",
                "city3": "100.00",
                "city4": "100.00",
                "city5": "100.00",
                "city6": "100.00",
                "city7": "100.00",
                "city8": "100.00",
            }
            self.action(c='expostulation', m='get_expostulation_by_user')
            japan_index = self.action(c='japan', m='index')
            for k, v in citydict.items():
                if japan_index['progress'][k] != "100.00":
                    cityid = k.split('y')[1]
                    city = self.action(c='japan', m='City', cityid=cityid)
                    counts = city['counts']
                    for k, v in city['instance_progress'].items():
                        if v < 100 and v != 0:
                            bossid = k.split('o')[1]
                            for i in range(counts):
                                print cityid, bossid
                                status = self.action(c='japan', m='pk', cityid=cityid, bossid=bossid)
                                if status != 1:
                                    time.sleep(0.3)
                                    self.japan()
                                    return
        except:
            pass

    def shopping_feast(self):  # 双十一签到
        try:
            self.action(c='shopping_feast', m='index')
            sign_index = self.action(c='shopping_feast', m='sign_index')
            for item in sign_index['reward_list']:
                if item['take_status'] == 1:
                    self.action(c='shopping_feast', m='sign', id=item['id'])
        except Exception as e:
            print e

    def essence_map(self):  # 经脉丹药扫荡
        try:
            result = self.action(c='essence_map', m='go_sweep_medicine', d='newequip')
            #扫荡所有
            # for item in result['list']:
            #     if item['is_open'] != 0 and item['is_going'] != 0:
            #         id = item['id']
            #         for i in item['diff_array_info']:
            #             diff_id = i['diff_id']
            #             self.action(c='essence_map', m='sweep', d='newequip', id=id, diff_id=diff_id, check=1)
            #紧扫荡指定Boss,获取指定资源
            for item in result['list']:
                if item['is_open'] != 0 and item['is_going'] != 0:
                    id = int(item['id'])
                    if id <5:
                       self.action(c='essence_map', m='sweep', d='newequip', id=id, diff_id=3, check=1)
        except Exception as e:
            print e

    def mission(self):
        """
        :return:
        """
        # 扫荡初级战鼓精魂
        # l: 18
        # s:7
        # id [3,6,9,10]
        # diff_id是困难级别分别为1,2,3个级别
        # monster_id 是第几个怪物，1-10个，
        # times 扫荡的次数
        try:
            for s in range(1, 8):
                # 遍历三个副本，
                print '开始扫荡副本:18'
                for id in [3, 6, 9, 10]:  # 攻击精英怪
                    print '开始扫关卡:%s' % s
                    # 遍历三个难度，普通，困难，英雄
                    # for monster_id in range(1,11): #此选项为攻击所有小怪
                    # 遍历十次小兵
                    times = self.action(c="map", m="mission", l=18, s=s, id=id)['info']['nowmaxtimes']
                    if times > 0:
                        print  "开始扫荡小兵"
                        self.action(c="map", m="action", l=18, s=s, id=id, times=int(times))
        except Exception as e:
            print e

    def double_denier(self):
        """双旦活动"""
        try:
            result = self.action(c='double_denier', m='index')
            free_time = result['free_time']
            if free_time > 0:
                formdata = {"num": free_time}
                self.p(self.action(c='double_denier', m='draw', body=formdata))
        except KeyError as e:
            print e

    def loginreward(self):
        """登录签到礼"""
        try:
            index = self.action(c='loginreward', m='index')
            self.action(c='loginreward', m='action_reward',type=1,reward_id=1)
            reward = index['reward']
            for item in reward:
                id = item['id']
                self.action(c='loginreward', m='action_reward', type=2, reward_id=id)
        except:
            pass
    def newyear_act(self):
        """新年活动"""
        #新年签到
        index = self.action(c='newyear_act',m='index')
        reward = index['reward']
        for item in reward:
            if item['status'] == 1:
                sign_day = item['sign_day']
                status = self.action(c='newyear_act',m='get_sign',sign_day=sign_day)
                if status['status'] ==1:
                    print '签到成功'
                    break
                else:
                    print '签到失败'
        #祈福
        bamboo_stick = self.action(c='newyear_act',m='bamboo_stick')
        free = bamboo_stick['free']
        if free == 1:
            self.action(c='newyear_act', m='action',num=1)
        result = self.action(c='newyear_act', m='usual_luck')
        if result['is_get'] == 0:
            chat_index = self.action(c='chat', m='index')
            status  = self.action(c='chat', m='send', message=u'新年快乐')  # 发送消息
            result = self.action(c='newyear_act', m='usual_luck')
            if result['is_get'] ==1:
                self.action(c='newyear_act', m='get_usual_luck')

    def lantern_festival(self):
        #猜灯谜
        try:
            answer = {
                "48":"c","10":"a","42":"a","27":"b","39":"b","5":"d","14":"c",
                "50":"d","47":"c","33":"b","23":"d","45":"b","15":"b","4":"b",
                "18": "c", "35": "d", "12": "b", "29": "c", "41": "b", "20": "b",
                "32": "a", "6": "d", "3": "a", "22": "a", "17": "a", "37": "a",
                "43": "a", "49": "d", "7": "a", "2": "a", "30": "a", "9": "a",
                "46": "b", "21": "c", "31": "b", "16": "d", "25": "b", "13": "d",
                "28": "a", "40": "c", "26": "a", "36": "b", "44": "b", "1": "c",
                "38": "b", "11": "c", "34": "c", "19": "d"
                      }
            for i in range(1,16):
                resutl = self.action(c='lantern_festival',m='question_index',position=i)
                if resutl['status'] != 1:
                    self.p(resutl)
                questiont = resutl['question']
                id = questiont['id']
                anserresutl = self.action(c='lantern_festival', m='answer', position=i,answer=answer[id])
                if anserresutl['is_right'] == 0:
                    self.p(questiont)
            self.action(c='lantern_festival',m='take_answer_reward')
        except:
            pass
    def act_parade(self):
        #沙场点兵
        try:
            index = self.action(c='act_parade',m='index')
            if index['status'] != 1:
                print index['msg']
                return None
            #self.p(index)
            is_free = int(index['is_free'])
            if is_free > 0:
                self.action(c='act_parade', m='action',num=1)
        except KeyError as e:
            print e
    def seven_year(self):
        #每日签到
        self.action(c='seven_year',m='sign_index')
        self.action(c='seven_year',m='sign')
    def cake_index(self):
        #瓜分元宝
        index = self.action(c='seven_year',m='cake_index')
        self.action(c='seven_year',m='join_cake')
    def undercity(self):
        #地下城
        try:
            index = self.action(c='undercity',m='index')
            diff = index['diff_max']
            for i in index['plate_mission']:
                if i['status'] == 0:
                    plate = i['plate']
                    formdata = {
                        "plate":plate,
                        "diff":diff
                    }
                    plate = self.action(c='undercity',m='plate',body=formdata)
                    times = int(plate['times'])
                    for item in plate['plate_mission']:
                        if item['status'] == 0:
                            id = int(item['id'])
                            sweep_show = self.action(c='undercity', m='sweep_show', id=id - 1)
                            self.p(sweep_show)
                            #type 1 就是扫荡5次，2就是10次，3就是50次
                            if times >= 15:
                                sweep_show = self.action(c='undercity', m='sweep', id=id - 1, type=1)
                                sweep_show = self.action(c='undercity', m='sweep', id=id - 1, type=2)
                            elif times>=10:
                                sweep_show = self.action(c='undercity', m='sweep', id=id - 1, type=2)
                            elif times>=5:
                                sweep_show = self.action(c='undercity', m='sweep', id=id - 1, type=1)
                            status = self.action(c='undercity',m='action',id=id)
                            # 终止任务，已经完成
                            break
                    #终止任务，已经完成
                    break
        except:
            pass
    def snow_ball(self):
        index = self.action(c='snow_ball',m='index')
        formdata = {
            "ball":1
        }
        for i in range(10):
            self.action(c='snow_ball',m='ball',body=formdata)
            self.action(c='snow_ball', m='index')
        for v in range(1,4):
            stagedata= {
                "stage":v
            }
            self.action(c='snow_ball',m='take_stage_reward',body=stagedata)
        pack = self.action(c='snow_ball',m='pack')
        try:
            if pack['own_box']:
                for l in pack['own_box']:
                    self.action(c='snow_ball', m='open_box',box_id=l['rewardInfo']['id'])
        except :
             pass
    def china_ny(self):#新年活动
        print 'china_ny新年活动'
        try:
            index = self.action(c='china_ny',m='index')
            if int(index['red_log']['take_time'])==0:
                take_red_money = self.action(c='china_ny',m='take_red_money')

            sign_index = self.action(c='china_ny', m='sign_index')
            formdata = {
                "sign_type":1
            }
            sign_index = self.action(c='china_ny', m='sign',body=formdata)
            #竞猜
            happy_quiz = self.action(c='china_ny', m='happy_quiz')

            import random
            num = random.sample([1, 2, 3, 4, 5, 6, 7, 8, 9, 10], 3)
            sitedata = {
                "site1":num[0],
                "site2":num[1],
                "site3":num[2],
            }
            bet = self.action(c='china_ny', m='bet',body=sitedata)
            #目标
            target_index = self.action(c='china_ny', m='target_index')
            if int(target_index['now_day']) == 1 and int(target_index['user_target_info'][0]['is_take']) == 0:
                #购买武将
                data ={
                   "page": 1,
                   "perpage": 9,
                   "tab": 4,
                }
                print data
                target_index = self.action(c='tavern', m='get_list',body=data)
                self.p(target_index)
                for i in list(1,30):
                    target_index = self.action(c='tavern', m='buy', generalid=id)
                    self.p(target_index)
                    if target_index['status'] ==1:
                        break
                self.action(c='china_ny', m='take_target')
        except:
            pass

    def activity(self):
        index = self.action(c='activity',m='index')
        box_info = index['box_info']
        for item in box_info:
            if item['is_take'] == 1:
                formdata = {
                    "box_id":item['id']
                }
                self.action(c='activity',m='get_active_value_box',body=formdata)
    def eaticecream(self):
        try:
            index = self.action(c='eaticecream',m='index')
            ice1 = int(index['info']['ice1'])
            ice2 = int(index['info']['ice2'])
            ice3 = int(index['info']['ice3'])
            if ice1 ==1:
                data = {
                    'type':1,
                    'num':1
                }
                self.action(c='eaticecream',m='eat',body=data)
            if ice2 ==1:
                data = {
                    'type':2,
                    'num':1
                }
                self.action(c='eaticecream',m='eat',body=data)
            if ice3 ==1:
                data = {
                    'type':3,
                    'num':1
                }
                self.action(c='eaticecream',m='eat',body=data)
        except:
            pass
    def prison(self):
        try:
            flag = 1
            self.action(c='prison',m='index')
            r = self.action(c='prison',m='get_target_list')
            for item  in r['random']:
                if  not item['master_info']:
                    formdata = {
                        "arrest_uid":item['uid'],
                        "arrest_country":item['country'],
                        "code":1,
                    }
                    r = self.action(c='prison',m='arrest',body=formdata)
                    flag = 0
            if flag == 1:
                formdata = {
                    "arrest_uid": r['random'][0]['uid'],
                    "arrest_country": r['random'][0]['country'],
                    "code": 1,
                }
                r = self.action(c='prison', m='arrest', body=formdata)

        except:
            pass
    def peace_art(self):
        try:
            print self.user,'购买太平次数'
            result = self.action(c='peace_art',m='index')
            times = int(result['can_buy_times'])
            formdata = {
                "t":1,
                "times":times
            }
            self.action(c='peace_art', m='buy_times',body=formdata)
        except:
               pass
    def eight_year(self):
        try:
            task_index = self.action(c='eight_year',m='task_index')
            if task_index['now_task_infous']:
                id = task_index['now_task_infous']["id"]
                formdata = {
                    "id":id
                }
                self.action(c='eight_year', m='take_task_reward',body=formdata)   
        except:
            pass
    def happy_double_festival(self):
        result = self.action(c='happy_double_festival',m='sign_index')
        sign = self.action(c='happy_double_festival',m='sign')
        try:
            sign_rewards = result['sign_rewards']
            for item in sign_rewards:
                if int(item['take_status']) ==1:
                    id = item['id']
                    pass
        except:
            pass
    def discount_carnival(self):
        #折扣狂欢
        try:
            cash_cow_index=self.action(c='discount_carnival', m='cash_cow_index')
            num = cash_cow_index['shake_num']
            formdata = {
                "num":num
            }
            self.action(c='discount_carnival',m='shake',body=formdata)
            self.action(c='discount_carnival',m='sign_index')
            self.action(c='discount_carnival',m='sign')
            for i in range(1,5):
                self.action(c='discount_carnival', m='shake_achieve',id=i)
        except:
            pass
    def four_seasons_picture(self):
        try:
            index = self.action(c='four_seasons_picture',m='touch_gold_stone')
            max_stone_touch = int(index['user_info']['max_stone_touch'])
            for i in range(max_stone_touch):
                self.action(c='four_seasons_picture', m='touch_stone')
                self.action(c='four_seasons_picture', m='touch_gold_stone')
        except:
            pass

    def brilliant_idea(self):#锦囊
        #加速
        try:
            index=self.action(c='brilliant_idea',m='index')
            remain_time = index['remain_time']
            if remain_time>0:
                #加速列表
                self.log.info('锦囊加速')
                expedite = index['list']['expedite'][:10]
                for item in expedite:
                    id = item['id']
                    formdata = {
                        'id':id
                    }
                    result=self.action(c='brilliant_idea',m='expedite',body=formdata)
                    try:
                        if result['id']== -4:
                            self.log.info("今日加速次数已达上限")
                            return True
                        self.log.info('加速成功')
                    except:
                        pass
            else:
                self.log.info('已经完成加速')
        except:
            pass
    def guess_lantern_riddle(self):
        try:
            print '贤才征辟'
            self.action(c='guess_lantern_riddle',m='index')
            result = self.action(c='guess_lantern_riddle',m='action')
            print '开始答题'
            quertion = result['ques_info']['id']
            for i in range(10):
                formdata = {
                    'quertion':quertion,
                    'answer':'b'
                }
                r = self.action(c='guess_lantern_riddle',m='fix_answer',body=formdata)
                quertion=r['next_ques'][id]
        except:
            pass
    def nine_year(self):
        try:
            index = self.action(c='nine_year', m='sign_index')
            index = self.action(c='nine_year', m='sign')
        except:
            pass
    def onekey_receive_give(self):
        #好友
        self.action(c='friend',m='index')
        self.action(c='friend',m='onekey_receive_give')
    def general_break_through(self):
        #点将台
        index = self.action(c='general_break_through',m='draw_index')
        try:
            times = int(index['times'])
            if times == 1:
                formdata = {
                    "pond_id": 1,
                    "type": 1
                }
                index = self.action(c='general_break_through',m='draw_card',body=formdata)
        except:
            pass
    def twentyyear_shop(self):
        try:
            self.action(c='twentyyear_shop', m='index')
            status = self.action(c='twentyyear_shop', m='draw_ticket_index')
            today_draw_num = status['today_draw_num']
            while today_draw_num > 0:
                try:
                    draw_ticket = self.action(c='twentyyear_shop', m='draw_ticket')
                    if draw_ticket['status'] == -11:
                        time.sleep(0.3)
                        self.action(c='twentyyear_shop', m='draw_ticket')
                    status = self.action(c='twentyyear_shop', m='draw_ticket_index')
                    today_draw_num = status['today_draw_num']
                except:
                    break
        except:
            pass
    def newyear_sign(self):
        self.action(c='newyear_sign',m='sign')
    def tenyear_celebration_sign(self):
        try:
            index=self.action(c='tenyear_celebration',m='sign_index')
            today = index['today']
            formdata= {
                "day":today
            }
            self.action(c='tenyear_celebration',m='sign',body=formdata)
        except:
           pass
         
    def weapon_warfare_order(self):
        try:
            index=self.action(c='weapon_warfare_order',m='receive_task_reward')
        except:
           pass

def run(user, apass, addr,pwd):
    log = MyLog(logname='task.log', level=logging.INFO)
    log.filter_.username = user
    log.filter_.addr = addr
    action = task(user, apass, addr,log)
    activity = action.get_act()
    level = action.level()
    country = activity['country']
    action.dice()  # 国家摇色子
    action.four_seasons_picture()
    #action.guess_lantern_riddle()#贤才征辟
    action.brilliant_idea()#锦囊
    action.onekey_receive_give()#好友
    if activity['nine_year'] == 1:
        action.nine_year()  # 九周年
    if level >269:
        action.general_break_through()
    if 30 < level:
        action.arena()  # 获取每日演武奖
        action.qiandao()  # 每日签到
        action.hitegg()  # 砸蛋
        #action.island()  # 金银洞
        action.mouth_card()  # 月卡奖励
        action.drink()  # 每日军令饮
    if 50 < level < 180 :
        action.lowtower()  # 低等级将魂星路推图
    else:
        action.unlock(pwd)
        action.tower()  # 高级将魂星路扫荡精英
        pass
    if 60 < level and activity['act_solt'] !=1:
        action.business()  # 每日通商
    if 70 < level:
        action.beauty()  # 铜雀台互动
    # if 91 < level:#91级开启石头收集
    #     action.workshop()  # 玉石采集
    #     action.exploit_tree()  # 木材采集
    #     action.exploit_stone()  # 石头采集
    if 50 < level:
        action.lottery(pwd)  # 每日抽奖
    if 70 <= level:
        if country != '0':
            #action.overseastrade()  # 海外贸易
            action.country()  # 国家奖励
            action.countrysacrifice()  # 每日免费贡献40
            action.gongxian(4)  # 国家贡献20次
            action.japan()  # 征战东瀛
            action.prison()#国家小黑屋
        action.assist_card()#助阵系统
        action.heaven()  # 通天塔
        action.herothrone()  # 英雄王座
        action.sanctum()  # 每日宝石领奖
        action.generaltask()  #
        action.mount_stone()  # 每日大马副本
        #for i in range(5):
        action.awaken_copy()  # 觉醒奖励
        action.essence_map()#经脉丹药扫荡
        action.undercity()#地下城
        action.world_boss()#世界boss
    if level >200:
        action.peace_art()
    if activity['eight_year'] == 1:
        action.eight_year()  # 蹴鞠
    if 220 < level and  activity['lantern_festival'] == 1:#猜灯谜
        action.lantern_festival()
    action.act_fight()  # 征战八方
    if activity['act_travel'] == 1:
        for i in range(3):
            action.sanguo()  # 游历三国
    if activity['actkemari'] == 1:
        action.cuju()  # 蹴鞠
    if activity['act_spring'] == 1:
        action.jisi()  # 新年祭祀
    if activity['happy_guoqing'] == 1:
        action.leigu()  # 欢度国庆
    if activity['chicken'] == 1:
        action.chicken()  # 吃鸡
    if activity['holiday'] == 1:
        action.holiday()  # 假日礼包
    if activity['sacredtree'] == 1:
        action.shenshu()  # 神树
    if activity['lantern'] == 1:
        action.yuanxiao()  # 元宵
    if activity['actjubao'] == 1:
        action.actjubao()  # 聚宝
    if activity['years_guard'] == 1:
        action.years_guard()  # 周年守护
    if activity['fukubukuro'] == 1:
        action.fukubukuro()  # 福矿
    if activity['gold_time'] == 1:
        action.gold_time()  # 黄金时间
    if activity['lucky_dice'] == 1:
        action.lucky_dice()  # 摇骰子
    if activity['break_egg'] == 1:
        action.break_egg()  # 砸蛋
    if activity['shopping_feast'] == 1:
        action.shopping_feast()  # 双十一签到
    if activity['double_denier'] == 1:
        action.double_denier()  # 双旦
    if activity['login_reward'] == 1:#登录签到礼
        action.loginreward()
    if activity['newyear_act'] == 1:#新年活动
        action.newyear_act()
    if activity['parade'] == 1:#沙场点兵
        action.act_parade()
    if activity['seven_year'] == 1:#周年庆
        action.seven_year()
        action.cake_index()
    if activity['snow_ball'] == 1:#扔雪球
        action.snow_ball()
    if activity['china_ny'] == 1:#新年
        action.china_ny()
    if activity['act_eatice'] == 1:#吃冰棍
        action.eaticecream()
    if activity['happy_doublefestival'] == 1:#吃冰棍
        action.happy_double_festival()
    if activity['discount_carnival'] == 1:#吃冰棍
        action.discount_carnival()
    if activity['twentyyear_shop'] == 1:#购物狂欢
        action.twentyyear_shop()
    if activity['newyear_sign'] == 1:#新年
        action.newyear_sign()
    if activity['tenyear_celebration'] == 1:#十周年
        action.tenyear_celebration_sign()
    if activity['weapon_warfare_orders'] == 1:#神奇战令
        action.weapon_warfare_order()
    if activity['jaderabbit_receivespring'] ==1:#玉兔迎春
        action.action_auto_jaderabbit_receivespringt()
    if activity['act11th_anniversary'] ==1:#十一周年庆
        action.auto_act11th_anniversary_lottery()
    if activity['luck_pk']==1:#
        action.auto_luck_pk()
    action.activity()#每日任务

def get_run(user, apass, addr,func):
    log = MyLog(logname='task.log', level=logging.INFO)
    log.filter_.username = user
    log.filter_.addr = addr
    action = task(user, apass, addr, log)
    getattr(action,func)()

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
                    try:
                        func_name = sys.argv[1]
                        t1 = threading.Thread(target=get_run, args=(name, passwd, addr, func_name))
                    except Exception as e:
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