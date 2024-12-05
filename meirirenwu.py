#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/2/11 12:19
# @Author  : xingyue
# @File    : 日常任务领取.py.py
import random

from stringold import lower

from task.base import SaoDangFb
import datetime
import time
import traceback
import threading
from Queue import Queue
import  os
from logging.handlers import RotatingFileHandler
import logging
import json,sys
import codecs


#from utils.questanwer import answer


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
    def __init__(self,level=logging.INFO,logpath=None, logname='meirirenwu.log'):
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



datilog = MyLog(logname='meiridati.log', level=logging.INFO)
# 假设json_file_path是你的JSON文件的路径
json_file_path = '/root/meiridati.json'

# 使用with语句确保文件正确关闭
with codecs.open(json_file_path, 'r+', 'utf-8') as file:
    data = json.load(file)




class rewary(SaoDangFb):
    def __init__(self,user, passwd, num,log,lockpwd=None):
        super(rewary,self).__init__(user, passwd, num)
        self.log = log
        self.lockpwd = lockpwd
    def unlock(self, pwd):
        return self.action(c='member', m='resource_unlock', pwd=pwd)
    def action(self, body=0, **kwargs):
        """动作参数m={'index':'获取基础账号密码等信息',‘get_monster_list’：“获取副本怪物列表信息”}
        """
        action_data = kwargs
        try:
            # 每个请求降级一下太快了
            time.sleep(random.uniform(0, 1))
            postresult = self.post_url(body, action_data)
            serverinfo = postresult.json(encoding="UTF-8")
            if serverinfo == 403:
                self.log.error('您已失去登录状态，请重新登录！')
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
                    try:
                        self.log.error(serverinfo['msg'])
                    except KeyError as e:
                        self.log.error(serverinfo['message'])
            except Exception as e:
                pass
            return serverinfo
        except Exception as e:
            self.log.error('请求异常')
    def guess_lantern_riddle(self):
        datilog.filter_.username = self.user
        datilog.filter_.addr = self.num
        try:
            #ques_status 0 还没有开始答题，1 正在答题中 2 已经答题完毕
            self.log.info('贤才征辟')
            result = self.action(c='guess_lantern_riddle', m='index')
            if result:
                if result['status']==1:
                    ques_status = int(result['ques_status'])
                    if ques_status == 0:
                        self.log.info('今日答题已结束，请明日在来！')
                        return False
                    elif  ques_status == 2:
                        self.log.info('正在答题中，继续答题！')
                    elif  ques_status == 1:
                        self.log.info('开始答题')
                    result = self.action(c='guess_lantern_riddle', m='action')
                    if result:
                        if result['status'] ==1:
                            ques_info = result['ques_info']
                            quertion = ques_info['quertion']
                            type_ = ques_info['type']
                            id_ = ques_info['id']
                            A = ques_info['A']
                            B = ques_info['B']
                            C = ques_info['C']
                            D = ques_info['D']
                            self.log.info("%s题 %s:%s A:%s,B:%s,C:%s,D:%s"%(id_,type_,quertion,A,B,C,D))
                            all_ques = int(result['all_ques'])
                            now_ques = int(result['now_ques'])
                            id_ = result['ques_info']['id']
                            if  quertion in data:
                                answer = random.choice(["a", "b", "c", "d"])
                                #判断下当前的题是不是在这个答案列表里，如果在这个里面就找到对应的答案，防止答题随机，找对应的
                                answer_info = data[quertion]#获取问题答案
                                #通过答案反找对应的选项
                                for k,v in quertion:
                                    if v == answer_info:
                                        answer = lower(k)
                                        break
                            else:
                                #没有正确答案，随机选择
                                answer = random.choice(["a", "b", "c", "d"])
                            for i in range(all_ques-now_ques):
                                formdata = {
                                    'quertion': id_,
                                    'answer': answer
                                }
                                r = self.action(c='guess_lantern_riddle', m='fix_answer', body=formdata)
                                if r:
                                    if r['status'] == -5:
                                        self.log.info(r['msg'])
                                        return False
                                    elif r['status'] != 1:
                                        time.sleep(0.5)
                                    elif r['status'] ==1:
                                        # 是否正确
                                        is_right = r['right']
                                        #答案的内容
                                        quertion_info = ques_info[answer.upper()]
                                        if is_right == 1:
                                            # 回答对了，找到对应答案的内容
                                            data[quertion] = quertion_info
                                            self.log.info("%s题 回答:正确 %s:%s  %s:%s A:%s,B:%s,C:%s,D:%s" % (
                                            id_, type_, quertion, answer, quertion_info, A, B, C, D))
                                            datilog.info("%s题 回答:正确  %s:%s  %s:%s " % (
                                            id_, type_, quertion, answer, quertion_info))
                                        else:
                                            self.log.info("%s题 回答:错误  %s:%s 选择 %s:%s A:%s,B:%s,C:%s,D:%s" % (
                                            id_, type_, quertion, answer, quertion_info, A, B, C, D))
                                        #继续下一道题
                                        quertion_info = r['next_ques']
                                        quertion = quertion_info['quertion']
                                        if quertion in data:
                                            answer = random.choice(["a", "b", "c", "d"])
                                            # 判断下当前的题是不是在这个答案列表里，如果在这个里面就找到对应的答案，防止答题随机，找对应的

                                            answer_info = data[quertion]  # 获取问题答案
                                            # 通过答案反找对应的选项
                                            for k, v in quertion_info:
                                                if v == answer_info:
                                                    answer = lower(k)
                                                    break
                                        else:
                                            #没有答案随机筛选
                                            answer = random.choice(["a", "b", "c", "d"])
                                        type_ = ques_info['type']
                                        id_ = ques_info['id']
                                        A = ques_info['A']
                                        B = ques_info['B']
                                        C = ques_info['C']
                                        D = ques_info['D']
                with open(json_file_path, 'w+') as file:
                    #在此读取文件看看有没有新的写入
                    new_data = json.load(file)
                    #新旧数据合并
                    new_data.update(data)
                    datilog.info(new_data)
                    json.dump(new_data, file,ensure_ascii=False)
            else:
                self.log.error('贤才征辟异常')
        except Exception as e:
            self.log.error(traceback.print_exc())
    def tower(self,times=10):
        try:
            get_price =  self.action(c='tower',m='get_price')
            price = int(get_price['price'])
            #初始是2，后续每次加2，
            cru_time = (price-2)/2
            if cru_time<times:
                self.log.info('将魂购买%s次' % cru_time)
                for i in range(times-cru_time):
                    self.log.info('当前将魂购买第%s次' %(i+1))
                    self.action(c='tower',m='buy')
            else:
                self.log.info('当前将魂已经购买%s次' % (cru_time))
        except Exception as e:
            self.log.error(e)
            self.log.error(traceback.print_exc())
    def activity(self):
        resutl = self.action(c='activity',m='index')
        return resutl
    def index(self):
        result = self.action(c='treasuremap', m='index')
        return  result
    def treasuremap(self):  # 海运藏宝图
        """ type 1 2 3 对应上中下
            quality 1,2,3,4,5,6 对应级别， 6位红色
            m = exit_team 解散
            create_team  创建
            join_team tid=  加入指定队伍
            sale 出售宝图
        """
        #查看当天拼图任务是否完成
        try:
            treasuremap_flag = self.activity()['info']['treasuremap']
            if treasuremap_flag ==2:
                self.log.info('拼图任务完成')
                return True
            index = self.index()
            # list 列表 返回数据为现有组队信息 ，列表对象为字典、
            # team_status 是否组队信息
            mapnum = int(index['num'])
            self.log.info('%s拥有藏宝图%s 个' % (self.user, mapnum))
            if mapnum > 0:
                # list 列表 返回数据为现有组队信息 ，列表对象为字典、
                # team_status 是否组队信息

                try:
                    maytype = index['map']['type']
                    mapid = index['map']['id']
                except:
                    # 没有藏宝图了
                    return
                if index['team_status'] == 1:
                    # 已经组队
                    self.log.info('已经组队')
                    return True
                for item in index['list']:
                    # 遍历组队列表
                    typelist = []
                    for id in item['list']:
                        typelist.append(id['type'])
                    if maytype not in typelist:
                        reust = self.action(c='treasuremap', m='join_team', tid=item['id'])
                        if reust['status'] == 1:
                            if reust['finish'] == 1:
                                self.log.info('拼图成功')
                                self.treasuremap()
                            self.log.info('加入队伍')
                            return True
                self.action(c='treasuremap', m='create_team')
                print '创建队伍'
            else:
                #征收
                try:
                    self.log.info('没有藏宝图，开始征收')
                    city_index = self.action(c='city',m='index')
                    times = int(city_index['times'])
                    if times ==0:
                        return  False
                    for i in range(times):
                        self.log.info('没有藏宝图，开始征收第%s次'%i)
                        status = self.action(c='city',m='impose',e=0)
                        if status['status']==-3:
                            time.sleep(0.3)
                            continue
                        if status['treasuremap']:
                            break
                except:
                    self.log.error(traceback.print_exc())
                self.treasuremap()
        except Exception:
            self.log.error(traceback.print_exc())
    def assist_copy(self,times=5):
        return self.action(c='assist_copy',m='index')
    def assist_copy_buy(self,times=3):
        #初始是20元宝，每次加20
        try:

            index = self.assist_copy()
            cru_price = int(index['data']['current_purchase_price'])
            cru_time = (cru_price-20)/20
            if cru_time<times:
                self.log.info('一骑当千购买%s次' % cru_time)
                for i in range(times-cru_time):
                    self.log.info('当前一骑当千购买第%s次' %(i+1))
                    status  = self.action(c='assist_copy', m='buy_time')
                    if status:
                        if status['status'] ==1:
                            self.log.info('一骑当购买成功')
                        else:
                            self.log.info('一骑当购买失败')
                    else:
                        continue
            else:
                self.log.info('当前一骑当千已经购买%s次' % (cru_time))
        except Exception as e:
            self.log.error(traceback.print_exc())
    def sanctum_buy(self,times=3):
        #初始是20元宝，每次加20
        try:
            formdata= {
                "l":1
            }
            index = self.action(c='sanctum',m='select_map',body=formdata)
            cru_price = int(index['price'])
            cru_time = (cru_price-20)/20

            if cru_time<times:
                formdata = {
                    "type": 1
                }
                self.log.info('四象圣域买%s次' % cru_time)
                for i in range(times-cru_time):
                    self.log.info('四象圣域购买第%s次' %(i+1))
                    status  = self.action(c='sanctum', m='buy_times',body=formdata)
                    if status:
                        if status['status'] ==1:
                            self.log.info('四象圣域购买成功')
                        else:
                            self.log.info('四象圣域购买失败')
                    else:
                        continue
            else:
                self.log.info('四象圣域已经购买%s次' % (cru_time))
        except Exception as e:
            self.log.error(traceback.print_exc())
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
    def user_case(self):
        try:
           formdata = {
               "mid":2,
               "case":1
           }
           self.action(c='matrix', m='use_case',body=formdata)
        except:
             pass
    def island(self,times=15,type=1):  # 金银洞活动
        """
        type: 1 金洞 ，2银洞
        :return:
        """
        # 获取当前攻击的次数和金银守护者5的状态，是否为攻击过，如果为1则为可以攻击，为0 则表示不可以
        #默认有两种，元宝和银币
        try:
            index = self.action(c='island', m='index')
            if type==1:
                self.log.info('当前选择为金洞')
                choice_type='gold_list'
            else:
                choice_type = 'silver_list'
                self.log.info('当前选择为银洞')
            choice_type_list = index[choice_type]
            id = choice_type_list[4]['id']
            formdata = {
                "id": id,
                "type": type
            }
            count = int(self.action(c='island', m='get_mission', body=formdata)['info']['act'])
            id_open = choice_type_list[4]['openstatus']
            self.log.info('当前金银洞扫荡次数%s'%count)
            #扫荡次数
            sweep_list = [5,10,50,100]
            if count <= times and count < 6:
                for item in choice_type_list:  # 每日共计5次
                    id_ = item['id']
                    if item['openstatus'] ==1 and item['killed']==0:
                        status = self.action(c='island', m='pk', id=id_)  # 共计金银洞
                        if status['status'] != 1:
                            self.p('islait', status)
                            return
            id_open = self.action(c='island', m='index')[choice_type][4]['openstatus']
            id_ = self.action(c='island', m='index')[choice_type][4]['id']
            if count <= times and id_open == 1:
                #扫荡指定次数
                sweep_times= times -5
                if  5< sweep_times< 10:
                    formdata= {
                        "id":id_,
                        "times":5
                    }
                    self.action(c='island',m='sweep',body=formdata)
                    for i in range(sweep_times-5):
                        status = self.action(c='island', m='pk', id=id_)
                elif sweep_times >10:
                    for i in range(sweep_times/10):
                        formdata = {
                            "id": id_,
                            "times": 10
                        }
                        self.action(c='island', m='sweep', body=formdata)
                else:
                    for i in range(times):
                        status = self.action(c='island', m='pk', id=id_)
            else:
                self.log.info('今天金银洞已经扫荡了%s次不在攻打'%count)
        except Exception as e:
            print e
    def copies(self,stage_type=3,):
        """
        :param stage_type: 1 只扫普通关卡，3 BOSS关卡，3全部关卡
        :return:
        """
        difficulty_type_d ={
            "1":'普通',
            "2":'困难',
            "3":'英雄'
        }
        try:
            self.action(c='copies',m='index',d='newequip')
            sweep_entry = self.action(c='copies',m='sweep_entry',d='newequip')
            for i in range(1,4):
                self.log.info('扫荡%s副本'%(difficulty_type_d[str(i)]))
                formdata = {
                    "difficulty_type":i,
                    "stage_type":stage_type,
                    "confirm":1
                }
                self.action(c='copies', m='sweep_all', d='newequip',body=formdata)
        except Exception as e:
            print e
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

    def apparatus_fight(self):
        #器械争夺
        return self.action(c='apparatus_fight',m='index')
    def apparatus_fight_action(self):
        #攻击
        return self.action(c='apparatus_fight', m='action')
    def apparatus_fight_entry_build(self,build_id):
        formdata= {
            'build_id':build_id,
        }
        return self.action(c='apparatus_fight', m='entry_build',body=formdata)
    def apparatus_fight_cur_status(self):
        #查看当前状态
        try:
            index = self.apparatus_fight()
            build_info = index['build_info']
            budld_dict = dict()
            for item in build_info:  # 开始遍历
                budld_dict['build_id'] = item['is_pass']
                entry_build = self.apparatus_fight_entry_build(item['build_id'])
                if entry_build['status']==-4:
                    self.log.info(entry_build['msg'])
                    return  False
                else:
                    return True
        except Exception:
            self.log.error(index['msg'])
            return False
    def apparatus_fight_auto_pk(self):
        try:
            if not self.apparatus_fight_cur_status():
                return
            index = self.apparatus_fight()
            build_info = index['build_info']
            for item in build_info:#开始遍历
                if int(item['is_pass']) == 0:#表示未打过，1为已经打过了
                    build_id = item['build_id']
                    build_name = item['build_name']
                    reward_level = item['reward_level']
                    self.log.info('开始攻打%s,奖励等级:Lv.%s' % (build_name, reward_level))
                    entry_build  = self.apparatus_fight_entry_build(build_id)
                    if entry_build['status'] != 1:#前置关卡未通过
                        self.log.info(entry_build['msg'])
                        time.sleep(2)
                    else:#如果返回正常，进行攻击,
                        for i in range(10):
                            entry_build = self.apparatus_fight_entry_build(build_id)
                            nickname = entry_build['opponent_info']['nickname']
                            level = entry_build['opponent_info']['level']
                            #攻击10次，如果10次也打不过就别打了，太弱了
                            self.log.info('开始攻打%sLv.%s'%(nickname,level))
                            result = self.apparatus_fight_action()
                            if result['status']==1 and result['win'] ==1:
                                #
                                self.log.info('攻打成功')
                                time.sleep(0.5)
                                break
                            elif result['status']==1 and result['win'] !=1:
                                self.log.info('攻打失败')
                                #需要刷新攻打对手
                                continue
                            elif result['status']==-3:
                                self.log.info('攻打失败%s'%result['msg'])
                                time.sleep(1)
                                continue
                            elif result['status']!=1:
                                self.log.info('攻打失败%s'%result['msg'])
                                break
                else:
                    build_name= item['build_name']
                    reward_level= item['reward_level']
                    self.log.info('%s已通关,奖励等级:Lv.%s'%(build_name,reward_level))
        except:
            self.log.error(traceback.format_exc())
def run(user, apass, addr,lockpwd):
    log = MyLog(logname='daily.log', level=logging.INFO)
    log.filter_.username=user
    log.filter_.addr= addr
    rewary.pwd = lockpwd
    action = rewary(user, apass, addr,log)
    action.unlock(lockpwd)
    level = action.level()
    action.user_case()#使用固定阵法
    if level > 150:
        action.guess_lantern_riddle()#贤才征辟
    action.tower(times=10)#将魂
    action.assist_copy_buy(times=3)#一骑当千
    action.general_break_through()#点将台
    action.island(times=15,type=1) #金银洞
    action.copies()#平乱
    action.dice()#国家色子
    action.treasuremap()#藏宝图
    action.apparatus_fight_auto_pk()#器械争夺
    action.sanctum_buy()#四象圣域


def get_run(user, apass, addr,func):
    log = MyLog(logname='meirirenwu.log', level=logging.INFO)
    log.filter_.username = user
    log.filter_.addr = addr
    action = rewary(user, apass, addr, log)
    getattr(action,func)()


if __name__ == '__main__':
    q = Queue()
    filepath = os.path.dirname(os.path.abspath(__file__))
    # cont =  ['user.txt','21user.txt','autouser.txt','alluser.txt']
    # cont = ['149cnm.txt', '149dgj.txt', '149gx1.txt', '148gx.txt','149xx.txt',
    #         '149xb.txt', '149lwzs.txt']
    cont = ['xing.py','autouser.txt']
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
