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
from const import catch_exception
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

    def get_map_status(self):
        map_index=self.action(c='map', m='index')
        shili_name=''
        gaunqia_name=''
        if map_index:
            l=1
            s=1
            id=1
            for k,v in map_index.items():
                try:
                    status =v['status']
                    pass_status = v['pass_status']
                    if status ==1 and pass_status == 0:
                        #表示当前攻击位置
                        shili_name= v['name']
                        l=k
                        break
                except :
                    pass
            formdata = {
                "l": l,
            }
            action_result = self.action(c='map', m='get_scene_list', body=formdata)
            for k,v in action_result['list'].items():
                status =v['status']
                openstatus = v['openstatus']
                if status ==0 and openstatus == 1:
                    #表示当前攻击位置
                    gaunqia_name= v['name']
                    s=v['stage']
                    break
            formdata = {
                "l": l,
                "s":s
            }
            action_result = self.action(c='map', m='get_mission_list', body=formdata)
            for k, v in action_result['list'].items():
                status = v['status']
                openstatus = v['openstatus']
                if status == 0 and openstatus == 1:
                    # 表示当前攻击位置
                    id = v['missionid']
                    break
            self.log.info('当期攻击关卡为%s%s l:%s,s:%s'%(shili_name,gaunqia_name,l,s))
            return int(l),int(s),int(id)
        else:
            self.log.error(map_index)
            return False

    def happy_double_festival(self):
        result = self.action(c='happy_double_festival', m='sign_index')
        sign = self.action(c='happy_double_festival', m='sign')

    def saodang(self, missionlevel=1, missionstage=1):  # 攻击小兵
        try:

            missionlevel,missionstage,missionid=self.get_map_status()
            for level in range(missionlevel, 13):  # 遍历每一个图
                result = self.action(c='map', m='get_scene_list', l=level)
                try:
                    site = len(result['list']) + 1
                except KeyError as e:
                    self.log.error('获取列表失败，l:%s'%level)
                    self.log.error(result)
                    return False
                for i in range(missionstage, site):  # 遍历关卡图次数
                    self.log.info('攻击进度 l:%s,s:%s' % (level, i))
                    status = 1
                    for id in range(missionid, 11):  # 遍历10个小兵
                        try:
                            # 获取首杀状态，1为首杀，-1为已经击杀
                            formdata ={
                                "l":level,
                                 "s":i,
                                "id":id
                            }
                            mission_result = self.action(c='map', m='mission',body=formdata)
                            if mission_result['status'] ==1:
                                try:
                                    first= mission_result['info']['first']
                                except:
                                    self.log.error('获取小怪信息失败%s,获取结果%s' % (formdata, mission_result))
                                    self.log.error(self.p(mission_result))
                                    exit(5)
                            elif mission_result['status'] == -4:
                                continue
                        except KeyError as e:
                            self.log.error('获取小怪信息失败%s,获取结果%s'%(formdata,mission_result))
                            return False
                        if first == 1 and status == 1: #
                            formdata = {
                                "l": level,
                                "s": i,
                                "id": id
                            }
                            action_result = self.action(c='map', m='action',body=formdata)
                            if action_result:
                                status = action_result['status']
                                if status == -5:
                                    self.log.error('攻击错误，参数%s' % str(formdata))
                                    self.log.error(action_result)
                                    exit_code = 2
                                    return exit_code
                                elif action_result['info']['win'] >0:
                                    self.log.info('成功击败小兵')
                                elif action_result['info']['win'] ==-3:
                                    self.log.info('攻击小兵失败')
                                    exit(5)
                            else:
                                self.log.error(action_result)
                                exit(222)
                           
                        else:
                            self.log.info('alredy kill')
                    missionid=1#重置通关的关卡小兵位置信息
                missionstage=1 #重置通关的关卡位置信息


        except Exception as e :
            traceback.print_exc()
            self.log.error('神武异常' + traceback.format_exc())
    def mapscene(self,level=1):  # 领取通关奖励
        self.action(c='map', m='get_scene_list', l=level, v=2018071801)
        self.action(c='map', m='get_newreward_index', levelid=1, v=2018071801)
        self.action(c='map', m='get_newreward', id=1, v=2018071801)
        self.action(c='map', m='get_newreward', id=2, v=2018071801)
        self.action(c='map', m='get_newreward', id=3, v=2018071801)
        self.action(c='map', m='get_newreward', id=4, v=2018071801)

    def levelgift(self):  # 获取等级奖励
        res=self.action(c='levelgift', m='index')  # 打开奖励页面
        for item in res['list']:
            if item['type'] == 1:
                self.action(c='levelgift', m='get_reward', level=item['level'])  # 获取30级奖励


    def muster(self, level=40):  # 添加武将并出征
        # gid武将id，pid那个槽位训练获取
        caiid = ''
        liaoid = ''
        gid = ''
        practtice_info = self.action(c='practice', m='index')
        # 初期都是两个训练槽位，
        pid = practtice_info['place']['1']['id']
        practice_stop_status= self.action(c='practice', m='practice_stop ', pid=pid)  # 终止训练
        if practice_stop_status['status'] ==1:
            self.log.info('终止训练成功')
        else:
            self.log.error('终止训练失败')
        # 获取武将
        self.action(c='levelgift', m='index')
        wujiang_index = self.action(c='muster', m='index', page=1, perpage=999)['list']
        for k, v in wujiang_index.items():
            if v['name'] == '神曹植':  # 蔡文姬
                self.action(c='muster', m='go_battle', gid=v['id'])
                self.action(c='matrix', m='index')
                gid = v['id']
            elif v['name'] == '廖化':
                self.action(c='muster', m='go_battle', gid=v['id'])
                liaoid = v['id']
            elif v['name'] == '张昭':
                print '找到张昭'
                gid = v['id']
        # lists = '0,%s,0,%s,0,0,0,0,0' % (gid, caiid)
        # status = self.action(c='matrix', m='update_matrix', list=lists, mid=4)
        # if status:
        #     self.log.info('出征成功')
        # 队武将突飞
        index_info = self.action(c='practice', m='index')
        # 训练武将，
        formdata = {
            "gid":gid,
            "pid":pid,
            "type":2
        }
        practice_start_status = self.action(c='practice', m='practice_start', body=formdata)

        if practice_start_status['status'] ==1 :
            self.log.info('训练成功')
        else:
            self.log.error('训练失败')
            self.log.error(practice_start_status)
        for k,v in index_info['list'].items():
            if v['name'] == '神曹植':

                freetimes = index_info['freetimes']  # 突飞卡
                isturn = index_info['list'][k]['isturn']  # 武将师是否到转生级别
                wjlevel = index_info['list'][k]['level']
                self.log.info('当前有突飞卡%s张，武将%s级'%(freetimes,wjlevel))
                status = 1
                while status == 1 and freetimes != 0:  # 队伍将进行突飞
                    if int(isturn) == 1 and int(wjlevel) <= level:
                        self.log.info('武将转生')
                        resutl_status=self.action(c='practice', m='turn', gid=gid)
                        if resutl_status['status'] ==1:
                            self.log.info('转生成功')
                        else:
                            self.log.error('转生失败')
                    self.action(c='practice', m='mop', times=100, gid=gid)
                    self.action(c='practice', m='mop', times=50, gid=gid)
                    self.action(c='practice', m='mop', times=10, gid=gid)
                    self.action(c='practice', m='mop', times=5, gid=gid)
                    index_info = self.action(c='practice', m='index')
                    freetimes = index_info['freetimes']
                    info = self.action(c='practice', m='go_leap', gid=gid)  # 武将突飞一次
                    status = info['status']
                    if status == 1:
                        self.log.info('武将突飞成功')
                    else:
                        self.log.error('武将突飞失败')
                        self.log.error(info)

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
            # 判断是否穿戴装备
            if etype1:
                equipments1 = sorted(etype1.items(), key=lambda etype: etype[0])
                eid.append({"1": equipments1[0][1]['id']})  # 第一个就就是最好的装备
        else:
            eid.append({"1": info['list']['1']['eid1']['id']})
        if info['list']['1']['eid2'] == 0 or info['list']['1']['eid2'] == "0":
            if etype2:
                equipments2 = sorted(etype2.items(), key=lambda etype: etype[0])
                eid.append({"2": equipments2[0][1]['id']})
        else:
            eid.append({"2": info['list']['1']['eid2']['id']})
        if info['list']['1']['eid3'] == 0 or info['list']['1']['eid3'] == "0":
            if etype3:
                equipments3 = sorted(etype3.items(), key=lambda etype: etype[0])
                eid.append({"3": equipments3[0][1]['id']})
        else:
            eid.append({"3": info['list']['1']['eid3']['id']})
        if info['list']['1']['eid4'] == 0 or info['list']['1']['eid4'] == "0":
            if etype4:
                equipments4 = sorted(etype4.items(), key=lambda etype: etype[0])
                eid.append({"4": equipments4[0][1]['id']})
        else:
            eid.append({"4": info['list']['1']['eid4']['id']})

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
        self.log.info('当前装备强化等级%s'%newlevel)
        try:
            while int(newlevel) < levelinfo:
                strenthinfo = self.action(c='strengthen', m='strengthen_start', id=id, ratetype=0)
                newlevel = strenthinfo['newlevel']
                self.log.info('强化等级%s'%newlevel)
        except KeyError as e:
            self.log.info('已经强化到最高级%s'%newlevel)

    def equip(self, gid, eid, etype):  # 给武将穿戴装备
        self.action(c='general', m='equip', gid=gid, eid=eid, etype=etype)

    def unequip(self, gid, eid, etype):
        self.action(c='general', m='unequip', gid=gid, eid=eid, etype=etype, position=etype)

    def mainquest(self):  # 领取所有活动奖励
        mainquest_info = self.action(c='mainquest', m='index')
        self.log.info('领取所有活动奖励')
        for i in mainquest_info['list']:
            if int(i['status']) == 1:  # 获取奖励
                self.action(c='mainquest', m='get_task_reward', id=i['task_id'])
                self.log.info('领取奖励%s'%i['task_id'])
    def twentyyear_shop(self):
        self.action(c='twentyyear_shop',m='index')
        self.action(c='twentyyear_shop',m='free_onece_mall')

        formdata = {
            "id": 1,
            "free_id": 4,
        }
        action_result = self.action(c='twentyyear_shop', m='buy_free_onece', body=formdata)
        status = action_result['status']
        if status == 1:
            self.log.info('购买宝石声望成功')
        else:
            self.log.info('购买宝石声望失败')

    def tavern(self):
        self.action(c='twentyyear_shop',m='index')
        self.action(c='twentyyear_shop',m='free_onece_mall')

        formdata = {
            "page": 1,
            "perpage": 9,
            "tab":4
        }
        action_result = self.action(c='tavern', m='get_list', body=formdata)
        status = action_result['status']
    def tavernbuy(self):
        self.tavern()
        formdata = {
            "generalid": 138
        }
        action_result = self.action(c='tavern', m='buy', body=formdata)
        status = action_result['status']
        if status == 1:
            self.log.info('购买神曹植成功')
        else:
            self.log.info('购买神曹植失败')
    def go_battle(self,name):
        wujiang_index = self.action(c='muster', m='index', page=1, perpage=999)['list']
        for k, v in wujiang_index.items():
            if v['name'] == name:  # 蔡文姬
                go_battle_result=self.action(c='muster', m='go_battle', gid=v['id'])
                if go_battle_result['status']==1:
                    self.log.info('%s出征成功'%name)
                    return go_battle_result
                else:
                    self.log.error('%s出征失败'%name)
                    return False

    @catch_exception
    def matrix(self):
        # 出征将领
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


    def update_matrix(self, uid1, uid2, uid3, uid4, uid5, mid=4):
        self.log.info('武将上阵%s,%s,%s'%(uid1,uid2,uid3))
        genral_info = self.matrix()

        lists2 = '%s,%s,%s,-1,%s,-1,-1,%s,-1' % (
            genral_info[uid1],
            genral_info[uid2],
            genral_info[uid3],
            uid4,
            uid5,
        )
        lists4 = '%s,-1,%s,-1,%s,-1,%s,-1,%s' % (
            genral_info[uid1],
            genral_info[uid2],
            genral_info[uid3],
            uid4,
            uid5,
        )
        self.log.info('没有运行%s'%lists4)
        if mid == 2:
            status= self.action(c='matrix', m='update_matrix', list=lists2, mid=mid)
        elif mid == 4:
            status= self.action(c='matrix', m='update_matrix', list=lists4, mid=mid)
        self.log.info('没有运行')
        if status['status'] == 1:
            self.log.info("武将上阵成功")
        else:
            self.log.info("武将上阵失败")
    @catch_exception
    def use_case(self, mid=4, case=1):
        formdata = {
            "case": case,
            "mid": mid,
            "token": self.token
        }
        result = self.action(c='matrix', m=self.get__function_name(), body=formdata)
        return result

    @catch_exception
    def case_index(self, case=1):
        #阵法详情
        formdata = {
            "case": case,
            "token": self.token
        }
        result = self.action(c='matrix', m=self.get__function_name(), body=formdata)
        return result

    @catch_exception
    def levelup(self):
        formdata = {
            "case": 1,
            "mid": 4,
            "token": self.token
        }
        result = self.action(c='matrix', m=self.get__function_name(), body=formdata)
        return result
    @catch_exception
    def get_info_case(self):
        formdata = {
            "case": 1,
            "mid": 4,
            "token": self.token
        }
        result = self.action(c='matrix', m=self.get__function_name(), body=formdata)
        return result

    def happy_double_festival(self):
        result = self.action(c='happy_double_festival', m='sign_index')
        sign = self.action(c='happy_double_festival', m='sign')


def run(user, apass, addr,lockpwd):
    log = MyLog(logname='jingsu.log', level=logging.INFO)
    log.filter_.username=user
    log.filter_.addr= addr
    god_weapon_catalog.pwd = lockpwd
    #
    try:
        action = god_weapon_catalog(user, apass, addr,log)
        try:
            action.happy_double_festival()
            memberindex = action.action(c='member', m='index')
            missionlevel = int(memberindex['missionlevel'])
            missionsite = int(memberindex['missionsite'])
            missionstage = int(memberindex['missionstage'])
            log.info('账号：%s 等级：%s,l:%s,s:%s,id:%s' % (user, action.level(),missionlevel,missionstage,missionsite))
        except Exception as e:
            print 'zhanghao ###################################### ', user
        # action.happy_double_festival()
        # 购买两次石头和声望，之后购买神曹植
        # action.twentyyear_shop()
        # action.twentyyear_shop()
        # action.tavernbuy()
        #切换为策略攻击阵法
        # action.go_battle('神曹植')
        # action.case_index()
        # action.use_case()
        # action.get_info_case()
        # for i in range(5):
        #     #阵法升级5次
        #     action.levelup()
        # action.update_matrix(u'神曹植',u'蔡文姬',u'廖化',0,0)
        # if action.level() >= 157:
        #     exit()
        # if action.level() < 10:
        #     log.info('角色小于10级')
        #     action.saodang(missionlevel, missionstage )  # 16级 失败退出
        #     action.levelgift()  # 领取16级奖励
        #     # 扫荡失败以后获取2级别装备，然后强化后并穿戴上去
        # if action.level() < 25:
        #     log.info('角色小于25级')
        #     gid, uid = action.general(7)  # 第一次的都是2级装备
        #     print gid, uid
        #     for i in uid:
        #         for etype, v in i.items():
        #             action.strengthen(v)
        #             action.equip(gid, v, etype)
        #     action.saodang(missionlevel, missionstage )   # 26级失败退出
        #     for i in uid:
        #         for etype, v in i.items():
        #             action.strengthen(v)
        # if action.level() < 35:
        #     log.info('角色小于35级')
        #     action.mapscene(missionlevel)  # 领取通关奖励
        #     action.levelgift()  # 领取30级奖励
        #     action.muster()  # 武将出征并上阵，并突飞到30级
        #     # action.morra()#节节高
        #     gid, uid = action.general(25)  # 获取三级装备，再次强化，并给武将穿戴上
        #     for i in uid:
        #         for etype, v in i.items():
        #             action.strengthen(v)
        #             action.equip(gid, v, etype)
        #         action.saodang(missionlevel, missionstage )   # 级失败退出
        #     for i in uid:
        #         for etype, v in i.items():
        #             action.strengthen(v)
        #             action.equip(gid, v, etype)
        #     action.saodang(missionlevel, missionstage )   # 30级失败退出从第二个图开始
        # if action.level() < 50:
        #
        #     for i in range(2):
        #         action.mainquest()  # 获取所有活动
        #     gid, uid = action.general(25)  # 获取25级需要穿戴的装备强化
        #     for i in uid:
        #         for etype, v in i.items():
        #             action.strengthen(v)
        #             action.equip(gid, v, etype)
        #     action.muster()  # 再次突飞
        #     action.saodang(missionlevel, missionstage )
        if 50 <action.level() < 70:  # 领取前60次奖励

            # action.muster()#对武将突飞
            # #action.morra()  # 节节高
            # for i in range(3):#循环领取通过奖励
            #     action.mainquest()
            for i in range(4, 13):
                action.levelgift()  # 领取60级奖励
            # 获取竞速元宝
            for i in range(10, 120, 10):
                action.action(c='map', m='get_mission_reward', id=i)

            #         action.strengthen(eid1_quality_equipments)#强化装备
            # action.strengthen(general_index_list['eid1']['id'])
            action.saodang(missionlevel, missionstage )
        if 70 <= action.level() < 120:  # 领取前60次奖励
            # action.muster(level=80)
            # gid, uid = action.general(25)  # 获取三级装备，再次强化，并给武将穿戴上
            # for i in uid:
            #     action.strengthen(i)
            for i in range(3):  # 循环领取通过奖励
                action.mainquest()
            for i in range(4, 13):
                action.levelgift()  # 领取60级奖励
            action.saodang(missionlevel, missionstage )
            # 获取竞速元宝
            for i in range(10, 120, 10):
                action.action(c='map', m='get_mission_reward', id=i)
        if 120 < action.level() < 130:  # 领取前60次奖励
            # action.muster(level=140)
            action.saodang(missionlevel, missionstage )
        if 130  < action.level() < 140:  # 领取前60次奖励
            # action.muster(level=140)
            action.saodang(missionlevel, missionstage )

        if 140 < action.level() < 170 :  # 领取前60次奖励
            # action.mainquest()
            # action.tujian()
            # action.soul()
            action.mapscene()  # 领取通关奖励
            # action.muster(level=90)
            # 获取竞速元宝
            for i in range(10, 180, 10):
                a= action.action(c='map',m='get_mission_reward',id=i)
            action.saodang(missionlevel, missionstage )

    except Exception as e:
        traceback.print_exc()
        log.error('竞速异常' + traceback.format_exc())


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

