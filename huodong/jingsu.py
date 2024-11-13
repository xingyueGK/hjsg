#-*- coding:utf-8 -*-
import threading
import time

from activ import  *
from shujufenx import fuben


"""竞速步骤
1、第一次扫荡攻击后16级失败
2、强化2级装备到16级，然后并穿戴，扫荡到16级后失败
3、再次强化装备到26级后攻击超过30级失败
4、领取蔡文姬武将，并出站，然后突飞够24级
5、等级达到32级
地图等级分布
111 第八个图

"""

headers = {
    'Accept-Encoding':'gzip, deflate',
    'Accept-Language':'zh-CN,zh;q=0.8',
    'Connection':'keep-alive',
    # 'Host':'s148.game.hanjiangsanguo.com',
    'Upgrade-Insecure-Requests':'1',
    'Content-Type':'application/json',
    'DNT':'1',
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'
}
def act(username,passwd,addr):
    action = fuben(username,passwd,addr)
    try:
        print '账号：%s   等级为：%s' % (username, action.level())
        memberindex = action.action(c='member', m='index')
        missionlevel = int(memberindex['missionlevel'])
        missionsite = int(memberindex['missionsite'])
        missionstage = int(memberindex['missionstage'])
    except Exception as e :
        print e
        print 'zhanghao ###################################### ',username
    if action.level() >= 157:
        exit()
    if  action.level() <10:
        print '10ji'
        action.saodang(missionlevel,missionsite,missionstage)#16级 失败退出
        action.levelgift()  # 领取16级奖励
    #扫荡失败以后获取2级别装备，然后强化后并穿戴上去
    if action.level() < 25:
        print '25ji'
        gid,uid = action.general(7)#第一次的都是2级装备
        print gid,uid
        for i in uid:
            for etype,v in i.items():
                action.strengthen(v)
                action.equip(gid,v,etype)
        action.saodang(missionlevel,missionsite,missionstage)#26级失败退出
        for i in uid:
            for etype, v in i.items():
                action.strengthen(v)
    if action.level() < 35:
        print '35ji'

        action.mapscene(missionlevel)#领取通关奖励
        action.levelgift()  # 领取30级奖励
        action.muster()  # 武将出征并上阵，并突飞到30级
        #action.morra()#节节高
        gid, uid = action.general(25)#获取三级装备，再次强化，并给武将穿戴上
        for i in uid:
            for etype, v in i.items():
                action.strengthen(v)
                action.equip(gid, v, etype)
            action.saodang(missionlevel,missionsite,missionstage)  # 级失败退出
        for i in uid:
            for etype, v in i.items():
                action.strengthen(v)
                action.equip(gid, v, etype)
        action.saodang(missionlevel,missionsite,missionstage)#30级失败退出从第二个图开始
    if action.level()<50:
        for i  in range(2):
            action.mainquest()#获取所有活动
        gid, uid = action.general(25)#获取25级需要穿戴的装备强化
        for i in uid:
            for etype, v in i.items():
                action.strengthen(v)
                action.equip(gid, v, etype)
        action.muster()  # 再次突飞
        action.saodang(missionlevel,missionsite,missionstage)
    if action.level()  <70:#领取前60次奖励

        # action.muster()#对武将突飞
        # #action.morra()  # 节节高
        # for i in range(3):#循环领取通过奖励
        #     action.mainquest()
        for i in range(4,13):
            action.levelgift()  # 领取60级奖励
        #获取竞速元宝
        for i in range(10, 120, 10):
            action.action(c='map',m='get_mission_reward',id=i)

        #         action.strengthen(eid1_quality_equipments)#强化装备
        # action.strengthen(general_index_list['eid1']['id'])
        action.saodang(3)
    if action.level()  <120:#领取前60次奖励
        #action.muster(level=80)
        # gid, uid = action.general(25)  # 获取三级装备，再次强化，并给武将穿戴上
        # for i in uid:
        #     action.strengthen(i)
        for i in range(3):#循环领取通过奖励
            action.mainquest()
        for i in range(4,13):
            action.levelgift()  # 领取60级奖励
        action.saodang(6)
        #获取竞速元宝
        for i in range(10, 120, 10):
            action.action(c='map',m='get_mission_reward',id=i)
    if action.level() < 130:  # 领取前60次奖励
       # action.muster(level=140)
        action.saodang(20)
    if action.level() < 140:  # 领取前60次奖励
       # action.muster(level=140)
        action.saodang(20)

    if action.level() < 170:  # 领取前60次奖励
        #action.mainquest()
        #action.tujian()
        #action.soul()
        #action.mapscene()  # 领取通关奖励
        #action.muster(level=90)
        #获取竞速元宝
        # for i in range(10, 180, 10):
        #     a= action.action(c='map',m='get_mission_reward',id=i)
        action.saodang(20)
def joi(username,passwd,addr):
    #国家海外贸易
    action = fuben(username,passwd,addr)
    action.join()#加入国家
    # print '账号：%s   等级为：%s' % (username, action.level())
    # action.overseastrade()
def fk(username,passwd,addr):
    #福卡活动
    action = activity(username,passwd,addr)
    # action.qiandao()
    # action.leigu()
    # action.generalpool()  #
    # action.cuju()
    # action.shenshu()
    action.fuka(45)
def wujiang(username,passwd,addr):#武将训练信息
    action = fuben(username,passwd,addr)
    action.mapscene()  # 领取通关奖励
    action.action(c='muster',m='index')
    practiceinfo=action.action(c='practice',m='index')
    freetimes = practiceinfo['freetimes']#突飞卡
    turn = practiceinfo['list']['1']['turn']
    level = practiceinfo['list']['1']['level']
    print '剩余突飞卡 %s 武将等级 %s 转 %s 级'%(freetimes,turn,level)
def xk(username,passwd,addr):
    activ = activity(username, passwd,addr)
   # activ.caikuang()
    #activ.actjubao()
   # activ.leigu()
  #  activ.generalpool()  #
    #activ.cuju()
#    activ.shenshu()
    #activ.fuka()
    #activ.qiandao()
    #activ.gongxiang()
    activ.usebuff()
def buy(username,passwd,addr):
    action = activity(username, passwd,addr)
    # action.countrysacrifice()
    # action.usebuff()
    action.action(c = 'tavern', m = 'get_list' ,page = 1 , perpage = 100 , tab = 4)
    # action.action(c='tavern',m='buy',generalid=79)#购买孙权武将武将
    action.action(c='tavern',m='buy',generalid=151)#购买张昭

def uneq(username,passwd):#武将训练信息
    action = fuben(username,passwd)
    general_index = action.get_general()  # 获取装备列表信息
    general_index_list = general_index['list']['2']  # 穿戴装备列表
    print general_index
    eid2 = general_index_list['eid2']
    eid3 = general_index_list['eid3']
    gid=general_index_list['id']
    action.action(c='general', m='unequip', gid=gid, eid=eid2, position=0)
    action.action(c='general', m='unequip', gid=gid, eid=eid3, position=0)
def genarl(username,passwd):#装备穿戴3级别以上装备
    action = fuben(username,passwd)
    general_index = action.get_general()  # 获取装备列表信息
    general_index_list = general_index['list']['1']  # 穿戴装备列表
    general_index_equipments = general_index['equipments']  # 未穿戴装备列表
    gid = general_index_list['id']  # 获取武将id
    # eid1_quality = general_index_list['eid1']['quality']#佩戴武器的等级
    for k, equ in general_index_equipments.items():  # 遍历未穿戴装备列表
        if equ['quality'] == '3' or equ['quality'] == '4' or equ['quality'] == '5':
            eid1_quality_equipments = equ['id']  # 未穿戴的6级或是5级装备
            action.eqip(gid, eid1_quality_equipments)
def map(username, passwd,addr):
    action = fuben(username, passwd,addr)
    action.morra()
def wjleveup(username, passwd,addr):
    action = fuben(username, passwd,addr)
    action.tufei(u'张昭',80)
def peiyang(username,passwd,addr):
    action = activity(username, passwd,addr)
    action.peiyang('张昭')

def carnival(username,passwd,addr):
    action = activity(username, passwd,addr)
    action.discount_carnival()
def run(username,passwd,addr):
    action = activity(username, passwd,addr)

    memberindex = action.action(c='member', m='index')
    action.p(memberindex)
    missionlevel = int(memberindex['missionlevel'])
    missionsite = int(memberindex['missionsite'])
    missionstage = int(memberindex['missionstage'])
    map = action.action(c='map', m='get_mission_list')
    exit_code = 1
    print 'saosang', missionlevel
    if exit_code == 1:
        for level in range(missionlevel, 13):  # 遍历每一个图
            print 'action  %s mission' % level
with open('../users/xing.py', 'r') as f:
    for i in f:
        if i.strip() and not i.startswith('#'):
            name = i.split()[0]
            passwd = i.split()[1]
            addr = i.split()[2]
            t1 = threading.Thread(target=act,args=(name,passwd,addr))
            t1.start()