#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2024/11/19 12:19
# @Author  : yuege
# @File    : 每日活动任务

import random
import threading
from Queue import Queue
import traceback

class jaderabbit_receivespring(object):
    """玉兔迎春"""
    def login_index(self,type=1):
        try:
            self.log.info('玉兔迎春')
            index= self.action(c='jaderabbit_receivespring',m='login_index')
            if index['status'] == 1:
                return index
            else:
                self.log.error(index['msg'])
                return False
        except:
            traceback.print_exc()
            self.log.error('玉兔迎春首页异常' + traceback.format_exc())
            return False
    def receive_login_reward(self,day=1):
        try:
            formdata={
                "day":day
            }
            index= self.action(c='jaderabbit_receivespring',m='receive_login_reward',body=formdata)
            if index['status'] == 1:
                self.log.info('玉兔迎春每日签到成功')
                return index
            else:
                self.log.error('玉兔迎春每日签到失败')
                self.log.error(index['msg'])
                return False
        except:
            traceback.print_exc()
            self.log.error('玉兔迎春每日签到异常' + traceback.format_exc())
            return False
    def chat(self,message):
        try:
            formdata = {
                "c": "chat",
                "m":"send",
                "message":message
            }
            index = self.action(c='chat', m='send', body=formdata)
            if index['status'] == 1:
                self.log.info('聊天消息发送成功:%s'%message)
                return index
            else:
                self.log.error(index['msg'])
                return False
        except:
            traceback.print_exc()
            self.log.error('玉兔迎春首页异常' + traceback.format_exc())
            return False

    def blessing_index(self, type=1):
        #common_blessing_word
        self.log.info('新春祝福')
        index = self.action(c='jaderabbit_receivespring', m='blessing_index')
        if index['status'] == 1:
            return index
        else:
            self.log.error(index['msg'])
            return False

    def auto_receive_login_reward(self):
        #
        login_index=self.login_index()
        if login_index:
            reward_list= login_index['reward_list']
            for item in reward_list:
                day = item['day']
                if item['status'] == 1:
                    result = self.receive_login_reward(day)
                    break
                elif item['status'] == 2:
                    self.log.info('第%s天已经完成签到'%day)
                    continue
        else:
            self.log.error('玉兔迎春自动签到失败')
    def receive_blessing_reward(self,type=1):
        formdata = {
            "type": type
        }
        index = self.action(c='jaderabbit_receivespring', m='receive_blessing_reward', body=formdata)
        if index['status'] == 1:
            self.log.info('新春祝福领取成功')
            return index
        else:
            self.log.error(index['msg'])
            return False

    def auto_receive_blessing_reward(self):
        #自动领取奖励
        blessing_index=self.blessing_index()
        if blessing_index:
            reward_list_status = blessing_index['reward_list'][0]['status']
            if reward_list_status ==0:
                #0表示为领取呢，就发消息领取
                    reward_list= blessing_index['common_blessing_word']
                    common_blessing_word = random.choice(reward_list)
                    result = self.chat(common_blessing_word)
                    if result:#消息发送失败就不需要领取了
                        self.receive_blessing_reward()
            elif reward_list_status == 2:
                self.log.info('玉兔迎春祝福已经领取')
            elif reward_list_status == 1:#符合条件了直接领取就行了
                self.receive_blessing_reward()
    def action_auto_jaderabbit_receivespringt(self):
        try:
            self.auto_receive_login_reward()
            self.auto_receive_blessing_reward()
        except Exception as e:
            traceback.print_exc()
            self.log.error('玉兔迎春签到异常' + traceback.format_exc())


class act11th_anniversary_lottery(object):
    def draw_reward_index(self,type=1):
        try:
            self.log.info('十一周年庆')
            index= self.action(c='act11th_anniversary_lottery',m='draw_reward_index')
            if index['status'] == 1:
                return index
            else:
                self.log.error(index['msg'])
                return False
        except:
            traceback.print_exc()
            self.log.error('十一周年庆异常' + traceback.format_exc())
            return False

    def shop_index(self, type=1):
        try:
            #shop_type = 10 是红包
            self.log.info('周年商城')
            index = self.action(c='act11th_anniversary', m='shop_index')
            if index['status'] == 1:
                return index
            else:
                self.log.error(index['msg'])
                return False
        except:
            traceback.print_exc()
            self.log.error('周年商城异常' + traceback.format_exc())
            return False

    def shop_lottery(self, type=1):
        try:
            #shop_type = 10 是红包

            index = self.action(c='act11th_anniversary', m='shop_lottery')
            if index['status'] == 1:
                self.log.info('开盲盒成功')
                return index
            else:
                self.log.info('开盲盒失败')
                self.log.error(index['msg'])
                return False
        except:
            traceback.print_exc()
            self.log.error('开盲盒异常' + traceback.format_exc())
            return False
    def lottery_index(self, type=1):
        try:
            #shop_type = 10 是红包
            self.log.info('福利抽奖')
            index = self.action(c='act11th_anniversary', m='lottery_index')
            if index['status'] == 1:
                return index
            else:
                self.log.error(index['msg'])
                return False
        except:
            traceback.print_exc()
            self.log.error('福利抽奖异常' + traceback.format_exc())
            return False
    def act11th_anniversary_lottery(self):
        try:
            #shop_type = 10 是红包
            self.log.info('开宝箱')
            index = self.action(c='act11th_anniversary', m='lottery')
            if index['status'] == 1:
                return index
            else:
                self.log.error(index['msg'])
                return False
        except:
            traceback.print_exc()
            self.log.error('开宝箱异常' + traceback.format_exc())
            return False
    def auto_act11th_anniversary_lottery(self):
        draw_reward_index = self.draw_reward_index()
        if draw_reward_index:
            shop_index = self.shop_index()
            if shop_index:
                shop_type = ''
                shop_detail = shop_index['shop_detail']
                for k,v in shop_detail.items():
                    shop_type = int(v['shop_type'])
                    break
                if shop_type == 10 :
                    self.log.info('当前抽奖为红包')
                    self.shop_lottery()
            lottery_index = self.lottery_index()
            if lottery_index:
                lottery_times = int(lottery_index['lottery']['lottery_times'])
                if lottery_times > 0 :
                    for i in range(lottery_times):
                        self.act11th_anniversary_lottery()

class luck_pk(object):
    def luck_pk_index(self,type=1):
        try:
            msg = "幸运比拼"
            self.log.info(msg)
            index= self.action(c='luck_pk',m='index')
            if index['status'] == 1:
                return index
            else:
                self.log.error(index['msg'])
                return False
        except:
            traceback.print_exc()
            self.log.error(msg + traceback.format_exc())
            return False

    def luck_pk_action(self, type=1):
        try:
            msg='幸运比拼抽取'
            self.log.info(msg)
            index = self.action(c='luck_pk', m='action')
            if index['status'] == 1:
                return index
            else:
                self.log.error(index['msg'])
                return False
        except:
            traceback.print_exc()
            self.log.error(msg + traceback.format_exc())
            return False


    def receive_luck_box(self, type=1):
        try:
            msg='幸运比拼领取礼包'
            self.log.info(msg)
            index = self.action(c='luck_pk', m='receive_luck_box')
            if index['status'] == 1:
                return index
            else:
                self.log.error(index['msg'])
                return False
        except:
            traceback.print_exc()
            self.log.error(msg + traceback.format_exc())
    def auto_luck_pk(self):
        index = self.luck_pk_index()
        if index:
            remain_times = index['remain_times']
            if remain_times >0:
                self.luck_pk_action()
            else:
                self.log.info('次数不足')
            self.receive_luck_box()