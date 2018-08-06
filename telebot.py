#!/usr/bin/python
# -*- coding: utf8 -*-
# vim: set rnu sw=4 ss=4 ts=4 et smartindent fdm=indent :
import sys
import time
import telepot
import json
import requests
import datetime
import re
import time
from pprint import pprint
from myconfig import MYTOKEN

reload(sys)
sys.setdefaultencoding('utf8')

class Menu:
    def __init__(self, name, desc):
        self.name = name
        self.desc = desc
        self.child=[]
        self.cmd=[]
    def addchild(self, child):
        self.child.append(child)
    def parent(self, parent):
        self.parent = parent
    def setcmd(self, cmd):
        self.cmd.append(cmd)
    def common(self):
        return '............  🏠 /start    ⬅️  /back';
    def setup(self):
        pass
    def msg(self, m):
        child = ''
        if self.child:
            for c in self.child:
                if c.name == m:
                    c.setup()
                    return c

        return -1
    def menu(self): 
        menu = ''
        if self.child:
            for m in self.child:
                menu += '\n' + m.name + ' : ' +  m.desc
        return menu
    def getchild(self):
        if self.child:
            return self.child
        else:
            return -1
        return self.child
    def getparent(self):
        if self.parent:
            return self.parent
        else:
            return -1
class DeviceAircon(Menu):
    def __init__(self, name, desc, ip):
        self.name   = name
        self.desc   = desc 
        self.ip     = ip
        self.cmd    = [['/on','에어컨 켜기'], ['/off', '에어컨 끄기'], ['/status','에어컨 상태보기']]
        self.di     = ''
        self.timer  = ''
        self.phase  = ''
    def setup(self):
        self.phase = ''
    def rcmd(self, key):
        fcmd = 'http://'
        fcmd += self.ip
        fcmd += '/'
        if key != '':
            requests.get(fcmd+key)  # url is cmd Rest API
            time.sleep(1)
        r = requests.get(fcmd)  # get status
        j = r.json()[u'variables']

        msg = ''
        msg += '\n에어컨 상태: %s' % (j['Status Cool'])
        msg += '\n방 온도: %s' % (j['Temp'])
        msg += '\n방 습도: %s' % (j['Humi'])
        msg += '\n방 불쾌지수: %s' % (j['DI'])
        msg += '\n타이머 남은 시간(분): %s' % (j['timer_ctrl'])
        msg += '\n설정된 불쾌지수: %s' % (j['di_ctrl'])

        '''
        {"Status Heat":"RELAY_OFF","Temp":34.0,"DI":79.34,
        "timer_ctrl":87,"Humi":24.0,"di_ctrl":79,"Status Cool":"RELAY_ON","heat_ctrl":-999}
        
        '''
        return msg
    def menu(self):
        msg =''
        for c in self.cmd:
            msg += '\n' + c[0] 
            msg += ': ' + c[1]
        return msg
    def menu_di(self):
        status = 'waiting di'
        msg  = '\n불쾌지수를 선택하세요'
        msg += '\n/068 불쾌감을 느끼는 사람 없음'
        msg += '\n/069'
        msg += '\n/070'
        msg += '\n/071'
        msg += '\n/072'
        msg += '\n/073'
        msg += '\n/074'
        msg += '\n/075 약 50% 인간이 불쾌감을 느끼기 시작함'
        msg += '\n/076'
        msg += '\n/077'
        msg += '\n/078'
        msg += '\n/079'
        msg += '\n/080 모든 인간이 불쾌감을 느끼기 시작함'
        msg += '\n/081'
        msg += '\n/082'
        msg += '\n/083'
        msg += '\n/084'
        msg += '\n/085'
        msg += '\n/086'
        msg += '\n/087'
        msg += '\n/088'
        msg += '\n/089'
        return msg
    def menu_timer(self):
        m = 0
        d = datetime.datetime.now()
        msg  = '\n타이머를 선택하세요'
        m += 30
        d += datetime.timedelta(minutes=30)
        msg += '\n/%03d 삽십분 ~ ~ %s' % (m, d.strftime('%m-%d %H:%M'))
        m += 30
        d += datetime.timedelta(minutes=30)
        msg += '\n/%03d 한시간 ~ ~ %s' % (m, d.strftime('%m-%d %H:%M'))
        m += 30
        d += datetime.timedelta(minutes=30)
        msg += '\n/%03d 한시간 삼십분 ~ %s' % (m, d.strftime('%m-%d %H:%M'))
        m += 30
        d += datetime.timedelta(minutes=30)
        msg += '\n/%03d 두시간 ~ %s' % (m, d.strftime('%m-%d %H:%M'))
        m += 30
        d += datetime.timedelta(minutes=30)
        msg += '\n/%03d 두시간 삼십분 ~ %s' % (m, d.strftime('%m-%d %H:%M'))
        m += 30
        d += datetime.timedelta(minutes=30)
        msg += '\n/%03d 세시간 ~ %s' % (m, d.strftime('%m-%d %H:%M'))
        m += 30
        d += datetime.timedelta(minutes=30)
        msg += '\n/%03d 세시간 삼십분 ~ %s' % (m, d.strftime('%m-%d %H:%M'))
        m += 30
        d += datetime.timedelta(minutes=30)
        msg += '\n/%03d 네시간 ~ %s' % (m, d.strftime('%m-%d %H:%M'))
        m += 30
        d += datetime.timedelta(minutes=30)
        msg += '\n/%03d 네시간 삼십분 ~ %s' % (m, d.strftime('%m-%d %H:%M'))
        m += 30
        d += datetime.timedelta(minutes=30)
        msg += '\n/%03d 다섯시간 ~ %s' % (m, d.strftime('%m-%d %H:%M'))
        m += 30
        d += datetime.timedelta(minutes=30)
        msg += '\n/%03d 다섯시간 삼십분 ~ %s' % (m, d.strftime('%m-%d %H:%M'))
        m += 30
        d += datetime.timedelta(minutes=30)
        msg += '\n/%03d 여섯시간 ~ %s' % (m, d.strftime('%m-%d %H:%M'))
        m += 30
        d += datetime.timedelta(minutes=30)
        msg += '\n/%03d 여섯시간 삼십분 ~ %s' % (m, d.strftime('%m-%d %H:%M'))
        m += 30
        d += datetime.timedelta(minutes=30)
        msg += '\n/%03d 일곱시간 ~ %s' % (m, d.strftime('%m-%d %H:%M'))
        m += 30
        d += datetime.timedelta(minutes=30)
        msg += '\n/%03d 일곱시간 삼십분 ~ %s' % (m, d.strftime('%m-%d %H:%M'))
        m += 30
        d += datetime.timedelta(minutes=30)
        msg += '\n/%03d 여덟시간 ~ %s' % (m, d.strftime('%m-%d %H:%M'))
        m += 30
        d += datetime.timedelta(minutes=30)
        msg += '\n/%03d 여덟시간 삼십분 ~ %s' % (m, d.strftime('%m-%d %H:%M'))
        m += 30
        d += datetime.timedelta(minutes=30)
        msg += '\n/%03d 아홉시간 ~ %s' % (m, d.strftime('%m-%d %H:%M'))
        m += 30
        d += datetime.timedelta(minutes=30)
        msg += '\n/%03d 아홉시간 삼십분 ~ %s' % (m, d.strftime('%m-%d %H:%M'))
        m += 30
        d += datetime.timedelta(minutes=30)
        msg += '\n/%03d 열시간 ~ %s' % (m, d.strftime('%m-%d %H:%M'))
        m += 30
        d += datetime.timedelta(minutes=30)
        msg += '\n/%03d 열시간 삼십분 ~ %s' % (m, d.strftime('%m-%d %H:%M'))
        return msg
    def msg(self, m):
        if self.phase == 'WAITINGTIMER':
            self.timer = m[1:]
            r = re.match('\d{3}', self.timer)
            if r:
                self.phase = 'WAITINGDI'
                return self.menu_di()
            else: return -1
        elif self.phase == 'WAITINGDI':
            self.di= m[1:]
            r = re.match('\d{3}', self.di)
            if r: 
                self.phase = '' 
                key = 'cool_on?params='
                key += '1' + self.timer + self.di
                return self.rcmd(key)
            else: return -1
        elif(m == '/on'):
            self.phase = 'WAITINGTIMER'
            return self.menu_timer()
        elif(m == '/off'):
            self.phase = ''
            key = 'cool_on?params='
            key += '0'
            return self.rcmd(key)
        elif(m == '/status'):
            self.phase = ''
            key = ''
            return self.rcmd(key)
        else:
            self.phase = ''
            return -1

home    = Menu('/start', '시작하기')
bedroom = Menu('/bedroom', '침실 작업')
library = Menu('/library', '서재 작업')
aircon0 = DeviceAircon('/aircon', '침실 에어컨', '192.168.0.25')
aircon1 = DeviceAircon('/aircon', '서재 에어컨', '192.168.0.26')

home.addchild(bedroom) 
home.addchild(library)

bedroom.parent(home)
bedroom.addchild(aircon0)

library.parent(home)
library.addchild(aircon1)

aircon0.parent(bedroom)
aircon1.parent(library)


def handle(msg):
    chat_id  = msg['chat']['id']
    command = msg['text']
    msg = ''
    print 'Got command: %s %s' % (command, datetime.datetime.now().strftime('%m-%d %H:%M'))
    if command == '/back':
        if handle.activemenu != home : 
            handle.activemenu = handle.activemenu.getparent()
        msg = handle.activemenu.menu()
    elif command == '/start':
        handle.activemenu = home
        msg = home.menu()
    else:
        __msg = handle.activemenu.msg(command) 
        if __msg  != -1:
            nextmsg = __msg
            if isinstance(nextmsg, Menu):
                handle.activemenu = nextmsg
                msg = nextmsg.menu()
            else:
                msg = nextmsg
        else: 
            msg = '\n\n뭔가 잘못되었어요 ㅠㅠ'
    bot.sendMessage(chat_id, msg)
    bot.sendMessage(chat_id,  handle.activemenu.common())

handle.activemenu = home

bot = telepot.Bot(MYTOKEN)
bot.message_loop(handle)

print 'I am listening ...'
while 1:
    time.sleep(10)

