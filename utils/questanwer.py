#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/10/12 14:52
# @Author  : xingyue
# @File    : questanwer.py


questdict = {
    "该题为福利题，请选A"
    "该题为福利题，请选B"
    "该题为福利题，请选C"
    "该题为福利题，请选D"
    "武将商城开启的时间为？"
    "稀有属性“锋芒”的作用是？"
    "稀有属性“坚韧”的作用是？"
    "稀有属性“最终伤害”的作用是？"
    "稀有属性“最终减伤”的作用是？"
    "稀有属性“暴击伤害”的作用是？"
    "强化百分百活动中，战鼓的强化是否也是百分百成功呢？"
    "超值月卡活动中，当前已拥有月卡时再次充值是否会替换当前的月卡呢？"
    "器械中的“眩晕”是否会考虑抗晕以及套装的免晕属性？"
    "备战坐骑的基础属性计算多少？"
    "备战坐骑的稀有属性计算多少？"
    "副坐骑的稀有属性计算多少？"
    "每日可卖出10级及以上装备的上限是多少？"
    "以下哪项不是元宵节的传统活动"
    "中国古代的“上元节”指的是哪个节日"
    "古代有赏花灯的习俗，被成为“灯节”的是哪一天"
    "被称为“天下第一关”的是"
    "配合周瑜使用“苦肉计”大破曹军的是哪位将领？"
    "司马懿辅佐的第一位魏国太子是谁？"
    "在“捉放曹”情节中是谁放了曹操并随曹操一并离去"
    "公孙瓒手下有支名震天下的骑兵，这支骑兵的名称"
    "十八路诸侯讨伐董卓时，谁为盟主"
    "下列人物中是讨伐黄巾军的主要统帅的是"
    "黄巾之乱时由谁发起"
    "穿绿衣裳，肩扛两把刀。庄稼地里走，害虫吓得跑(打一动物名)"
    "娘子娘子，身似盒子。麒麟剪刀，八个钗子(打一动物名)"
    "百万孩子去造林(干果)"
    "白糖梅子真稀奇(打一食物)"
    "一黑一白斗智斗勇（打一物品）"
    "昔日鸟儿归来乐开怀（打一动物）"
    "头顶小红帽，清早把嗓练（打一动物）"
    "人在云端漫步。（打一字）"
    "木棍上边串个太阳（打一字）"
    "独坐八卦阵，谁来把网投（打一动物）"
    "王允通过谁使董卓与吕布反目成仇？"
    "凤雏庞统殒命何处？"

}
answer = {
    "48": "c", "10": "c", "42": "a", "27": "b", "39": "b", "5": "d", "14": "c",
    "50": "d", "47": "c", "33": "b", "23": "d", "45": "b", "15": "b", "4": "d",
    "18": "c", "35": "d", "12": "b", "29": "c", "41": "a", "20": "b",
    "32": "a", "6": "d", "3": "d", "22": "a", "17": "a", "37": "a",
    "43": "a", "49": "d", "7": "a", "2": "a", "30": "a", "9": "a",
    "46": "b", "21": "c", "31": "b", "16": "d", "25": "b", "13": "d",
    "28": "a", "40": "c", "26": "a", "36": "b", "44": "b", "1": "a",
    "38": "b", "11": "b", "34": "c", "19": "d", "8": "d"
}

print sorted(answer.items(), lambda x,y: cmp(x[1], y[1]))