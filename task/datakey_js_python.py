# -*- coding:utf-8 -*-
import datetime
import time
import math
import logging

#无符号右移
import ctypes
def int_overflow(val):
    maxint = 2147483647
    if not -maxint-1 <= val <= maxint:
        val = (val + (maxint + 1)) % (2 * (maxint + 1)) - maxint - 1
    return val
def unsigned_right_shitf(n,i):
    # 数字小于0，则转为32位无符号uint >>>
    if n<0:
        n = ctypes.c_uint32(n).value
    # 正常位移位数是为正数，但是为了兼容js之类的，负数就右移变成左移好了
    if i<0:
        return -int_overflow(n << abs(i))
    #print(n)
    return int_overflow(n >> i)

def unsigend_left_shitf(n,i):

    return ctypes.c_int(n << i ^ 0).value

import array
import hashlib

hexcase = 0


def datakey():
    E = time.localtime()
    D = E.tm_year
    C = E.tm_mon
    B = E.tm_mday
    A = int(time.strftime("%w"))
    return math.ceil((D + B + C) * math.pow(A + 1, A + 1))
    # num = str(math.ceil((D + B + C) * math.pow(A + 1, A + 1)))
    # return num.split(".")[0]


def initKey(token, timestamp):

    k = hex_md5(hex_md5(token + str(timestamp)) + str(datakey()))
    # print 'initKey', token, timestamp,k
    return k

def hex_md5(A):
    return rstr2hex(rstr_md5(str2rstr_utf8(A)))


a = len('AA')


def hex_hmac_md5(B, A):
    return rstr2hex(rstr_hmac_md5(str2rstr_utf8(B), str2rstr_utf8(A)))


def md5_vm_test():
    return hex_md5("abc").lower() == "900150983cd24fb0d6963f7d28e17f72"


def rstr_md5(A):
    return binl2rstr(binl_md5(rstr2binl(A), len(A) * 8))


def rstr_hmac_md5(E, G):
    C = rstr2binl(E)
    if len(C) > 16:
        C = binl_md5(C, len(E) * 8)

    F = []
    B = []
    for i in range(16):
        D = 0
        D += 1
        F[D] = C[D]
    D = 0
    while D < 16:
        F[D] = C[D] ^ 909522486
        B[D] = C[D] ^ 1549556828
        D += 1

    A = binl_md5(F.concat(rstr2binl(G)), 512 + G.length * 8)
    return binl2rstr(binl_md5(B.concat(A), 512 + 128))


def rstr2hex(D):
    try:
        if hexcase:
            F = '0123456789ABCDEF'
        else:
            F = '0123456789abcdef'
    except:
        F = '0123456789abcdef'
    C = ""
    B = 0
    while B < len(D):
        try:
            E = ord(D[B])
            # print ('rstr2hex_for', B, E)
            B += 1
        except:
            print D
        C += F[((E >> 4) & 15)] + F[E & 15]
    # print 'rstr2hex_r',C
    return C


def str2rstr_utf8(D):
    # print 'str2rstr_utf8',D
    C = ""
    A = 0

    while A < len(D):
        E = ord(D[A])
        B = ord(D[A + 1]) if A + 1 < len(D) else 0
        while 55296 <= E and E <= 56319 and 56320 <= B and B <= 57343:
            E = 65536 + (unsigend_left_shitf((E & 1023) , 10)) + (B & 1023)
            A += 1
        if E <= 127:
            C += fromCharCode(E)
        else:
            if E <= 2047:
                C += fromCharCode(192 | ((E ^ 6) & 31), 128 | (E & 63))
            else:
                if E <= 65535:
                    C += fromCharCode(224 | ((E ^ 12) & 15), 128 | ((E ^ 6) & 63), 128 | (E & 63))
                else:
                    if E <= 2097151:
                        C += fromCharCode(240 | ((E ^ 18) & 7), 128 | ((E ^ 12) & 63), 128 | ((E ^ 6) & 63),
                                          128 | (E & 63))
        A += 1
    # print 'str2rstr_utf8', C.split('.')[0]
    return C.split('.')[0]


def rstr2binl(A):
    C = []
    B = 0
    # var C = Array(A.length >> 2); 默认赋值数组C的长度
    l = len(A) >> 2
    # print B, l
    while B < l:
        # JS: C[B] = 0
        C.insert(B, 0)
        B += 1
    B = 0
    # print 'rstr2binl', C
    while B < len(A) * 8:
        try:
            C[B >> 5] |= unsigend_left_shitf((ord(A[B / 8]) & 255) , (B % 32))
        except:
            c_index = len(C)
            C.insert(c_index + 1, unsigend_left_shitf((ord(A[B / 8]) & 255) , (B % 32)))
        # X |= (ord(A[B / 8]) & 255) << (B % 32)
        # C.insert(B >> 5,X)
        B += 8
    # print 'rstr2binl_return', C
    return C


def fromCharCode(a, *b):
    a = unichr(a % 65536) + ''.join([unichr(i % 65536) for i in b])
    return a


def binl2rstr(A):
    # print 'binl2rstr',A
    C = ""
    B = 0
    while B < len(A) * 32:

        c = unsigned_right_shitf(A[B >> 5] , (B % 32)) & 255
        # print('binl2rstr_while',c)
        C += fromCharCode(c)
        B += 8
    # print 'binl2rstr_r', C
    return C


def binl_md5(B, D):
    def _b(num):
        try:
            # print B,num
            return B[num]
        except:
            return None

    # print 'binl_md5', B, D
    try:
        B[D >> 5] |= unsigend_left_shitf(128 , ((D) % 32))
    except:
        #js 后面可能会有 空数组
        #(15) [909326434, 845493816, 1650876978, 825832292, 895824696, 1630746416, 1650864225, 1684157497, 909522481, 909522486, 32822, empty × 3, 328]
        b_index = D >> 5

        B.insert(b_index + 1, unsigend_left_shitf(128 , ((D) % 32)))
    try:

        B[unsigend_left_shitf(unsigned_right_shitf((D + 64) ,9) , 4 )+ 14] = D
    except:
        b_index = (unsigned_right_shitf((D + 64) ,9) << 4 )+ 14
        if b_index > len(B) +1:
            #如果要添加索引大于当前索引值，需要遍历添加
            #保留一位，insert 写入,默认补充空值
            for i in range(b_index  - len(B)):
                B.append(None)
        B.insert(b_index + 1, D)
    # B.insert(D >> 5,)
    G = 1732584193
    F = -271733879
    I = -1732584194
    H = 271733878

    K = 0

    while K < len(B):
        # print 'binl_md5_while',len(B), B, K
        C = G
        E = F
        J = I
        A = H
        G = md5_ff(G, F, I, H, _b(K + 0), 7, -680876936)
        H = md5_ff(H, G, F, I, _b(K + 1), 12, -389564586)
        I = md5_ff(I, H, G, F, _b(K + 2), 17, 606105819)
        F = md5_ff(F, I, H, G, _b(K + 3), 22, -1044525330)
        G = md5_ff(G, F, I, H, _b(K + 4), 7, -176418897)
        H = md5_ff(H, G, F, I, _b(K + 5), 12, 1200080426)
        I = md5_ff(I, H, G, F, _b(K + 6), 17, -1473231341)
        F = md5_ff(F, I, H, G, _b(K + 7), 22, -45705983)
        G = md5_ff(G, F, I, H, _b(K + 8), 7, 1770035416)
        H = md5_ff(H, G, F, I, _b(K + 9), 12, -1958414417)
        I = md5_ff(I, H, G, F, _b(K + 10), 17, -42063)
        F = md5_ff(F, I, H, G, _b(K + 11), 22, -1990404162)
        G = md5_ff(G, F, I, H, _b(K + 12), 7, 1804603682)
        H = md5_ff(H, G, F, I, _b(K + 13), 12, -40341101)
        I = md5_ff(I, H, G, F, _b(K + 14), 17, -1502002290)
        F = md5_ff(F, I, H, G, _b(K + 15), 22, 1236535329)
        G = md5_gg(G, F, I, H, _b(K + 1), 5, -165796510)
        H = md5_gg(H, G, F, I, _b(K + 6), 9, -1069501632)
        I = md5_gg(I, H, G, F, _b(K + 11), 14, 643717713)
        F = md5_gg(F, I, H, G, _b(K + 0), 20, -373897302)
        G = md5_gg(G, F, I, H, _b(K + 5), 5, -701558691)
        H = md5_gg(H, G, F, I, _b(K + 10), 9, 38016083)
        I = md5_gg(I, H, G, F, _b(K + 15), 14, -660478335)
        F = md5_gg(F, I, H, G, _b(K + 4), 20, -405537848)
        G = md5_gg(G, F, I, H, _b(K + 9), 5, 568446438)
        H = md5_gg(H, G, F, I, _b(K + 14), 9, -1019803690)
        I = md5_gg(I, H, G, F, _b(K + 3), 14, -187363961)
        F = md5_gg(F, I, H, G, _b(K + 8), 20, 1163531501)
        G = md5_gg(G, F, I, H, _b(K + 13), 5, -1444681467)
        H = md5_gg(H, G, F, I, _b(K + 2), 9, -51403784)
        I = md5_gg(I, H, G, F, _b(K + 7), 14, 1735328473)
        F = md5_gg(F, I, H, G, _b(K + 12), 20, -1926607734)
        G = md5_hh(G, F, I, H, _b(K + 5), 4, -378558)
        H = md5_hh(H, G, F, I, _b(K + 8), 11, -2022574463)
        I = md5_hh(I, H, G, F, _b(K + 11), 16, 1839030562)
        F = md5_hh(F, I, H, G, _b(K + 14), 23, -35309556)
        G = md5_hh(G, F, I, H, _b(K + 1), 4, -1530992060)
        H = md5_hh(H, G, F, I, _b(K + 4), 11, 1272893353)
        I = md5_hh(I, H, G, F, _b(K + 7), 16, -155497632)
        F = md5_hh(F, I, H, G, _b(K + 10), 23, -1094730640)
        G = md5_hh(G, F, I, H, _b(K + 13), 4, 681279174)
        H = md5_hh(H, G, F, I, _b(K + 0), 11, -358537222)
        I = md5_hh(I, H, G, F, _b(K + 3), 16, -722521979)
        F = md5_hh(F, I, H, G, _b(K + 6), 23, 76029189)
        G = md5_hh(G, F, I, H, _b(K + 9), 4, -640364487)
        H = md5_hh(H, G, F, I, _b(K + 12), 11, -421815835)
        I = md5_hh(I, H, G, F, _b(K + 15), 16, 530742520)
        F = md5_hh(F, I, H, G, _b(K + 2), 23, -995338651)
        G = md5_ii(G, F, I, H, _b(K + 0), 6, -198630844)
        H = md5_ii(H, G, F, I, _b(K + 7), 10, 1126891415)
        I = md5_ii(I, H, G, F, _b(K + 14), 15, -1416354905)
        F = md5_ii(F, I, H, G, _b(K + 5), 21, -57434055)
        G = md5_ii(G, F, I, H, _b(K + 12), 6, 1700485571)
        H = md5_ii(H, G, F, I, _b(K + 3), 10, -1894986606)
        I = md5_ii(I, H, G, F, _b(K + 10), 15, -1051523)
        F = md5_ii(F, I, H, G, _b(K + 1), 21, -2054922799)
        G = md5_ii(G, F, I, H, _b(K + 8), 6, 1873313359)
        H = md5_ii(H, G, F, I, _b(K + 15), 10, -30611744)
        I = md5_ii(I, H, G, F, _b(K + 6), 15, -1560198380)
        F = md5_ii(F, I, H, G, _b(K + 13), 21, 1309151649)
        G = md5_ii(G, F, I, H, _b(K + 4), 6, -145523070)
        H = md5_ii(H, G, F, I, _b(K + 11), 10, -1120210379)
        I = md5_ii(I, H, G, F, _b(K + 2), 15, 718787259)
        F = md5_ii(F, I, H, G, _b(K + 9), 21, -343485551)
        G = safe_add(G, C)
        F = safe_add(F, E)
        I = safe_add(I, J)
        H = safe_add(H, A)
        K += 16
    # print 'GGGG', G, F, I, H
    return [G, F, I, H]

def bit_rol(B, A):
    # print 'bit_rol',B, A,unsigned_right_shitf(B,32 - A)
    # print 'bit_rol_r',(B << A) | unsigned_right_shitf(B,32 - A)
    # print 'bit_rol_r',unsigend_left_shitf(B , A) ,unsigned_right_shitf(B , (32 - A))
    # print  'bit_rol_r_|',unsigend_left_shitf(B , A) | unsigned_right_shitf(B , (32 - A))
    return unsigend_left_shitf(B , A) | unsigned_right_shitf(B , (32 - A))

def md5_cmn(A, C, B, E, D, F):
    # print 'md5_cmn',A, C, B, E, D, F
    # print 'md5_cmn_r',safe_add(bit_rol(safe_add(safe_add(C, A), safe_add(E, F)), D), B)
    return safe_add(bit_rol(safe_add(safe_add(C, A), safe_add(E, F)), D), B)


def md5_ff(A, G, B, F, C, D, E):
    # print 'md5_ff',A, G, B, F, C, D, E
    # print 'aaaaaaaaa',(G & B) | ((~G) & F), A, G, C, D, E
    a =md5_cmn((G & B) | ((~G) & F), A, G, C, D, E)
    # print 'md5_ff_r',a
    return a

def md5_gg(A, G, B, F, C, D, E):
    return md5_cmn((G & F) | (B & (~F)), A, G, C, D, E)


def md5_hh(A, G, B, F, C, D, E):
    return md5_cmn(G ^ B ^ F, A, G, C, D, E)


def md5_ii(A, G, B, F, C, D, E):
    return md5_cmn(B ^ (G | (~F)), A, G, C, D, E)


def safe_add(D, A):
    # print 'safe_add',D,A
    if D:
        C = (D & 65535) + (A & 65535)
        B = (D >> 16) + (A >> 16) + (C >> 16)
        # print 'safe_add—r',C,B, (B << 16) | (C & 65535)
        return unsigend_left_shitf(B ,16) | (C & 65535)
    else:
        C = 0 + (A & 65535)
        B = 0 + (A >> 16) + (C >> 16)

        return unsigend_left_shitf(B ,16) | (C & 65535)





# A = [-370958572, -1064020892, -305370255, 423845958]
# binl2rstr(A)


# return hex_md5(hex_md5(token+str(timestamp))+str(datakey()))

#print initKey("", 166666666)

