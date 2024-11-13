#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023/11/27 12:19
# @Author  : xingyue
# @File    : 神兵图录副本


from task.base import SaoDangFb
import time
import threading
from Queue import Queue
import  os,configparser
import traceback
from logging.handlers import RotatingFileHandler
import logging

config= configparser.ConfigParser()
config_file = '%s/conf/conf.ini' % (os.path.dirname(os.path.abspath(__file__)))

config.read(config_file,encoding='utf-8')
class ContextFilter(logging.Filter):

    username = 'USER'
    addr = 'ADDR'

    def filter(self, record):
        record.addr = self.addr
        record.username = self.username
        return True

def my_listener(event):
    if event.exception:
        print('The job crashed :(') # or logger.fatal('The job crashed :(')
    else:
        print('The job worked :)')



class MyLog(object):
    def __init__(self,level=logging.INFO,logpath=None, logname='mylog.log'):
        if logpath:
            if not os.path.exists(logpath):
                os.makedirs(logpath)
                self._log = os.path.join(logpath, logname)
            else:
                self._log = os.path.join(logpath, logname)
        else:
            self._log = logname

        self.filter_ = ContextFilter()
        self.logger = logging.getLogger(__name__)
        # 这为清空当前文件的logging 因为logging会包含所有的文件的logging
        logging.Logger.manager.loggerDict.pop(__name__)
        self.logger.handlers = []
        # 然后再次移除当前文件logging配置
        self.logger.removeHandler(self.logger.handlers)
        self.logger.addFilter(self.filter_)
        self.logger.setLevel(level)
        self.format = logging.Formatter(
            '%(asctime)s %(filename)s[line:%(lineno)d] [%(username)s:%(addr)s] %(levelname)s %(message)s')



    def console(self,level,message):
        ch = logging.StreamHandler()
        ch.setFormatter(self.format)

        fh = RotatingFileHandler(self._log, mode='a', maxBytes=1024 * 1024 * 1024, backupCount=3, encoding='utf-8')
        fh.setFormatter(self.format)
        self.logger.addHandler(fh)
        self.logger.addHandler(ch)
        if level == 'info':
            self.logger.info(message)
        elif level == 'debug':
            self.logger.debug(message)
        elif level == 'warning':
            self.logger.warning(message)
        elif level == 'error':
            self.logger.error(message)
        # 这两行代码是为了避免日志输出重复问题
        self.logger.removeHandler(ch)
        self.logger.removeHandler(fh)
        # 关闭打开的文件
        fh.close()

    def debug(self, message):
        self.console('debug', message)

    def info(self, message):
        self.console('info', message)

    def warning(self, message):
        self.console('warning', message)

    def error(self, message):
        self.console('error', message)


class god_weapon_catalog(SaoDangFb):
    def __init__(self,user, passwd, num,log,lockpwd=None):
        super(god_weapon_catalog,self).__init__(user, passwd, num)
        self.log = log
        self.lockpwd = lockpwd
    def unlock(self, pwd):
        return self.action(c='member', m='resource_unlock', pwd=pwd)
    def action(self, body=0, **kwargs):
        """动作参数m={'index':'获取基础账号密码等信息',‘get_monster_list’：“获取副本怪物列表信息”}
        """
        action_data = kwargs
        try:
            postresult = self.post_url(body, action_data)
            serverinfo = postresult.json(encoding="UTF-8")
            if serverinfo == 403:
                time.sleep(3)
                # 重新初始化
                self.token = self.get_token(self.num, self.user, self.passwd)
                postresult = self.post_url(body, action_data)
                serverinfo = postresult.json(encoding="UTF-8")
            try:
                status = int(serverinfo['status'])
                if status == 1 or status == 0:
                    return serverinfo
                elif status == 101:
                    #有准备锁，进行解锁
                    resutl = self.unlock(self.lockpwd)
                    if resutl['status'] == -1:
                        #解锁失败
                        return False
                    else:
                        #解锁后重新调用一次
                        self.action(body=0, **kwargs)
                else:
                     pass
            except Exception as e:
                pass
            return serverinfo
        except Exception as e:
            self.log.error('登陆失败')

    def ticket_shop_index(self,type=1):
        self.log.info('门票商店')
        formdata = {
            "type":type
        }
        index= self.action(c='god_weapon_catalog',m='ticket_shop_index',body=formdata)
        if index['status'] == 1:
            return index
        else:
            self.log.error(index['msg'])
            return False

    def index(self):
        self.log.info('进入神兵图录')
        index= self.action(c='god_weapon_catalog',m='index')
        if index['now_copy']:
            copy_name = index['now_copy']['copy_name']  # 副本名字
            now_speed = index['now_copy']['now_speed']  # 副本进度
            floor = index['now_copy']['floor']  # 层数
            integral = index['now_copy']['integral']  # 积分
            income_add = index['now_copy']['income_add']  # 当前战斗积分收益
            self.log.info("当前正在探索" + copy_name + "(" + floor + "层)" +"积分"+integral+"当前战斗积分收益"+income_add+ "副本进度" + now_speed)
        if index['status'] == 1:
            return index
        else:
            self.log.error(index['msg'])
            return False
    def buy_ticket(self,id=1):
        formdata = {
            "id": id
        }

        index= self.action(c='god_weapon_catalog',m='buy_ticket',body=formdata)
        self.log.info('购买门票')
        if index['status'] == 1:
            return index
        else:
            self.log.error(index['msg'])
            return False
    def explore_start(self,copy_id=1,floor=5):
        self.log.info('进入探索选路')
        formdata= {
            "copy_id": copy_id,
            "floor": floor
        }
        index= self.action(c='god_weapon_catalog',m='explore_start',body=formdata)
        if index['status'] == 1:
            return index
        else:
            self.log.error(index['msg'])
            return False
    def select_route(self,copy_id=1,floor=5,event_id=1,route_id=2):
        self.log.info('选路')
        formdata = {
            "copy_id": copy_id,
            "floor": floor,
            "event_id": event_id,
            "route_id": route_id
        }
        index= self.action(c='god_weapon_catalog',m='select_route',body=formdata)
        if index['status'] ==1:
            self.log.debug(index)
            return  index
        else:
            self.log.error(index['msg'])
            return False
    def battle_start(self,copy_id=1,floor=5,event_id=2):
        self.log.info('战斗')
        formdata = {
            "copy_id": copy_id,
            "floor": floor,
            "event_id": event_id
        }

        index= self.action(c='god_weapon_catalog',m='battle_start',body=formdata)

        if index['status'] ==1 and index['battle']['assess'] >0:
            copy_name = index['copy_name']  # 副本名字
            now_speed = index['now_speed']  # 副本进度
            floor = str(index['floor'])  # 层数
            integral = str(index['integral'])  # 积分
            income_add = str(index['income_add'])  # 当前战斗积分收益
            self.log.info(
                "战斗完成,当前正在探索" + copy_name + "(" + floor + "层)" + "积分" + integral + "当前战斗积分收益" + income_add + "副本进度" + now_speed)
            return  index
        elif index['status'] ==1 and index['battle']['assess'] <0:
            self.log.info('战斗失败，退出程序')
            return False
        else:
            self.log.error(index['msg'])
            return False
    def open_box(self,copy_id=1,floor=5,event_id=2):
        self.log.info('开箱')
        formdata = {
            "copy_id": copy_id,
            "floor": floor,
            "event_id": event_id
        }
        index= self.action(c='god_weapon_catalog',m='open_box',body=formdata)
        if index['status'] == 1:
            self.log.debug(index)
            return index
        else:
            self.log.error(index['msg'])
            return False

    def make_god_weaponry(self):
        self.log.info('打造神兵')
        index= self.action(c='god_weapon_catalog',m='make_god_weaponry')
        if index['status'] == 1:
            self.log.debug(index)
            get_reward = index['get_reward']['reward_info']['name']
            self.log.info(get_reward)
            return index
        else:
            self.log.error(index['msg'])
            return False
    def leave_copy(self):
        self.log.info('退出副本')
        index= self.action(c='god_weapon_catalog',m='leave_copy')
        if index['status'] == 1:
            return index
        else:
            self.log.error(index['msg'])
            return False
    def action_auto_start(self,route,times=3,**kwargs):
        try:
            """
            event_status 所有事件完成状态1未完成2完成所有事件
            event_type 事件类型1选路2宝箱3怪物
            event_info 有mission_id 就不用 选路，没有就需要选路
            explore_status  探索状态0未在探索中1探索中2完成所有事件, 但还未点击退出副本, 跳到打造神兵界面
            """
            index = self.index()
            now_copy = index['now_copy']
            floor = now_copy['floor']
            event_id = now_copy['event_id']
            event_type = int(now_copy['event_type'])
            copy_id = now_copy['copy_id']
            event_info=index['event_info']
            now_speed = now_copy['now_speed']
            explore_status = index['explore_status']
            if explore_status ==1:
                if event_type ==1:
                    #事件进行中需要选路
                    try:
                        event_info_type = index['event_info']['type']
                    except Exception as e:
                        select_route = self.select_route(copy_id=copy_id,floor=floor,event_id=event_id,route_id=route)
                        if select_route:
                            self.action_auto_start(route,select_route=select_route)
                        else:
                            return False
                elif event_type ==2 and not event_info:
                    self.log.info('需要开箱子')
                    #需要开箱子
                    self.open_box(copy_id=copy_id,floor=floor,event_id=event_id)
                    self.action_auto_start(route)
                elif event_type ==3 and  event_info:
                        while True:
                            battle_start = self.battle_start(copy_id=copy_id, floor=floor, event_id=event_id)
                            self.log.debug(battle_start)
                            if battle_start:
                                event_type = int(battle_start['event_type'])
                                event_info = battle_start['event_info']
                                event_id = int(battle_start['event_id'])
                                now_speed  = battle_start['now_speed']
                                event_status  =battle_start['event_status']
                                if event_status ==2:
                                    #完成所有事件领奖
                                    while times > 0:
                                        if self.make_god_weaponry():
                                            times -= 1
                                        else:
                                            self.leave_copy()
                                            return True
                                    self.leave_copy()
                                    return True
                                else:
                                    if event_type == 2 and not event_info:
                                        # 需要开箱子，返回第一步重新执行
                                        self.open_box(copy_id=copy_id, floor=floor, event_id=event_id)
                                        self.action_auto_start(route)
                                        break
                                    elif event_type == 1 :
                                        result = self.select_route(copy_id=copy_id, floor=floor, event_id=event_id,
                                                                   route_id=route)
                                        self.action_auto_start(route)
                                        break
                            else:
                                self.log.error("自动战斗异常，程序退出")
                                break
            elif explore_status ==2 :
                while times > 0:
                    if self.make_god_weaponry():
                        times -= 1
                    else:
                        self.leave_copy()
                        return True
                self.leave_copy()
                return  True
        except Exception as e:
            traceback.print_exc()
            self.log.error('神兵图录异常' + traceback.format_exc())

def run(user, apass, addr,lockpwd):
    log = MyLog(logname='shenbingtulu.log', level=logging.INFO)
    log.filter_.username=user
    log.filter_.addr= addr
    god_weapon_catalog.pwd = lockpwd
    #

    try:
        action = god_weapon_catalog(user, apass, addr,log)
        if action.level() < 360:
            log.error('等级不足360,无法进入!')
            return False
        #获取攻打副本名字
        copy_name = config.get('god_weapon_catalog', 'copy_name')
        #获取攻打副本的层数
        floor = int(config.get('god_weapon_catalog', 'floor'))
        #获取神兵铸造次数
        times = int(config.get('god_weapon_catalog', 'times'))
        #获取选路
        route_name = config.get('god_weapon_catalog', 'select_route')
        route_dict = {
            u"艰险之路": 2,
            u"崎岖之路": 1
        }
        route = route_dict[route_name]
        log.info('当前设定探索' + copy_name + '第' + str(floor) + '层' + route_name)
        time.sleep(2)
        index = action.index()
        if index['status'] ==1:
            #explore_status 探索状态0未在探索中1探索中2完成所有事件, 但还未点击退出副本, 跳到打造神兵界面
            explore_status = index['explore_status']
            if explore_status == 0:
                # 如果不在带副本里,开始第一次副本，选路
                # 普通门票
                ticket1 = int(index['ticket1'])
                # 高级门票
                ticket2 = index['ticket2']
                # 聚宝盆币
                ticket3 = index['ticket3']
                log.info("当前有普通门票：{ticket1},高级门票：{ticket2},聚宝盆币：{ticket3}".format(ticket1=ticket1, ticket2=ticket2,
                                                                               ticket3=ticket3))
                time.sleep(1)
                is_buy_ticket = config.get('god_weapon_catalog', 'is_buy_ticket')
                if is_buy_ticket == '是':
                    # 是否购买门票
                    shop_type = int(config.get('god_weapon_catalog', 'shop_type'))
                    ticket_shop_index = action.ticket_shop_index(shop_type)
                    if ticket_shop_index['status'] == 1:
                        id = 1
                        action.buy_ticket(id)
                    else:
                        log.error(ticket_shop_index['msg'])
                log.info('准备探索' + copy_name)
                for item in index['copy_info']:
                    if item['name'] == copy_name:
                        # 通过设置的copy_name 获取id
                        copy_id = item['copy_id']
                        need_ticket = int(item['need_ticket'])
                        if ticket1 < need_ticket:
                            log.warning('门票不足进入第' + str(floor) + '层')
                            break
                        else:
                            action.explore_start(copy_id, floor)
                            log.info("开始进行自动探索")
                            action.action_auto_start(route)
                            break
            elif explore_status == 1:
                log.info("开始进行自动探索")
                action.action_auto_start(route)
            elif explore_status == 2:
                while times > 0:
                    if action.make_god_weaponry():
                        times -= 1
                    else:
                        action.leave_copy()
                        return True
                action.leave_copy()
                return True
        else:
            log.error(index['msg'])
            return False

    except Exception as e:
        traceback.print_exc()
        log.error('神武异常' + traceback.format_exc())


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

