#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/9/10 10:37
# @Author  : xingyue
# @File    : task.py


from task.base import SaoDangFb
import  time,threading
import os,json
class task(SaoDangFb):
    def copies(self):
        # 扫荡副本需要传递的参数
        # id 是副本名字id ，self.role_info
        # diff_id是困难级别分别为1,2,3个级别
        # monster_id 是第几个怪物，1-10个，
        # times 扫荡的次数
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
                        times = self.action(c="copies", m="get_monster_info", id=id, diff_id=diff_id, monster_id=monster_id,
                                    d="newequip")['info']['free_times']
                    except Exception:
                        pass
                    if times != '0':
                        print self.action(c="copies", m="mop_up", id=id, diff_id=diff_id, monster_id=monster_id,
                                          d="newequip", times=int(times))

    def qiandao(self):  # 签到
        # 领取连续登陆15天奖励，id:15，c:logined，m:get_reward
        print self.action(c='logined', m='index')

        print self.action(c='logined', m='get_reward', id=15)
        # 每日签到，所有动作就是c内容，m动作参数即可，包括领取vip工资，还有每日抽奖
        self.action(c='sign', m='sign_index')
        # c:vipwage，m:get_vip_wage，领取VIP每日奖励
        self.action(c='vipwage', m='get_vip_wage')

    def zhengshou(self):  # 征收
        cishu = self.action(c='city', m='index')  # 获取银币征收次数,m=impose,执行征收
        cishu_count = cishu['times']
        if cishu_count != '0':  # 判断征收次数是否为0，不为0则进行全部征收
            for count in range(1, int(cishu_count) + 1):
                print '开始征收第 %d 次' % count
                time.sleep(0.5)
                print self.action(c='city', m='impose')
        else:
            print '次数为0次'

    def hitegg(self):  # 砸蛋
        hitegg_cd = self.action(c='hitegg', m='index')  # 获取砸蛋首页面
        for i in range(3):
            cd = hitegg_cd['list'][i]['cd']
            if cd == 0:
                print '砸蛋成功'
                _id = i + 1
                self.action(c='hitegg', m='hit_egg', id=_id)
            elif  120 > cd >0 :
                time.sleep(cd)
                print '砸蛋成功'
                _id = i + 1
                self.action(c='hitegg', m='hit_egg', id=_id)

    def island(self):  # 金银洞活动
        # 获取当前攻击的次数和金银守护者5的状态，是否为攻击过，如果为1则为可以攻击，为0 则表示不可以
        count = self.action(c='island', m='get_mission', id=85)['info']['act']
        id_open = self.action(c='island', m='index')['list'][4]['openstatus']
        if count <= 10 and id_open != 1:
            for i in range(81, 86):  # 每日共计5次
                print self.action(c='island', m='pk', id=i)  # 共计金银洞
        id_open = self.action(c='island', m='index')['list'][4]['openstatus']
        if count <= 10 and id_open == 1:
            for i in range(5):
                print self.action(c='island', m='pk', id=85)  # 共计通过之后的最高金银洞5次
        else:
            print '今天已经攻击了10次不在攻打'

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

    def overseastrade(self):  #
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
                    print self.action(c="overseastrade", m='join_team', id=self.id, place=int(k), site=2, page=1)
                else:
                    print '加入1'
                    self.id = v['id']
                    print self.action(c="overseastrade", m='join_team', id=self.id, place=int(k), site=1, page=1)
                # print list_country[k]['member1']
        else:
            # 加入贸易队伍，每页有四个框，为place：1-4，每个框有两个位置site:1-2，页数为page:1-10默认为1即可，
            print self.action(c="overseastrade", m='join_team', id=0, place=4, site=2, page=1)

    def tower(self):  # 将魂星路
        # 领取每日奖励
        try:
            self.action(c='tower', m='reward_info')
            self.action(c='tower', m='get_reward')
            # 获取次数：
            self.tower_times = self.action(c='tower', m='get_mission_list', s=7)['times']
            print self.action(c='tower', m='mop_up', id=174, times=self.tower_times)
        except:
            pass
    def business(self):  #
        # 获取通商次数
        business_times = self.action(c='business', m='index')['times']
        print '可用通商次数 %s' % business_times
        for count in range(business_times):  # 执行通商次数
            # 每次通商是需要输入通商id
            print '开始第 %s 次通商' % count
            business_id = self.action(c='business', m='index')['trader'][0]['id']
            self.action(c='business', m='go_business', id=business_id)
        print '通商完成'

    def generaltask(self):  # 每日神将
        try:
            info  = self.action(c='generaltask', m='index')  # 获取次数
            number = info['number']
            #默认第一个将领
            gid = info['list'][0]['id']
            print '开始神将扫荡，共计 %s 次' %number
            get_list=  self.action(c='generaltask', m='get_list',p=0)
            id = int(get_list['list'][0]['id']) - 10
            # 使用长孙无忌gid=210000353508
            # 怪物id=255
            for count in range(int(number)):
                self.action(type=0, id=id, gid=gid, c='generaltask', m='action')
            print '神将10次扫荡完毕'
        except:
            pass

    def sanctum(self):
        # 每日宝石领奖
        try:
            print '领取每日宝石奖励'
            self.action(c='sanctum', m='get_reward', type=1, multiple=0)

            # 扫荡宝石次数
            # 获取次数
            print '开始扫荡宝石'
            numbers = self.action(c='sanctum', m='select_map', l=3)['times']
            if numbers != 0:
                self.action(c='sanctum', m='action', id=150, num=numbers)
            else:
                print '剩余次数为 %s 次' % numbers
            print '宝石扫荡结束'
        except:
            print '已经领取宝石奖励'

    def lottery(self):  # 每日抽奖
        # c=lottery，m=action
        # 获取每日抽奖次数
        try:
            self.numbers = self.action(c='lottery', m='index')['log']['info']['total_num']
            print '开始抽奖，剩余次数 %s' % self.numbers
            for num in range(self.numbers):
                self.action(c='lottery', m='action')
            print '抽奖结束'
        except:
            pass

    def herothrone(self):  # 英雄王座
        try:
            vip = self.action(c='member', m='index')['vip']
            if int(vip) < 9:
                self.action(c='herothrone', m='index')
                for i in range(3):
                    self.action(c='herothrone', m='start')  # 开始王座
                    # 攻击:
                    while True:
                        flag = self.action(c='herothrone', m='action')['status']
                        print  '攻击王座副本'
                        if flag == -2:
                            break
            else:
                self.action(c='herothrone', m='index')
                for i in range(3):
                    self.action(c='herothrone', m='start')  # 开始王座
                    self.action(c='herothrone', m='end_battle')
                    self.action(c='herothrone', m='go_back')

        except:
            pass
    def mount_stone(self):
        try:
            vip = self.action(c='member', m='index')['vip']
            if int(vip) < 9:
                self.action(c='mountstone_throne', m='index')
                for i in range(3):
                    self.action(c='mountstone_throne', m='start')  # 开始王座
                    # 攻击:
                    while True:
                        flag = self.action(c='mountstone_throne', m='action')['status']
                        print  '攻击符石副本'
                        if flag == -2:
                            break
            else:
                self.action(c='mountstone_throne', m='index')
                for i in range(3):
                    self.action(c='mountstone_throne', m='start')  # 开始王座
                    self.action(c='mountstone_throne', m='end_battle')  # 开始王座
                    self.action(c='mountstone_throne', m='go_back')  # 开始王座
        except:
            pass
    def workshop(self):  # 玉石收集
        # 收取
        for i in range(1, 7):
            try:
                self.action(c='workshop', m='get_reward', s=i)
            except:
                pass

    def exploit_tree(self):  # 木材收集
        try:
            # gather收集,site:1,第一个框
            self.action(c='exploit_tree', m='gather', site=1)
            self.action(c='exploit_tree', m='action', site=1)
        except:
            pass

    def exploit_stone(self):  # 石头收集
        try:
        # exploit_stone，m:{gather收集,action，采集}site:1,第一个框,有三个
            for i in range(1, 4):
                self.action(c='exploit_stone', m='gather', site=i)
                self.action(c='exploit_stone', m='action', site=i)
        except:
            pass
    def heaven(self):  # 通天塔每日奖励和扫荡
        # 获取每日奖励
        try:
            self.action(c='heaven', m='get_reward')
            self.times = self.action(c='heaven', m='index')['times']
            if self.times:
                self.action(c='heaven', m='mop_up', id=87, times=self.times)
        except:
            pass

    def arena(self): #每日觉醒奖励
        try:
            self.action(c='arena', m='index')
            self.action(c='arena', m='get_reward')
        except:
            pass
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
                        print self.action(c='map', m='action', l=level, s=i + 1, id=id, times=times)

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
        print self.action(c='actguyu', m='reward_index', id=22, num=1)


    def dice(self):  # 国家摇色子
        points = self.action(c='dice', m='index')['member']['points']
        if int(points) > 400:
            self.action(c='dice', m='get_reward', id=2)
        for i in range(1, 8):
            self.action(c='dice', m='shake_dice')

    def act_steadily(self):  # 节节高
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
        except:
            pass

    def act_sword(self):  # 铸剑
        print self.action(c='act_sword', m='start')
        info = self.action(c='act_sword', m='index')
        print  info
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
            print self.action(c='act_sword', m='get_cast_reward')
            time.sleep(0.5)
            self.action(c='act_sword', m='index')
            self.action(c='act_sword', m='start')
        else:  #
            sleep_time = need_nums - int(nums)
            print sleep_time
            time.sleep(sleep_time * 50)
        # print self.action(c='act_sword',m='battle',touid='260000484980')

    def awaken_copy(self):  # 每日
        self.action(c='awaken_copy', m='index')
        self.action(c='awaken_copy', m='every_reward_index')
        self.action(c='awaken_copy', m='get_every_reward', b=1)

    def countrymine(self):#国家矿
        try:
            mineinfo = self.action(c='countrymine', m='index')
            print mineinfo
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
        status = 1
        while status == 1:
            status = self.action(c='beauty', m='active_action', beauty_id=2, type=1)['status']

    def country(self):  # 每日国家奖励
        self.action(c='country', m='get_salary')

    def countrysacrifice(self):  # 每日贡献
        print self.action(c='countrysacrifice', m='index', id=1)
        print self.action(c='countrysacrifice', m='action', id=1)

    def get_act(self):
        act_info = self.action(c='member', m='index')
        return act_info

    def awaken(self):
        shop_index = self.action(c='awaken', m='shop')
        count = shop_index['remain_freetimes']  # 获取免费次数
        refresg_list = shop_index['list']  # 获取信息
        self.action(c='awaken', m='refresh')
        for info in refresg_list:
            if info['reward_type'] == '64' and info['coin_type'] == '65':
                id = int(info['id'])
                # self.action(c='awaken',m='shop_buy',id=id)#购买物品
    def gongxian(self):  # 国家贡献
        self.action(c='country', m='get_member_list')
        self.action(c='country', m='storage')
        result = self.action(c='country', m='donate', type=1)
        try:
            status = result['status']
            if status != 1:
                info = self.action(c='country', m='donate', type=1)
                print info
                status = info['status']
        except:
            print result
    def cuju(self):  # 蹴鞠首页
        try:
            index = self.action(c='act_kemari', m='index')
            for i in index['list']:
                if i['id'] == 2 and i['times'] != 0 and i['cd'] == 0:
                    self.action(c='act_kemari', m='action', type=2)
                elif i['id'] == 1 and i['times'] != 0 and i['cd'] == 0:
                    self.action(c='act_kemari', m='action', type=1)
        except:
            pass

    def sanguo(self):  # 游历三国活动
        try:
            travelindex = self.action(c='act_travel', m='index')  # 获取活动
            details = self.action(c='act_travel', m='action_travel')['details']  # 开始活动
            print travelindex['info']['points']
            if travelindex['info']['free'] == 1:
                result = self.action(c='act_travel', m='action_dice')  # 掷骰子
            if travelindex['info']['points'] != 0:
                # #走路顺序list[4,2,3,5,8,9,10,11,12,13,14]
                plain = [1, 4, 2, 3, 5, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28,
                         29,
                         30]
                num = plain.index(int(details['current'])) + 1
                stats = self.action(c='act_travel', m='plain', point=plain[num])
        except:
            pass
    def jisi(self):  # 新年活动
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
        except:
            pass
    def leigu(self):
        self.action(c='happy_guoqing', m='get_reward', type=1)
    def chicken(self):
        try:
            chenk = self.action(c='chicken', m='vip_index', v=2018021101)['reward']
            member = self.action(c='member', m='index')
            vip = member['vip']
            print json.dumps(chenk)
            for l in chenk:
                # print vip,l['vip']
                if int(l['vip']) == int(vip):
                    print self.action(c='chicken', m='get_vip_reward', id=l['id'])
                    break
        except:
            pass
    def holiday(self):
        print self.action(c='act_holiday', m='index', v=2018021101)
        print self.action(c='act_holiday', m='add_login_reward', v=2018021101)
    def shenshu(self):  # 神树
        index = self.action(c='sacredtree', m='index')
        if index['time'] == 1:
            print self.action(c='sacredtree', m='watering', type=1, v=2018021101)
    def yuanxiao(self):
        try:
            index = self.action(c='act_lantern', m='index', v=2018021101)
            if index['freetimes'] > 0:
                self.action(c='act_lantern', m='buy', lid=1, mid=1, v=2018021101)
                self.action(c='act_lantern', m='buy', lid=1, mid=2, v=2018021101)
                self.action(c='act_lantern', m='buy', lid=1, mid=3, v=2018021101)
        except:
            pass
    def actjubao(self):
        self.action(c='actjubao', m='index', v=2018042801)
        self.action(c='actjubao', m='action', type=1, v=2018042801)
        self.action(c='actjubao', m='reward_index', v=2018042801)
        self.action(c='actjubao', m='get_reward', id=1, v=2018042801)
    def years_guard(self):  # 周年守护签到
        self.action(c='years_guard', m='des_index')
        self.action(c='years_guard', m='sign_index')

    def fukubukuro(self):  # 周年福矿签到
        self.action(c='fukubukuro', m='index')
        self.action(c='fukubukuro', m='sign', type=1)
        self.action(c='fukubukuro', m='get_general', gid=354)
    def drink(self):#每日饮酒
        self.action(c='drink',m='index')
        self.action(c='drink',m='go_drink',type=1)
def run(user,apass, addr):
    action = task(user,apass, addr)
    action.arena()  # 获取每日演武奖
    action.qiandao()  # 每日签到
    action.hitegg()  # 砸蛋
    action.heaven()  # 通天塔
    action.workshop()  # 玉石采集
    action.exploit_tree()  # 木材采集
    action.exploit_stone()  # 石头采集
    action.herothrone()  # 英雄王座
    action.sanctum()  # 每日宝石领奖
    action.generaltask()  #
    action.business()  # 每日通商
    action.tower()  # 将魂星路
    action.island()  # 金银洞
    action.lottery()  # 每日抽奖
    action.worldboss()  # 世界boos
    #action.copies()  # 扫荡副本
    action.mount_stone()  # 每日大马副本
    action.awaken_copy()  # 觉醒奖励
    action.dice()  # 国家摇色子
    action.mouth_card()  # 月卡奖励
    action.beauty()  # 铜雀台互动
    action.drink()#每日军令饮酒
    action.country()  # 国家奖励
    action.overseastrade()  # 海外贸易
    action.countrysacrifice()
    for i in range(50):
        action.gongxian()
    if action.get_act()['act_travel'] == 1:
        action.sanguo()#游历三国
    if action.get_act()['actkemari'] == 1:
        action.cuju()#蹴鞠
    if action.get_act()['act_steadily'] == 1:
        while True:
            action.act_steadily()
    if action.get_act()['act_spring'] == 1:
        action.jisi()#游历三国
    if action.get_act()['leigu'] == 1:
        action.leigu()#游历三国
    if action.get_act()['chicken'] == 1:
        action.chicken()#游历三国
    if action.get_act()['holiday'] == 1:
        action.holiday()#游历三国
    if action.get_act()['sacredtree'] == 1:
        action.shenshu()#游历三国
    if action.get_act()['lantern'] == 1:
        action.yuanxiao()#游历三国
    if action.get_act()['actjubao'] == 1:
        action.actjubao()#游历三国
    if action.get_act()['years_guard'] == 1:
        action.years_guard()#游历三国
    if action.get_act()['fukubukuro'] == 1:
        action.fukubukuro()#游历三国

    # action.zimap()
    # action.hongmap()

if __name__ == '__main__':
    filepath = os.path.dirname(os.path.abspath(__file__))
    cont = ['autouser.txt','']
    for t in cont:
        with open('%s/users/%s'%(filepath,t),'r') as f:
            for i in f:
                if i.strip() :
                    name = i.split()[0]
                    passwd = i.split()[1]
                    addr = i.split()[2]
                    t1 = threading.Thread(target=run, args=(name, passwd, addr))
                    t1.start()
                    # t1.join()
                    time.sleep(0.2)
        time.sleep(60)