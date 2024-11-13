# -*- coding:utf-8 -*-
import threading
import time
import json
import shujufenx
from shujufenx import fuben
from Queue import Queue
from random import choice
import hashlib
import random


import redis
pool = redis.ConnectionPool(host='localhost', port=6379, db=0)
_redis = redis.StrictRedis(connection_pool=pool)
"""每日不定期开展活动"""


def p(message):
    print json.dumps(message, ensure_ascii=False)


def userinfo(username, password, addr):
    s1.acquire()
    action = shujufenx.fuben(username, password, addr)
    info = action.action(c='blackmarket', m='index')  # 获取黑市首页
    memberInfo = action.action(c='member', m='index')
    sign_index = action.action(c='sign', m='sign_index')
    sign_times = sign_index['sign_times']
    # sale_shop_reward = act.action(c='sign', m='sale_shop')['reward']
    # p(act.action(c='country', m='get_member_list'))
    country = action.action(c='country', m='get_member_list')['country']
    if country:
        countryName = country['name']
    else:
        countryName = None
    name = memberInfo['nickname']  # 账号
    level = memberInfo['level']  # 等级
    act = memberInfo['act']  # 军令
    silver = memberInfo['silver']  # 银币
    gold = memberInfo['gold']  # 元宝
    vip = memberInfo['vip']
    reputation = memberInfo['reputation']  # 声望
    print '\n账号 %s 名字 %s 等级 %s vip %s 国家 %s 大区 %s 军令 %s 银币 %s 元宝 %s 黄宝石 %s 紫宝石 %s 声望 %s 签到 %s' % (
        username, name, level, vip, countryName, action.num, act, silver, gold, info['info']['get2'], info['info']['get3'],
        reputation, sign_times)
    userlist = [username, name, level, vip, countryName, act, silver, gold, info['info']['get2'], info['info']['get3'],
                reputation, sign_times]
    s1.release()
    return userlist


class activity(fuben):
    def sanguo(self):  # 游历三国活动
        try:
            travelindex = self.action(c='act_travel', m='index')  # 获取活动
            details = self.action(c='act_travel', m='action_travel')['details']  # 开始活动
            print travelindex['info']['points']
            if travelindex['info']['free'] == 1:
                result = self.action(c='act_travel', m='action_dice')  # 掷骰子
            if travelindex['info']['points'] != 0:
                # #走路顺序list[4,2,3,5,8,9,10,11,12,13,14]
                plain = [1, 4, 2, 3, 5, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27,
                         28,
                         29,
                         30]
                num = plain.index(int(details['current'])) + 1
                stats = self.action(c='act_travel', m='plain', point=plain[num])
        except:
            pass

    def jingsu(self):  # 竞速奖励
        info = self.action(c='map', m='get_reward_list', channel=11, v=2017122401)
        # print info
        for i in info['list']:
            if i['open_status'] == 0:
                print '%s 已通过未领取 ，元宝：%s' % (i['name'], i['gold'])
                self.action(c='map', m='get_mission_reward', id=i['missionid'])
            elif i['open_status'] == 1:
                print '%s 未通过 ，元宝：%s' % (i['name'], i['gold'])
            elif i['open_status'] == 2:
                print '%s 已通过已领取 ，元宝：%s' % (i['name'], i['gold'])
        #       self.action(c='map',m='get_mission_reward',id=i['missionid'])

    def sign(self):  # 够买签到声望
        index = self.action(c='sign', m='sign_index')
        shop = self.action(c='sign', m='sale_shop')
        for i in shop['reward']:
            self.action(c='sign', m='get_reward', type=2, id=i['id'])

    def fuka(self, num, flag=False):  # 福卡活动处理
        print '-' * 20
        flag = True
        status = 1
        qm_card = self.action(c='qm_card', m='index')
        index = self.action(c='qm_card', m='get_lottery')
        score = int(index['lottery_num']['score'])
        refresh_times = int(qm_card['refresh_times'])
        print '当前福卡', int(index['lottery_num']['score'])
        print '翻牌数', num
        cost = str(qm_card['cost'])
        while score < int(num) and status == 1:
            print '本次花费: %s' % cost
            print '剩余福卡: %s' % score
            print '开始翻牌'
            if cost < '50' and status == 1:
                draw = self.action(c='qm_card', m='draw ', v=2018061901)
                cost = draw['next_cost']
                status = draw['status']  # 随机翻牌
                score = int(draw['score'])
            elif cost == '50' and refresh_times != 0:
                self.action(c='qm_card', m='refresh')  # 重制翻盘
                refresh_times -= 1
            elif cost == '50' and refresh_times == 0:
                try:
                    print '当前福卡:%s,设定值:%s' % (score, num)
                    draw = self.action(c='qm_card', m='draw ', v=2018061901)
                    cost = draw['next_cost']
                    status = draw['status']  # 随机翻牌
                    score = int(draw['score'])
                except KeyError as e:
                    print e
                    continue
            else:
                break
        print '当前福卡', int(index['lottery_num']['score'])
        print '翻牌数', num

        # qm_index = self.action(c='qm_card', m='get_lottery')  # 获取福卡商店首页
        # qmindex = self.action(c='qm_card', m='action_lottery', id=4)  # 用福卡买1紫宝石,2突飞卡4 1150突飞
        # while qmindex['status'] == 1:
        #     self.action(c='qm_card', m='action_lottery', id=4)
        #     qmindex = self.action(c='qm_card', m='action_lottery', id=1)  # 用福卡买紫宝石

    def guyu(self):  # 古玉换银币
        info = self.action(c='actguyu', m='index')
        reputation = int(info['reputation'])
        vip = int(info['vip'])
        purple_jade = int(info['purple_jade'])
        if info['vip'] == "1":
            if reputation / 220000 >= 2:
                self.action(c='actguyu', m='reward_index ', id=6, num=2)
            elif reputation / 220000 == 1:
                self.action(c='actguyu', m='reward_index ', id=6, num=1)
            info = self.action(c='actguyu', m='index')
            reputation = int(info['reputation'])
            if reputation / 55000 >= 2:
                self.action(c='actguyu', m='reward_index ', id=5, num=2)
            elif reputation / 55000 == 1:
                self.action(c='actguyu', m='reward_index ', id=5, num=1)
            info = self.action(c='actguyu', m='index')
            reputation = int(info['reputation'])
            if reputation / 11000 >= 2:
                self.action(c='actguyu', m='reward_index ', id=4, num=2)
            elif reputation / 11000 == 1:
                self.action(c='actguyu', m='reward_index ', id=4, num=1)
            self.action(c='actguyu', m='reward_index ', id=1, num=2)
            self.action(c='actguyu', m='reward_index ', id=2, num=2)
            self.action(c='actguyu', m='reward_index ', id=3, num=2)
        else:
            self.action(c='actguyu', m='reward_index ', id=1, num=1)
            self.action(c='actguyu', m='reward_index ', id=2, num=1)
            self.action(c='actguyu', m='reward_index ', id=3, num=1)
            self.action(c='actguyu', m='reward_index ', id=6, num=1)
            self.action(c='actguyu', m='reward_index ', id=5, num=1)
            self.action(c='actguyu', m='reward_index ', id=4, num=1)
            self.action(c='actguyu', m='reward_index ', id=7, num=1)
            self.action(c='actguyu', m='reward_index ', id=8, num=1)
            self.action(c='actguyu', m='reward_index ', id=9, num=1)
        # #所有 古玉够买声望
        info = self.action(c='actguyu', m='index')
        num = info['guyu']
        self.action(c='actguyu', m='reward_index', id=34, num=num)

    def mooncake(self):  # 活动吃月饼
        self.action(c='act_mooncake', m='action', type=1)
        self.action(c='act_mooncake', m='action', type=2)
        self.action(c='act_mooncake', m='action', type=3)

    def generalpool(self):  # 武将池
        # id 350 董卓，351 神文丑  282 神鲁肃 353 神卢植 281 神刘表 279 神袁尚
        self.action(c='act_generalpool', m='index')
        # result = self.action(c='act_generalpool', m='general_chip')

        # 免费武将1谋士，2武将
        # self.action(c='act_generalpool', m='lottery', type=1)
        # self.action(c='act_generalpool', m='lottery', type=2)
        # chip = self.action(c='act_generalpool', m='general_chip')
        # for i in chip['own_chip']:
        while True:
            try:
                info = self.action(c='act_generalpool', m='general_chip_info', gid=352)
                if info['general']['is_exist'] == 1:
                    print '已招募'
                    break
                print self.user, "已有碎片{}，剩余碎片{}".format(info['own_chip'], info['need_chip'])
                own_chip = int(info['own_chip'])
                need_chip = int(info['need_chip'])
                if own_chip < need_chip:
                    result = self.action(c='act_generalpool', m='lottery_ten', type=1, shop=2)  # 10次文丑， type 1 谋士，2 武将
                    if result['status'] != 1:
                        break
                else:
                    print 'hecheng'
                    self.action(c='act_generalpool', m='recruit', gid=352)
                    break
            except Exception as e:
                status = self.action(c='act_generalpool', m='lottery_ten', type=1, shop=2)
                print self.user, status['status']
                break

        # self.action(c='act_generalpool', m='recruit', gid=gid)合成武将

    def messages(self):
        print  self.action(c='message', m='get_notice')

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

    def gongxiang(self):  # 国家贡献
        memberInfo = self.action(c='member', m='index')
        self.action(c='country', m='get_member_list')
        self.action(c='country', m='storage')
        if int(memberInfo['level']) > 90:
            print '等级大于90'
            return
        flag = 0
        donate = 0
        try:
            while True:
                if flag < 10:
                    result = self.action(c='country', m='donate', type=1)
                    status = result['status']
                    if status == 1:
                        donate += 10
                        print donate
                    else:
                        flag += 1
                else:
                    break
        except:
            print result
            # self.action(c='country',m='get_member_list')
            # self.action(c='country',m='storage')
            # status = self.action(c='country',m='donate',type=1)['status']
            # while status != 1:
            #       status = self.action(c='country',m='donate',type=1)['status']

    def countrysacrifice(self):  # 国家每日贡献
        self.action(c='country', m='get_salary')
        self.action(c='countrysacrifice', m='action', id=1)

    def tes(self):  # 国家任务
        self.action(c='country', m='get_member_list')
        self.action(c='expostulation', m='support', id=251000004878)

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

    def jinyan(self):  # 国家谨言
        self.action(c='expostulation', m='get_reward', id=251000004881)

    def usebuff(self):
        self.action(c='country_taxes_shop', m='index')
        buy = self.action(c='country_taxes_shop', m='buy', id=1)
        p(self.action(c='war_college', m='use_buff', need_general=4))

    def act_sword(self):  # 铸剑
        self.action(c='act_sword', m='start')
        # print self.action(c='act_sword', m='battle', touid='291000034922')
        info = self.action(c='act_sword', m='index')

        self.action(c='act_sword', m='get_rank_reward', type=1)
        self.action(c='act_sword', m='get_rank_reward', type=0)
        need_nums = int(info['need_nums'])
        nums = info['nums']
        print need_nums, nums
        # 收获
        if need_nums == int(nums):
            self.action(c='act_sword', m='index')
            time.sleep(0.5)
            print self.action(c='act_sword', m='get_cast_reward')
            time.sleep(0.5)
            self.action(c='act_sword', m='index')
            self.action(c='act_sword', m='start')
        else:
            slp = need_nums - int(nums)
            print slp
            time.sleep(slp * 50)

    def pack(self):  # 卖垃圾装备
        index1 = self.action(c='pack', m='index', type=1)  # 武器
        index3 = self.action(c='pack', m='index', type=3)  # 铠甲
        index4 = self.action(c='pack', m='index', type=4)  # 防御
        index5 = self.action(c='pack', m='index', type=5)  # 兵符
        for equ in index1['list']:  # 遍历未穿戴装备列表
            if equ['quality'] == "3" or equ['quality'] == "1" or equ['quality'] == "2":
                self.action(c='pack', m='sale', id=equ['id'])
        for equ in index3['list']:  # 遍历未穿戴装备列表
            if equ['quality'] == "3" or equ['quality'] == "1" or equ['quality'] == "2":
                self.action(c='pack', m='sale', id=equ['id'])
        for equ in index4['list']:  # 遍历未穿戴装备列表
            if equ['quality'] == "3" or equ['quality'] == "1" or equ['quality'] == "2":
                self.action(c='pack', m='sale', id=equ['id'])
        # c=pack&m=sale&id=291000378856 ,出售制定装备
        # print self.action(c='pack', m='open_box', id=5, num=40)

    def jisi(self):  # 新年活动
        self.action(c='act_spring', m='index')
        index = self.action(c='act_spring', m='sacrifice_index')
        if index['price']['3']['1'] < "70":  # 福币
            self.action(c='act_spring', m='sacrifice', type=3, resource_type=1)

        if index['price']['1']['1'] < "50":  # 装备
            self.action(c='act_spring', m='sacrifice', type=1, resource_type=1)
        if index['price']['1']['79'] < "5":
            p(self.action(c='act_spring', m='sacrifice', type=1, resource_type=79))
        # if index['price']['2']['1'] < "50":#将魂
        #     self.action(c='act_spring', m='sacrifice', type=2, resource_type=1)
        #     self.action(c='act_spring', m='sacrifice', type=2, resource_type=2)

    def leigu(self):
        self.action(c='happy_guoqing', m='get_reward', type=1)

    def fubi(self):
        status = 1
        while status == 1:
            index = self.action(c='act_spring', m='exchange', id=23, v=2018021101)
            status = index['status']

    def jianghun(self):
        try:
            index = self.action(c='soul', m='index')
            info = index['pack']['list']
            memberInfo = self.action(c='member', m='index')
            pages = index['pack']['pages']
            name = memberInfo['nickname']  # 账号
            for i in info:
                if i['name'] in ['穷变战魂', '移山战魂', '形虚战魂']:
                    print '账号 :%s ,%s' % (self.username, i['name'])
            for page in range(1, pages):
                result = self.action(c='soul', m='get_pack_info', page=page)
                for i in result['info']['list']:
                    if i['name'] in ['穷变战魂', '移山战魂', '形虚战魂']:
                        print '账号 :%s ,%s' % (self.username, i['name'])
        except:
            pass

    def meiri(self):
        for i in range(1, 16):
            print self.action(c='logined', m='get_reward', id=1)

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
        # print self.action(c='chicken', m='get_vip_reward', id=17)
        # print self.action(c='chicken', m='get_vip_reward', id=2)
        # print self.action(c='chicken', m='get_vip_reward', id=3)

    def holiday(self):
        print self.action(c='act_holiday', m='index', v=2018021101)
        print self.action(c='act_holiday', m='add_login_reward', v=2018021101)

    def signs(self):  # 每日福利签到购买
        self.action(c='sign', m='get_reward', type=2, id=95)

    def ivlist(self):  # 邀请好友
        # print self.action(c='invitation', m='change', code='nifckpm', v=2018021101)
        print self.action(c='invitation', m='change', code='7tzwcii', v=2018021101)

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
                print "\r", exp, levelup_exp
                if cd < 86400 and levelup_exp < 2000:
                    print '浇水'
                    self.action(c='sacredtree', m='watering', type=1, v=2018021101)
                else:
                    break
        except:
            pass

    def yuanxiao(self):
        try:
            index = self.action(c='act_lantern', m='index')
            if index['is_open'] == 1:
                for item in index['list']:
                    if item['l_status'] ==2:
                        continue
                    else:
                        print 'jin'
                        for i in range(1,4):
                            lid = item['lid']
                            mid = i
                            formdata={
                                'mid':mid,
                                'lid':lid,
                            }
                            num = 0
                            while num < 50:
                                result = self.action(c='act_lantern',m='buy',body=formdata)
                                self.p(result)
                                if result['status'] ==1:
                                    num = int(result['num%s'%i])
                                elif result['status'] == -3:
                                    break
                                else:
                                    time.sleep(0.5)
                            self.action(c='act_lantern',m='eat',lid=lid)

            # if index['freetimes'] > 0:
            #     self.action(c='act_lantern', m='buy', lid=1, mid=1)
            #     self.action(c='act_lantern', m='buy', lid=1, mid=2)
            #     self.action(c='act_lantern', m='buy', lid=1, mid=3)
        except:
            pass

    def message(self):
        while True:
            stauts = self.action(c='worldarena', m='get_server_reward')
            #self.p(stauts)
            if stauts['status']!=1:
                time.sleep(0.3)
                break

    def betray(self):  # 叛国
        if int(self.level()) > 170:
            return None
        else:
            self.action(c='country', m='betray')

    def jioncountry(self, name):  # 加入国家
        self.action(c='member', m='index')
        self.action(c='country', m='get_rank')

        # info = self.action(c='country', m='search', name=name)
        # print info
        # if info['status'] == 1:
        #     uid = info['country']['id']
        #     print uid
        #     print self.action(c='country', m='apply', id=uid)
        #     return
        # print 'assssssss'
        for i in range(1, 85):
            info = self.action(c='country', m='get_rank', page=i)
            for item in info["list"]:
                if item['name'] == name:
                    print item['name'], name
                    id = int(item['id'])
                    print id
                    self.action(c='country', m='apply', id=id)
                    exit(3)

    def gxinfo(self):  # 国家贡献
        # member_List = self.action(c='country', m='get_member_list')
        # p(member_List)
        info = self.action(c='country', m='storage')
        # p(info)
        print 'level:%s %s/%s' % (info['country']['level'], info['country']['exp'], info['country']['levelupexp'])
        print  '名次\t昵称\t贡献'
        for i in range(5):
            item = info['list'][i]
            print '%s\t%s\t%s' % (info['list'].index(item), item['nickname'], item['contribute'])

    def actjubao(self):
        self.action(c='actjubao', m='index', v=2018042801)
        self.action(c='actjubao', m='action', type=1, v=2018042801)
        self.action(c='actjubao', m='reward_index', v=2018042801)
        self.action(c='actjubao', m='get_reward', id=1, v=2018042801)

    def jingcai(self):
        # 拍卖行竞拍，魔马超
        self.action(c='act_auction', m='auction', id=61, num=1)

    def wuxing(self, id1, id2):
        self.action(c='member', m='resource_unlock', token_uid=210000353508, pwd=413728)
        info = self.action(c='five_line_guess', m='guessing', guess_type_1=1, guess_id_1=id1, guess_type_2=2,
                           guess_id_2=id2, goods_type=7, num=2000, v=2018061101)
        return info

    def caikuang(self):
        mineinfo = self.action(c='mine', m='index')
        dateline = mineinfo['dateline']
        log = mineinfo['log']
        if log:
            log_dateline = log['dateline']
            lasttime = int(dateline) - int(log_dateline)
            print lasttime
            if lasttime > 14400:
                self.action(c='mine', m='give_up')
                print self.action(c='mine', m='get_silver', s=mineinfo['log']['site'])
                for i in range(1, 6):
                    mineinfo = self.action(c='mine', m='index', p=i)['list']
                    for l in mineinfo:
                        if l['status'] == 0:
                            self.action(c='mine', m='caikuang', p=i, id=l['id'], t=l['type'])
                            break
        else:
            for i in range(1, 6):
                mineinfo = self.action(c='mine', m='index', p=i)['list']
                for l in mineinfo:
                    if l['status'] == 0:
                        self.action(c='mine', m='caikuang', p=i, id=l['id'], t=l['type'])
                        break
                # 占矿

    def countrymine(self):
        try:
            mineinfo = self.action(c='countrymine', m='index')
            dateline = mineinfo['dateline']
            log = mineinfo['log']
            if log:
                log_dateline = log['dateline']
                lasttime = int(dateline) - int(log_dateline)
                if lasttime > 900:
                    s = log['site']
                    self.p(self.action(c='countrymine', m='get_reward', s=s))
                print self.user, lasttime
                for i in range(2, 10):
                    mineinfo = self.action(c='countrymine', m='index', p=i)['list']
                    for l in mineinfo:
                        if l['status'] == 0:
                            self.action(c='countrymine', m='caikuang', p=i, id=l['id'], t=l['type'])
                            return
        except KeyError as e:
            print e, '没有加入国家，或是等级不够'

    def arena(self):  #
        self.action(c='arena', m='index')
        self.action(c='arena', m='get_reward')

    def role(self, name):  # 注册名字
        p(self.action(c='member', m='select_role', sex=2, name=name))

    def chat(self, ms):  # 获取聊天信息
        chat_index = self.action(c='chat', m='index')
        # for message in chat_index['list']:
        #     print u'%s' % message['nickname'] + ":" + u'%s' % message['message']
        print self.action(c='chat', m='send', message=ms)  # 发送消息

    def robholiday_seatrade(self, name, user):  # 海运打劫
        # name 就是打劫的国家[list]
        # authorization 需要 hd5key
        # udi:用户角色id信息 ，robkey：zykj
        # "rob" + uid +robkey + robid)
        uid = self.get_act()['uid']
        robkey = "zykj"
        robtimes = 1
        while robtimes > 0:
            time.sleep(random.random())
            index_result = self.action(c='holiday_seatrade', m='index')
            try:
                robtimes = int(index_result['info']['robtimes'])  # 获取打劫次数
                print '{user} 剩余打劫次数 {robtimes}\r'.format(user=user, robtimes=robtimes)
            except Exception as e:
                break
            try:
                try:
                    fromdata = {
                        'p':1
                    }
                    refresh = self.action(c='holiday_seatrade', m='refresh', body=fromdata) # 获取刷新船信息
                    refresh_result = refresh['team']
                except KeyError as e:
                    refresh = self.action(c='holiday_seatrade', m='refresh', body=fromdata)  # 获取刷新船信息
                    refresh_result = refresh['team']
                if refresh_result['allpage'] > 1:  # 船页数大于1页需要遍历
                    for i in range(refresh_result['allpage']):
                        try:
                            aaa = self.action(c='holiday_seatrade', m='refresh', p=i + 1)
                            team_list = aaa['team']['list']
                        except:
                            team_list = self.action(c='holiday_seatrade', m='index')['team']['list']
                        for team in team_list:
                            if team['country_name'] in name + ['皇家酒店%d'%i for i in range(1,80)] + ['dc%d'%i for i in range(1,20)]:
                                id = team['id']
                                key = "world_rob" + uid + robkey + id
                                authorization = hashlib.md5(key).hexdigest()
                                rob_result = self.action(c='holiday_seatrade', m='rob',
                                                         body={"id": id, "authorization": authorization})
                                if rob_result['status'] != 1:
                                    print '打劫失败'
                                    continue
                                else:
                                    self.p(rob_result)
                                    break

                else:
                    team_list = refresh_result['list']
                    for team in team_list:
                        print team['country_name']
                        if team['country_name'] in name + ['皇家酒店%d'%i for i in range(1,80)] + ['dc%d'%i for i in range(1,20)]:
                            id = team['id']
                            key = "rob" + uid + robkey + id
                            authorization = hashlib.md5(key).hexdigest()
                            rob_result = self.action(c='holiday_seatrade', m='rob',
                                                     body={"id": id, "authorization": authorization})
                            if rob_result['status'] != 1:
                                print '打劫失败'
                                continue
                            else:
                                self.p(rob_result)
                                break

            except Exception as e:
                #self.p(self.action(c='overseastrade', m='refresh', p=i + 1))
                pass

    def world_rob_redis(self,user,addr):
        #直接从redis 获取id打劫3
        # 如果redis 有key 则从redis 取，没有创建
        # 判断大区是什么
        ip149 = [i for i in range(145, 150)]
        ip21 = [21, 22, 25, 26, 29, 30]
        worldkey = 'set:worldstrade:{addr}'.format(addr=149)
        ip = int(addr)
        if ip in ip149:
            print '大区为149'
            worldkey = 'set:worldstrade:{addr}'.format(addr=149)
        elif ip in ip21:
            print '大区为 21'
            worldkey = 'set:worldstrade:{addr}'.format(addr=21)
        uid = self.get_act()['uid']
        robkey = "zykj"
        index_result = self.action(c='overseastrade', m='world_index')
        try:
            robtimes = int(index_result['info']['robtimes'])  # 获取打劫次数
            allpage = index_result['team']['all_page']
            print '{user} 剩余打劫次数 {robtimes}，现有海运{allpage}页\r'.format(user=user, robtimes=robtimes, allpage=allpage)
        except Exception as e:
            print e
        while robtimes > 0:
            v = _redis.get(worldkey)
            if not v:
                continue
            id = v.split(':')[0]
            key = "rob" + uid + robkey + id
            authorization = hashlib.md5(key).hexdigest()
            rob_result = self.action(c='overseastrade', m='world_rob',
                                     body={"id": id, "authorization": authorization})
            if rob_result['status'] != 1:
                print '打劫失败'
                try:
                    print rob_result['msg']
                except:
                    pass
                continue
            else:
                self.p(rob_result)
                robtimes -= 1


    def world_rob(self, name, user):  # 海运打劫
        # name 就是打劫的国家[list]
        # authorization 需要 hd5key
        # udi:用户角色id信息 ，robkey：zykj
        # "rob" + uid +robkey + robid)

        uid = self.get_act()['uid']
        robkey = "zykj"
        robtimes = 1
        while robtimes > 0:
            time.sleep(random.random())
            index_result = self.action(c='overseastrade', m='world_index')
            try:
                robtimes = int(index_result['info']['robtimes'])  # 获取打劫次数
                allpage = index_result['team']['all_page']
                print '{user} 剩余打劫次数 {robtimes}，现有海运{allpage}页\r'.format(user=user, robtimes=robtimes,allpage=allpage)
            except Exception as e:
                break
            try:
                try:
                    fromdata = {
                        'p':1
                    }
                    refresh = self.action(c='overseastrade', m='world_refresh', body=fromdata) # 获取刷新船信息
                    refresh_result = refresh['team']
                except KeyError as e:
                    refresh = self.action(c='overseastrade', m='world_refresh', body=fromdata)  # 获取刷新船信息
                    refresh_result = refresh['team']
                if allpage > 1:  # 船页数大于1页需要遍历
                    for i in range(int(refresh_result['all_page'])):
                        try:
                            aaa = self.action(c='overseastrade', m='world_refresh', p=i + 1)
                            team_list = aaa['team']['list']
                        except:
                            team_list = self.action(c='overseastrade', m='world_index')['team']['list']
                        for k,team in team_list.items():
                            for item in team:
                                if item:
                                    #只要有必定是两个船一起开
                                    #print item['country_name'],item['member1_name'],item['member2_name']
                                    if item['country_name'] in name + ['皇家酒店%d'%i for i in range(1,80)] + ['dc%d'%i for i in range(1,20)]:
                                        id = item['id']
                                        key = "rob" + uid + robkey + id
                                        authorization = hashlib.md5(key).hexdigest()
                                        rob_result = self.action(c='overseastrade', m='world_rob',
                                                                 body={"id": id, "authorization": authorization})
                                        if rob_result['status'] != 1:
                                            print '打劫失败'
                                            continue
                                        else:
                                            self.p(rob_result)
                                            break

                else:
                    team_list = refresh_result['list']
                    for k, team in team_list.items():
                        for item in team:
                            if item:
                                # 只要有必定是两个船一起开
                                # print item['country_name'],item['member1_name'],item['member2_name']
                                if item['country_name'] in name + ['皇家酒店%d' % i for i in range(1, 80)] + ['dc%d' % i for
                                                                                                          i in
                                                                                                          range(1, 20)]:
                                    id = item['id']
                                    key = "rob" + uid + robkey + id
                                    authorization = hashlib.md5(key).hexdigest()
                                    rob_result = self.action(c='overseastrade', m='world_rob',
                                                             body={"id": id, "authorization": authorization})
                                    if rob_result['status'] != 1:
                                        print '打劫失败'
                                        continue
                                    else:
                                        self.p(rob_result)
                                        break
            except Exception as e:
                #self.p(self.action(c='overseastrade', m='refresh', p=i + 1))
                print e
                pass
    def jierihaiyun(self, user):  # 节日海外贸易
        self.action(c='message', m='index')
        index = self.action(c='overseastrade', m='index')
        # 购买粮食，花费银币的，id=1为粮食，id2-5为花费元宝的玛瑙等
        if int(index['info']['times']) > 0:
            while True:
                try:
                    info = self.action(c='overseastrade', m='renew', v=2018061901)
                    print json.dumps(info)
                    if info['reward'] > '3':  # and info['renew'] < '880':#封顶200元宝，如果不限制元宝要注释renew
                        self.action(c='overseastrade', m='buy_item', id=int(info['reward']))
                        break
                #    elif  info['renew'] > '80':
                #        self.action(c='overseastrade', m='buy_item', id=int(info['reward']))
                #        break
                except Exception as e:
                    break
            # 组队 ，检查是否有对， 有则加入，没有则创建 ，开始贸易
            # 1获取组队列表
            list_country = self.action(c='overseastrade', m='get_list_by_country', p=1)['list']

            # 加入贸易队伍，每页有四个框，为place：1-4，每个框有两个位置site:1-2，页数为page:1-10默认为1即可，
            print self.action(c="overseastrade", m='join_team', id=0, place=4, site=2, page=5)
            self.action(c="overseastrade", m='trade', v=0)  # 开启
            time.sleep(0.2)
        index = self.action(c='overseastrade', m='index')
        print '{} 剩余贸易次数：{}'.format(user, index['info']['times'])

    def peiyang(self, name, attribute='wuliup'):
        """
        :param gid: 武将名字
        :param attribute: 培养属性 'zhiliup','wuliup'
        :return:
        """
        print '开始培养'
        index = self.action(c='cultivate', m='index')
        for k, v in index['list'].items():
            print v['name']
            if v['name'] == name:
                gid = v['id']
                limit = str(int(v['level']) + 20)  # 属性值上限
                initnum = v[attribute]  # 当前值
                print limit, initnum
                while int(initnum) < int(limit):
                    print '=' * 20
                    index = self.action(c='cultivate', m='roll', mode=1, gid=gid)
                    print json.dumps(index)
                    roll = index['info'][attribute]
                    print '智力值是：', initnum, limit
                    print '剩余银币', index['info']['silver']
                    print 'roll 值', roll
                    if int(roll) <= int(initnum):
                        print '放弃'
                        self.action(c='cultivate', m='giveup', gid=gid)  # 放弃
                    else:
                        result = self.action(c='cultivate', m='save', gid=gid)  # 保存
                        initnum = roll
                        print '保存'
                        print json.dumps(result)
                print 'name: %s  属性值 %s' % (name, initnum)

    def matrix(self):
        genral_dict = {}
        matrix_index = self.action(c='matrix', m='index')
        general = matrix_index['general']
        for k, v in general.items():
            name = v['name']
            genral_dict[name] = v['id']
        return genral_dict

    def update_matrix(self, mid=4):
        genral_info = self.matrix()
        if mid != 4:
            print '下全部将领'
            lists = '0,0,0,0,0,0,0,0,0'
        else:
            lists = '%s,-1,%s,-1,%s,-1,%s,-1,%s' % (
                genral_info[u'蔡文姬'], genral_info[u'神周仓'], 0, 0, 0)
        print self.action(c='matrix', m='update_matrix', list=lists, mid=4)
        print self.action(c='matrix', m='use_matrix', mid=4)

    def years_guard(self):  # 周年守护签到
        self.action(c='years_guard', m='des_index')
        self.action(c='years_guard', m='sign_index')

    def fukubukuro(self):  # 周年福矿签到
        self.action(c='fukubukuro', m='index')
        self.action(c='fukubukuro', m='sign', type=1)
        self.action(c='fukubukuro', m='get_general', gid=360)

    def zhounianfukuang(self, username):  # 周年矿
        self.action(c='fukubukuro', m='index')
        self.action(c='fukubukuro', m='get_mine_discription')
        mineinfo = self.action(c='fukubukuro', m='mine')
        dateline = mineinfo['dateline']
        log = mineinfo['log']
        times = log['times']
        fukuangstatus = log['site']  # 为空说明没有下矿，反之已经占领矿
        if times == '0' and fukuangstatus == '0':
            print username, '未占矿，剩余次数为0'
            exit(1)
        elif times == '0' and fukuangstatus != '0':
            # 收取占领的矿
            print '收货抢劫矿'
            log_dateline = log['jointime']
            lasttime = int(dateline) - int(log_dateline)
            print lasttime
            if lasttime > 3600:
                print self.action(c='fukubukuro', m='harvest_mine', s=mineinfo['log']['site'])
                print '退出'
                exit(2)
        elif times != "0" and fukuangstatus != '0':
            log_dateline = log['jointime']
            lasttime = int(dateline) - int(log_dateline)
            print lasttime
            if lasttime > 3600:
                print self.action(c='fukubukuro', m='harvest_mine', s=mineinfo['log']['site'])
                for i in range(10, 0, -1):
                    mineinfo = self.action(c='fukubukuro', m='mine', p=i)['list']
                    for l in mineinfo:
                        if l['status'] == 0:
                            status = self.action(c='fukubukuro', m='action_mine', p=i, id=l['id'], t=l['type'])
                            if status['status'] != 1:
                                continue
                            else:
                                print '占矿'
                    #             exit(3)
        else:
            for i in range(10, 0, -1):
                mineinfo = self.action(c='fukubukuro', m='mine', p=i)['list']
                for l in mineinfo:
                    if l['status'] == 0:
                        status = self.action(c='fukubukuro', m='action_mine', p=i, id=l['id'], t=l['type'])
                        if status['status'] != 1:

                            continue
                        else:
                            print '占矿'
                            exit(3)
                # 占矿

    def robfukuang(self, username, countryname):  # 打劫周年礦城
        self.action(c='fukubukuro', m='index')
        self.action(c='fukubukuro', m='get_mine_discription')
        mineinfo = self.action(c='fukubukuro', m='mine')
        robtimes = mineinfo['log']['robtimes']  # 打劫次数
        dateline = mineinfo['dateline']
        log = mineinfo['log']
        times = log['times']
        fukuangstatus = log['site']
        print '剩余打劫次数为{times}'.format(times=times)
        if robtimes == "0" and fukuangstatus == "0":

            exit(1)
        elif robtimes != "0" and fukuangstatus == "0":
            for page in range(10, 0, -1):
                try:
                    info = self.action(c='fukubukuro', m='mine', p=page)['list']
                    for item in info:
                        try:
                            if item['status'] == 1 and item['country'] in countryname:
                                print '打劫'
                                status = self.action(c='fukubukuro', m='loot_mine', p=item['page'], id=item['id'],
                                                     t=item['type'])
                                if status['status'] != 1:
                                    continue
                                else:
                                    exit(3)
                        except Exception as e:
                            print 'aaaaaaaaaaaaaa', e
                except Exception as e:
                    print 'wwwwwwwwwww', e
        else:
            print '收矿'
            self.zhounianfukuang(username)

    def fq(self):  # 打劫周年礦城
        self.action(c='fukubukuro', m='index')
        self.action(c='fukubukuro', m='get_mine_discription')
        mineinfo = self.action(c='fukubukuro', m='mine')
        self.action(c='fukubukuro', m='give_up')

    def fukuang(self):
        info = self.action(c='fukubukuro', m='index')
        print json.dumps(info)

    def springshop(self, name=u'聊得'):  # 武將商城
        spring = self.action(c='springshop', m='index')['list']
        self.action(c='springshop', m='buy', id=1)
        # self.action(c='springshop', m='buy', id=1)
        self.action(c='springshop', m='buy', id=3)
        self.action(c='springshop', m='buy', id=10)
        self.action(c='springshop', m='buy', id=17)
        # for item in spring:
        #     if item['name'] == name:
        #         self.action(c='springshop', m='buy',id=item['id'])

    def znhh(self):
        # 周年喊话
        result = self.action(c='act_halloween', m='index')
        hammer = result['hammer']
        for i in range(int(result['candy'])):
            self.action(c='act_halloween', m='action_candy')
        for i in range(10):
            for i in range(1, 10):
                self.action(c='act_halloween', m='action_pumpkin', id=i)

    def zhounianshop(self):
        medal = self.action(c='fukubukuro', m='index')['medal']
        print medal
        # self.action(c='fukubukuro', m='shop', type=1,)
        # self.action(c='fukubukuro', m='shop', type=2, )
        self.action(c='fukubukuro', m='shop_buy', type=1, id=35)  # 天皇铠甲

    # self.action(c='fukubukuro', m='shop_buy', type=1, id=35)
    # self.action(c='fukubukuro', m='shop_buy', type=1, id=35)
    def fukubukuro(self):  # 周年将签到,
        print '周年将签到'
        try:
            self.action(c='fukubukuro', m='index')
            self.action(c='fukubukuro', m='sign', type=1)
            # 合成签到将领
            self.action(c='fukubukuro', m='get_general', gid=360)
        except:
            pass

    def tavern(self):  # 批量银币贸易
        self.action(c='tavern', m='trade_batch', option=1)

    def guozhan(self):
        self.action(c='siege', m='battle_prepare')
        self.action(c='siege', m='join_battle')

    def priceoversea(self):
        index = self.action(c='overseastrade', m='index')
        if index['rob']['price'] < 70:
            rest = self.action(c='overseastrade', m='buy')
            p(rest)
            if rest['status'] == 2:
                exit(1)
            self.priceoversea()
        else:
            print '%s alrealdy buy 3 times' % self.user

    def gold_time(self):
        self.action(c='gold_time', m='index')
        data = self.action(c='gold_time', m='sign_reward')
        for item in data['data']:
            if item['receive_status'] == 1:
                self.action(c='gold_time', m='receive_sign_reward', reward_id=item['id'])

    def get_audit_list(self):  # 国家审计同意
        audit = self.action(c='country', m='get_audit_list')
        print len(audit['list'])
        for member in audit['list']:
            """:type {1,2} 1同意，2 忽略"""
            uid = member['uid']
            print '同意 %s 加入国家' % member['nickname']
            self.action(c='country', m='audit', uid=uid, type=1)

    def friend(self):  # 好友在线列表
        result = self.action(c='friend', m='index', p=1, l=4)
        for item in result['list']:
            if item['online'] == 1:
                print item['nickname']
        stats = '{"status":1,"all_page":1,"list":[{"fuid":"14900008589783","online":0,"nickname":"\u6253\u53d1\u65f6\u95f41","level":"139","countryid":"14500000000027","country":"\u5171\u4ea7\u515a","job":"\u5efa\u4e49\u4e2d\u90ce\u5c06","tree":"1"}],"page":1,"all_number":100,"now_number":"1","online":0}'

    def challenge(self, uid):  # 切磋对手
        # uid 角色id号
        rest = self.action(c='challenge', m='action', uid=uid)
        info = rest['info']
        touid = uid
        report = info['report']
        win = info['win']
        # 发送世界战报
        if self.user != 'sunzi1' and win != -2:
            self.action(c='arena', m='send_to_chat', touid=touid, report=report, win=win)

    def information(self, uid):  # 获取角色vip
        # top = self.action(c='worldarena',m='index')#演武榜top10
        # top = self.action(c='country', m='get_member_list')#国家列表
        # top = self.action(c='act_kemari', m='kemari_rank')#蹴鞠排行榜
        top = self.action(c='friend', m='index', p=1, l=100)  # 好友列表
        # print json.dumps(top)
        # for info in top['top']:
        for info in top['list']:
            try:
                uid = info['uid']
            except:
                uid = info['fuid']
            player = self.action(c='information', m='index', uid=uid)['player']
            print '%s %s %s ' % (player['nickname'], player['level'], player['vip'])

    def usurp(self):  # 国家升官
        self.action(c='country', m='get_member_list')
        status = 1
        while status == 1:
            info = self.action(c='country', m='get_usurp_info')
            p(info)
            try:
                if info['type'] == 2:
                    break
            except:
                break
            rest = self.action(c='country', m='usurp')
            status = rest['status']

    def mount_stone(self):  # 符石合成
        try:
            index = self.action(c='mount_stone', m='index')
            allpage = index['allpage']
            rest = self.action(c='mount_stone', m='get_mount_by_page', page=allpage)
            # hecheng
            self.action(c='mount_stone', m='get_mount_by_page', page=allpage)
            stone_id = [i for i in range(61, 74)]
            for id in stone_id:
                merge_index = self.action(c='mount_stone', m='merge_index', id=id)
                if merge_index['status'] == 1:
                    num = merge_index['all_count']
                    if num > 0:
                        p(self.action(c='mount_stone', m='merge', id=id, num=num))
        except KeyError as e:
            pass

    def god(self):  # 战神殿
        self.action(c='god', m='index')
        self.action(c='god', m='entry')  # 报名

    def gjzb(self):  # 国家争霸
        self.action(c='country_gvg', m='index')
        self.p(self.action(c='country_gvg', m='member_entry'))

    def war(self):  # 武斗会
        self.action(c='war', m='index')
        self.action(c='war', m='entry')  # 报名争霸

    def treasuremap(self):  # 海运藏宝图
        """ type 1 2 3 对应上中下
            quality 1,2,3,4,5,6 对应级别， 6位红色
            m = exit_team 解散
            create_team  创建
            join_team tid=  加入指定队伍
            sale 出售宝图
        """
        result = self.action(c='treasuremap', m='index')
        # list 列表 返回数据为现有组队信息 ，列表对象为字典、
        # team_status 是否组队信息
        mapnum = int(result['num'])
        while mapnum > 0:
            result = self.action(c='treasuremap', m='index')
            # list 列表 返回数据为现有组队信息 ，列表对象为字典、
            # team_status 是否组队信息
            mapnum = int(result['num'])
            time.sleep(20)
            print '%s拥有藏宝图%s 个' % (self.user, mapnum)
            """
            {
                "status":1,
                "team_status":1,
                 "list":[
                    {
                        "id":"14500008515184",
                        "quality":"6",
                        "list":[
                            {
                                "id":"14901000482478",
                                "uid":"14500008515184",
                                "nickname":"南宫雪青",
                                "type":"2",
                                "quality":"6",
                                "dateline":"1563327573",
                                "isuse":"0",
                                "name":"神话藏宝图",
                                "level":"303",
                                "sale_price":242400,
                                "ismax":1
                            }
                        ]
                    },
                ],
                "map":{
                    "id":"14901000482396",
                    "uid":"14900008572777",
                    "nickname":"小东东",
                    "type":"2",
                    "quality":"6",
                    "dateline":"1563326749",
                    "isuse":"1",
                    "name":"神话藏宝图",
                    "level":"269",
                    "sale_price":215200,
                    "ismax":1
                },
                "team":{
                    "id":"14900008572777",
                    "quality":"6",
                    "list":[
                        {
                            "id":"14901000482396",
                            "uid":"14900008572777",
                            "nickname":"小东东",
                            "type":"2",
                            "quality":"6",
                            "dateline":"1563326749",
                            "isuse":"0",
                            "name":"神话藏宝图",
                            "level":"269",
                            "sale_price":215200,
                            "ismax":1
                        }
                    ]
                },
                "refresh_price":2,
                "num":"1",
                "add_silver":0,
                "add_fubi":0,
                "silver":"23917330837"
                }
            """
            try:
                maytype = result['map']['type']
                mapid = result['map']['id']
            except:
                # 没有藏宝图了
                return
            if result['team_status'] == 1:
                # 已经组队
                print '已经组队'
                continue
            if result['map']['quality'] == "6":
                # 如果现有藏宝图为最高级
                for item in result['list']:
                    # 遍历组队列表
                    if item['quality'] == "6":
                        # 如果队伍为最高级
                        typelist = []
                        for id in item['list']:
                            typelist.append(id['type'])
                        if maytype not in typelist:
                            reust = self.action(c='treasuremap', m='join_team', tid=item['id'])
                            if reust['status'] == 1:
                                if reust['finish'] == 1:
                                    print '拼图成功'
                                    self.treasuremap()
                            print '加入队伍'
                            continue
                self.action(c='treasuremap', m='create_team')
                print '创建队伍'
            else:
                self.action(c='treasuremap', m='sale', id=mapid)
                print '出手宝图残片'
                self.treasuremap()

    def advance(self):  # 宝石合成
        result = self.action(c='advanced', m='index')
        for item in result['list']:
            gid = item['id']
            for i in range(6):
                for t in range(1, 5):
                    for w in range(6):
                        print self.action(c='advanced', m='level_up', gid=gid, t=t)
                self.p(self.action(c='advanced', m='start_advanced', gid=gid))

    def newyearshop(self):
        print 'aaaaaa'
        self.action(c='newyear_act', m='index')
        index = self.action(c='newyear_act', m='shop')
        fuka = index['fuka']
        print '福币数', fuka
        if fuka > '100':
            count = int(fuka) % 100
            num = int(fuka) // 100
            for i in range(num):
                self.action(c='newyear_act', m='exchange', id=34)
            for i in range(count):
                self.action(c='newyear_act', m='exchange', id=33)
        else:
            for i in range(int(fuka)):
                self.action(c='newyear_act', m='exchange', id=33)

    def tavern(self):
        # self.action(c='tavern', m='get_list', page=1,perpage=9,tab=4)
        self.action(c='tavern', m='buy', generalid='105')  # 神甘宁

    def matrix(self):
        result = self.action(c='matrix', m='get_info', mid=4)
        m_level = int(result['matrix']['level'])
        if m_level < 5:
            for i in range(5 - m_level):
                self.action(c='matrix', m='levelup', mid=4)

    def gomuster(self):  # 武将出征
        index = self.action(c='muster', m='index', page=1, perpage=999)

        for k, v in index['list'].items():
            if v['name'] in ["神卢植", "神文丑", "神董卓", "神刘璋", "神周仓", "神甘宁"]:
                gid = v['id']
                self.action(c='muster', m='go_battle', gid=gid, confrim=0)

    def update_matrix(self, uid1, uid2, uid3, uid4, uid5, mid=4):

        genral_dict = {}
        matrix_index = self.action(c='matrix', m='index')
        general = matrix_index['general']
        for k, v in general.items():
            name = v['name']
            genral_dict[name] = v['id']
        genral_info = genral_dict
        try:
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
        except:
            print self.user

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
                    for monster_id in range(1, 11):  # 攻击精英怪
                        # 遍历十次小兵
                        try:
                            first_kill = self.action(c="copies", m="get_monster_info", id=id, diff_id=diff_id,
                                                     monster_id=monster_id, d="newequip")['info']['first_kill']
                            if first_kill == 1:
                                status = self.action(c="copies", m="pk", id=id, diff_id=diff_id,
                                                     monster_id=monster_id, d="newequip")
                                if status['status'] != 1:
                                    break
                        except Exception as e:
                            print e

        except Exception as e:
            print e

    def financing(self):
        # 购买理财
        formdata = {"product_id": 6}
        self.action(c='financing', m='index')
        self.p(self.action(c='financing', m='purchase', body=formdata))
    def get_financing(self):
        profit_list = self.action(c='financing',m='profit_list')
        product_id = profit_list['financing_id']
        formdata = {
            "product_id":product_id
        }
        profit_list = self.action(c='financing',m='profit',body=formdata)

    def act_parade(self):
        # 沙场点兵
        index = self.action(c='act_parade', m='index')
        if index['status'] != 1:
            print index['msg']
            return None
        # self.p(index)
        is_free = int(index['is_free'])
        if is_free > 0:
            self.action(c='act_parade', m='action', num=1)

    def mult_(self):
        # 批量分解战鼓
        ids = []
        index = self.action(c='equip_forge', m='resolve_index', d='newequip', type=2)
        for i in index['equiplist']:
            if i['name'] in ['铜腰鼓', '圆鼓']:
                ids.append(i['id'])

                formdata = {
                    "id": ids
                }
                result = self.action(c='drum_forge', m='resolve_mulit', body=formdata)
                if result['status'] != 1:
                    print result['msg']
                else:
                    for item in result['get_materials']:
                        print '获得 %s %s 个' % (item['name'], item['num'])

    def zimap(self):  # 获取图片
        # levev:7,11，14是红色sh关卡s:1-9，id:6
        # 扫荡金色以上5-9
        # 获取次数nowmaxtimes
        for level in range(8, 11):  # 遍历每一个图
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
                        print self.action(c='map', m='mission', l=level, s=i + 1, id=id)['info']
                    except KeyError:
                        continue

                    times = self.action(c='map', m='mission', l=level, s=i + 1, id=id)['info']['nowmaxtimes']
                    # times = self.action(c='map', m='mission', l=level, s=i + 1, id=id)['info']['maxtimes']#红色天赋
                    print '剩余扫荡次数 %s' % times
                    if times != 0:
                        # print 'gongji',level,i+1,id,times
                        print self.action(c='map', m='action', l=level, s=i + 1, id=id, times=times)

    def get_talent(self):
        # 获取关卡地图
        levelmap = [6, 7, 8, 9, 10, 14, 15, 16, 17, 19]
        try:
            # for l in range(18,25):
            for l in levelmap:
                site = len(self.action(c='map', m='get_scene_list', l=l)['list'])
                for i in range(1, site + 1):  # 遍历关卡图次数
                    for id in range(1, 11):
                        result = self.action(c='map', m='mission', l=l, s=i, id=id)
                        if result['status'] != 1:
                            self.p(result)
                            print l, i, id
                            continue
                        info = result['info']
                        try:
                            getitemname = info['getitemname']
                            quality = info['quality']
                            # print getitemname
                            if '天赋' in getitemname:
                                # self.p(result)
                                print l, i, id, quality, getitemname
                        except KeyError as e:
                            pass
        except KeyError as e:
            print e
            self.p(result)

    def get_reputatio(self):
        # 获取关卡地图
        levelmap = [6, 7, 8, 9, 10, 14, 15, 16, 17, 19]
        try:
            for l in range(12, 25):
                # for l in levelmap:
                site = len(self.action(c='map', m='get_scene_list', l=l)['list'])
                for s in range(1, site + 1):  # 遍历关卡图次数
                    for id in range(1, 11):
                        result = self.action(c='map', m='mission', l=l, s=s, id=id)
                        if result['status'] != 1:
                            self.p(result)
                            print l, s, id
                            continue
                        info = result['info']
                        try:
                            getitemname = int(info['gexp'])
                            exp = info['exp']
                            nowmaxtimes = info['nowmaxtimes']
                            print l, s, id, nowmaxtimes, getitemname, exp
                            # self.p(result)
                        except KeyError as e:
                            pass
        except KeyError as e:
            print e
            self.p(result)

    def island(self):  # 金银洞活动
        # 获取当前攻击的次数和金银守护者5的状态，是否为攻击过，如果为1则为可以攻击，为0 则表示不可以
        index = self.action(c='island', m='index')
        self.p(index)
        id = index['list'][4]['id']
        count = self.action(c='island', m='get_mission', id=id)['info']['act']
        self.p(count)
        id_open = index['list'][4]['openstatus']
        print id_open
        if count <= 50 and id_open != 1:
            for item in index['list']:  # 每日共计5次
                id_ = item['id']
                status = self.action(c='island', m='pk', id=id_)  # 共计金银洞
                self.p(status)
        id_open = self.action(c='island', m='index')['list'][4]['openstatus']
        if count <=500 and id_open == 1:
            for i in range(400):
                print i
                status = self. action(c='island', m='pk', id=id)  # 共计通过之后的最高金银洞5次
                if status['status']!=1:
                    return
        else:
            print '今天已经攻击了10次不在攻打'
    def shuaisland(self):
        index = self.action(c='island', m='index')
        id = index['list'][0]['id']
        for item in range(200):  # 每日共计5次
            print item
            self.action(c='island', m='pk', id=id)  # 共计金银洞

    def act_fight_lottery(self):
        #征战八方抽奖
        result = self.action(c='act_fight', m='index')
        lottery_num = int(result['lottery_num'])
        if lottery_num / 3 > 120:
            formdata = {"id": 1}
            result = self.action(c='act_fight', m='get_achievement_info')
            num = int(result['num'])
            if num > 200:
                return
            for i in range(200 - num):
                result = self.action(c='act_fight', m='lottery', body=formdata)
        self.p(result)
        for item in result['reward']:
            try:
                if int(item['status']) == 1:
                    formdata = {
                        "id": item['id']
                    }
                    result = self.action(c='act_fight', m='get_achievement_reward', body=formdata)
            except:
                self.p(item)

    def collect_cards(self):
        card_info = {
            'card1':'七',
            'card2':'周',
            'card3':'年',
            'card4':'快',
            'card5':'乐',
                     }
        self.action(c='seven_year',m='cake_index')
        collect_cards = self.action(c='seven_year',m='collect_cards')
        user_info = collect_cards['user_info']
        card1 = int(user_info['card1'])
        card2 = int(user_info['card2'])
        card3 =int(user_info['card3'])
        card4 =int(user_info['card4'])
        card5 =int(user_info['card5'])
        print "%s 七%s 、周 %s、年 %s、快 %s、 乐%s" %(self.user,card1,card2,card3,card4,card5)
        # if card5 >= 1:
        #     print self.user,'乐'
        #     self.give_cards(5)
    def friend(self):
        formdata = {
            'f':260000149847
        }
        self.action(c='friend',m='add_friend',body=formdata)
    def give_cards(self,card):
        formdata = {
            'uid':14900008572777,
            'card':card,
        }
        status = self.action(c='seven_year',m='give_cards',body=formdata)
        self.p(status)
    def seven_year(self):
        #每日签到
        self.action(c='seven_year',m='sign_index')
        self.action(c='seven_year',m='sign')
    def cake_index(self):
        #瓜分元宝
        index = self.action(c='seven_year',m='cake_index')
        result = self.action(c='seven_year',m='join_cake')
        if result['status'] == -3:
            self.p(result)
            time.sleep(10)
            self.cake_index()
    def poll_reward(self):#zongzi
           self.action(c='quyuan_festival',m='poll_index')
           self.action(c='quyuan_festival',m='poll_reward')
           self.action(c='quyuan_festival',m='take_poll')
# 周年比购物start_advanced

# def wx():#五行竞猜刷数据
# for i in range(100):
# id1 = random.randint(1, 5)
# id2 = random.randint(1, 12)
# sum = 0
# jin = 0
# mu = 0
# shui = 0
# huo = 0
# tu = 0
# for i in range(5):
#     infos = action.wuxing(id1,id2)
#     if infos['five_line']['id'] == "1":
#         jin += 1
#     elif infos['five_line']['id'] == "2":
#         mu += 1
#     elif infos['five_line']['id'] == "3":
#         shui += 1
#     elif infos['five_line']['id'] == "4":
#         huo += 1
#     elif infos['five_line']['id'] == "5":
#         tu += 1
#     sum +=infos['reward_num']
#     print infos['reward_num']
# print id1, id2
# print '共计：',sum - 10000
# print jin,mu,shui,huo,tu
# action.generalpool()
# action.fuka()
# action.messages()
if __name__ == '__main__':
    q = Queue()

    l = threading.Lock()


    def act(user, apass, addr):
        action = activity(user, apass, addr)
        action.get_talent()


    def task(user, apass, addr):  # 节节高买突飞
        action = activity(user, apass, addr)
        # action.actjubao()
        # action.morra()
        # action.gongxiang()
        # action.lottery()#抽奖
        # action.actjubao()
        # action.leigu()
        # action.shenshu()
        # action.qiandao()
        # action.actjubao()
        # action.island()
        # action.guyu()
        # action.gongxiang()
        # action.usebuff()
        # action.sign()
        # action.fuka(15)
        # action.fukubukuro()
        # action.holiday()
        # action.chicken()
        # action.years_guard()
        action.poll_reward()


    def zhujian(user, apass, addr):
        while True:
            action = activity(user, apass, addr)
            # action.unlock(413728)
            action.act_sword()


    def xinnain(user, apass, addr):
        action = activity(user, apass, addr)
        # action.leigu()
        # action.shenshu()
        action.newyearshop()


    def fanpai(user, apass, addr):
        action = activity(user, apass, addr)
        action.unlock(123456)
        action.fuka(2600)


    def haiyun(user, apass, add):
        action = activity(user, apass, add)
        # action.jierihaiyun(user)
        action.overseastrade()
        # action.countrymine()


    def jion(user, apass, addr):  # 加入腐败天朝
        action = activity(user, apass, addr)
        action.jioncountry(u'光芒神殿')


    def gongxian(user, apass, addr):
        action = activity(user, apass, addr)
        action.gongxiang()


    def panguo(user, apass, addr):
        action = activity(user, apass, addr)
        action.betray()


    def dajie(user, apass, addr):
        s1.acquire()
        print '%s 获取锁' % user
        action = activity(user, apass, addr)
        action.world_rob_redis(user,addr)
        # action.world_rob(
        #     ['体检了', '8523', '英雄', '是你学姐', '杰克傻bi', '杰克喝sui', '杰克喝尿', '杰克吃翔', 'haiyun1', 'haiyun2', 'haiyun3','haiyun4', '打船专用',
        #      '我乐个趣',
        #      '喔喔喔噢',
        #      '溜溜溜',
        #      '呵呵我来了啊',
        #      '呃呃呃',
        #      '打船专用',
        #      '1512412',
        #      '1241251',
        #      '234234',
        #      '12341',
        #      'shabi',
        #      'dc',
        #      '悍龙',
        #      '炎黄天都',
        #      '明',
        #      '若溪若溪',
        #      ], user)
        # # time.sleep(0.3)
        print('%s 释放锁') % user
        s1.release()


    def teshujianghun(user, apass, addr):
        action = activity(user, apass, addr)
        action.jianghun()


    def buff(user, apass, addr):
        action = activity(user, apass, addr)
        action.usebuff()


    def ylsanguo(user, apass, addr):
        action = activity(user, apass, addr)
        action.sanguo()


    def chats(user, apass, addr):
        action = activity(user, apass, addr)
        # action.chat('sssssse')
        # action.gxinfo()
        action.information(123)
        # action.get_audit_list()
        # action.chat(u"悍将三国六周年快乐")


    def upmatrix(user, apass, addr):  # 更新出征武将
        action = activity(user, apass, addr)
        action.update_matrix(mid=5)


    def guyuyinbi(user, apass, addr):  # 换古玉买银币
        action = activity(user, apass, addr)
        action.sign()  # 购买签到声望
        action.guyu()


    def countrycaikuang(user, apass, addr):  # 下国家矿
        action = activity(user, apass, addr)
        action.countrymine()


    def rolename(user, apass, addr):  # 更新出征武将
        action = activity(user, apass, addr)
        # nickname = 'mmp' + user.split('y0')[1]
        # nicklist = ['天','下','无','贼','越']
        nicklist = ['降临贡献']
        # nicklist = ['G更健康','G更好','G你倒是处理啊','哎呦喂G']
        name = user.split(r'gx', 1)
        if name[0] == 'gmsd':
            nickname = 'gmsd' + user.split(r'0', 1)[1]
            print nickname
            action.role(nickname)
        elif name[0] == 'lwzs':
            nickname = 'lwzs' + user.split(r'0', 1)[1]
            print nickname
            action.role(nickname)
        elif name[0] == 'cnm':
            nickname = 'nmp' + user.split(r'0', 1)[1]
            print nickname
            action.role(nickname)
        elif name[0] == 'dgj':
            nickname = 'dgj' + user.split(r'0', 1)[1]
            print nickname
            action.role(nickname)
        else:
            nickname = choice(nicklist) + name[1].title()
            print nickname
            action.role(nickname)


    def zhouniankuang(user, apass, addr):  # 更新出征武将
        action = activity(user, apass, addr)
        action.zhounianfukuang(user)


    def robfu(user, apass, addr):  # 更新出征武将
        action = activity(user, apass, addr)
        action.robfukuang(user,
                          ['英雄', '体检了', '杰克吃翔', '杰克喝尿', '悍龙', '是你学姐', '炎黄天都', '杰克喝sui', 'haiyun1', 'haiyun2', 'haiyun3',
                           '明'])


    def znshop(user, apass, addr):  # 周年福矿商店
        action = activity(user, apass, addr)
        action.fukubukuro()


    def practice(user, apass, addr):  # 武将突飞
        action = activity(user, apass, addr)
        action.tufei(u'神周仓', 100)


    def equip_strengthen(user, apass, addr):  # 强化，穿戴装备
        action = activity(user, apass, addr)
        gid, uid = action.general()  # 获取三级装备，再次强化，并给武将穿戴上
        for i in uid:
            for etype, v in i.items():
                # action.strengthen(v)
                action.equip(gid, v, etype)


    def getjingsu(user, apass, addr):
        action = activity(user, apass, addr)
        action.jingsu()
        action.levelgift()


    def buysea(user, apass, addr, lockpwd):
        action = activity(user, apass, addr)
        action.unlock(lockpwd)
        action.priceoversea()


    def goldtime(user, apass, addr):
        action = activity(user, apass, addr)
        action.gold_time()


    def shenguan(user, apass, addr):  # 国家升官
        action = activity(user, apass, addr)
        action.usurp()


    def godentry(user, apass, addr):  # 战神殿报名
        action = activity(user, apass, addr)
        action.god()


    def country_zb(user, apass, addr):  # 国家争霸
        action = activity(user, apass, addr)
        action.guozhan()


    def warentry(user, apass, addr):  # 武斗会报名
        action = activity(user, apass, addr)
        action.war()


    def mountStone(user, apass, addr):  # 石头合成
        action = activity(user, apass, addr)
        action.mount_stone()


    def wjc(user, apass, addr):  # 石头合成
        action = activity(user, apass, addr)
        action.advance()


    def pool(user, apass, addr):  # 武将池
        action = activity(user, apass, addr)
        action.update_matrix(u'神甘宁', u'神刘璋', u'神卢植', u'神周仓', u'神文丑', )


    def licai(user, apass, addr):  # 理财
        action = activity(user, apass, addr)
        # action.financing()
        action.get_financing()

    def dianbing(user, apass, addr):  # 沙场点兵
        action = activity(user, apass, addr)
        action.act_parade()


    def tianfu(user, apass, addr):  # 天赋碎片
        action = activity(user, apass, addr)
        action.zimap()
        action.hongmap()


    def pintu(user, apass, addr):  # 天赋碎片
        action = activity(user, apass, addr)
        action.treasuremap()

    def yuanbao(user, apass, addr):  # 元宝
        s1.acquire()
        action = activity(user, apass, addr)
        action.island()
        s1.release()


    def kapian(user, apass, addr):  # 周年卡片
        s1.acquire()
        action = activity(user, apass, addr)
        # action.seven_year()
        # action.cake_index()
        action.collect_cards()
        s1.release()
    def zhengzhangchoujiang(user, apass, addr):  # 征战八方抽奖
        s1.acquire()
        action = activity(user, apass, addr)
        action.act_fight_lottery()
        s1.release()
    def shijiejiangli(user, apass, addr):  # 世界奖励领奖
        s1.acquire()
        action = activity(user, apass, addr)
        action.message()
        s1.release()
    def py(user, apass, addr):  # 征战八方抽奖
        s1.acquire()
        action = activity(user, apass, addr)
        action.peiyang('神董卓')
        s1.release()
    s1 = threading.Semaphore(10)



    def chuan():
        with open('../users/user.txt', 'r') as f:
            # with open('../users/duguyi.txt', 'r') as f:
            for i in f:
                if i.strip() and not i.startswith('#'):
                    name = i.split()[0]
                    # name = i.split()[0]zr
                    passwd = i.split()[1]
                    try:
                        addr = i.split()[2]
                    except:
                        addr = None
                    try:
                        lockpwd = i.split()[3]
                    except:
                        lockpwd = None
                    #addr = 21
                    t1 = threading.Thread(target=userinfo, args=(name, passwd, addr))
                    t1.start()
                    # q.put(t1)


    def gm():
        cont = ['149cnm.txt', '149dgj.txt', '149gx1.txt', '149xx.txt', '149xb.txt', '149lwzs.txt', '148gx.txt']
        for t in cont:
            with open('../users/%s' % t, 'r') as f:
                for i in f:
                    if i.strip():
                        user = i.split()[0]
                        passwd = i.split()[1]
                        addr = i.split()[2]
                        # addr = 149
                        t1 = threading.Thread(target=kapian, args=(user, passwd, addr))
                        # t1.start()
                        q.put(t1)


    def dg():
        # cont = ['150.txt', '150num.txt', '150nm.txt', '150taohua.txt', '150bank.txt']
        # cont = ['autouser.txt', 'user.txt', 'alluser.txt', 'duguyi.txt', '149cnm.txt', '149dgj.txt', '149gx1.txt',
        # '149xx.txt',
        # '149xb.txt', '149lwzs.txt', '21user.txt', '150.txt', '150gx.txt', '150nm.txt', '150num.txt',
        # '150taohua.txt', '150bank.txt']
        cont = ['xing.txt']
        for t in cont:
            with open('../users/%s' % t, 'r') as f:
                for i in f:
                    if i.strip() and not i.startswith('#'):
                        user = i.split()[0]
                        passwd = i.split()[1]
                        addr = i.split()[2]
                        for i in range(5):
                            t1 = threading.Thread(target=userinfo, args=(user, passwd, addr))
                            q.put(t1)


    # chat('xingyue123', 413728161, 21)
    # chat('pock520',5553230,149)
    # chat('123456789', 987654321, 135)
    # dg()
    # gm()
    # chuan()
    with open('../users/xing.txt', 'r') as f:
        for i in f:
            if i.strip():
                name = i.split()[0]
                passwd = i.split()[1]
                addr = i.split()[2]
                t1 = threading.Thread(target=userinfo, args=(name, passwd, addr))
                t1.start()