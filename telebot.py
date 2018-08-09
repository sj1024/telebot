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
from telepot.loop import MessageLoop
from telepot.namedtuple import ReplyKeyboardRemove, InlineKeyboardMarkup, InlineKeyboardButton
from pprint import pprint
from myconfig import MYTOKEN

reload(sys)
sys.setdefaultencoding('utf8')

class Menu:
    def __init__(self, name, desc):
        self.name = name
        self.desc = desc
        self.parent = None
        self.child=[]
        self.cmd=[]
        self.bread=[]
    def addchild(self, child):
        self.child.append(child)
    def setparent(self, parent):
        self.parent = parent
    def setcmd(self, cmd):
        self.cmd.append(cmd)
    def common(self):
        return [[InlineKeyboardButton(text='🏠 시작', callback_data='/start'), InlineKeyboardButton(text='↩️  뒤로', callback_data='/back')]]
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
    def getbreadcrumb(self, buf=None): 
        if buf ==None:
            buf=[]
        buf.insert(0, self.desc)
        if self.getparent() != -1:
            return self.getparent().getbreadcrumb(buf)
        else:
            r=''
            for b in buf:
                r += b + ' » '
            return r[:-3]
    def menu(self): 
        menu = [] 
        if self.child:
            for m in self.child:
                menu.append({'name': m.name, 'desc': m.desc})
        return {'menu':menu, 'desc':self.getbreadcrumb()}
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
        Menu.__init__(self, name, desc)
        self.ip     = ip
        self.cmd    = [{'desc':'에어컨 켜기', 'name':'/on'}, {'desc':'에어컨 끄기', 'name':'/off'}, {'desc':'⚙️  에어컨 상태보기', 'name':'/status'}]
        self.di     = ''
        self.timer  = ''
        self.phase  = ''
    def setup(self):
        self.phase = ''
    def menu(self):
        return {'menu':self.cmd, 'desc':self.getbreadcrumb()}
    def rcmd(self, key):
        print 'http://' + self.ip + '/' + key
        fcmd = 'http://'
        fcmd += self.ip
        fcmd += '/'
        if key != '':
            requests.get(fcmd+key)  # url is cmd Rest API
            time.sleep(1)
        r = requests.get(fcmd)  # get status
        j = r.json()[u'variables']
        msg = 'ℹ️ '
        msg += '\n❄️  에어컨 상태: %s' % (j['Status Cool'])
        msg += '\n🔥 히터 상태: %s' % (j['Status Heat'])
        msg += '\n🌡 방 온도: %s' % (j['Temp'])
        msg += '\n💦 방 습도: %s' % (j['Humi'])
        msg += '\n😕 방 불쾌지수: %s' % (j['DI'])
        msg += '\n⏰ 타이머 남은 시간(분): %s' % (j['timer_ctrl'])
        msg += '\n⚙️  설정된 불쾌지수: %s' % (j['di_ctrl'])
        msg += '\n⚙️  설정된 히터온도: %s' % (j['heat_ctrl'])
        '''
        {"Status Heat":"RELAY_OFF","Temp":34.0,"DI":79.34,
        "timer_ctrl":87,"Humi":24.0,"di_ctrl":79,"Status Cool":"RELAY_ON","heat_ctrl":-999}
        
        '''
        return msg
    def menu_di(self):
        menu=[]
        menu.append({'desc':'68, 😄 불쾌감을 느끼는 사람 없음', 'name':'/068'})
        menu.append({'desc':'69',  'name':'/069'})
        menu.append({'desc':'70', 'name':'/070'})
        menu.append({'desc':'71', 'name':'/071'})
        menu.append({'desc':'72, 😕', 'name':'/072'})
        menu.append({'desc':'73', 'name':'/073'})
        menu.append({'desc':'74', 'name':'/074'})
        menu.append({'desc':'75, ☹️  약 50% 인간이 불쾌감을 느끼기 시작함', 'name':'/075'})
        menu.append({'desc':'76', 'name':'/076'})
        menu.append({'desc':'77', 'name':'/077'})
        menu.append({'desc':'78', 'name':'/078'})
        menu.append({'desc':'79', 'name':'/079'})
        menu.append({'desc':'80, 😣 모든 인간이 불쾌감을 느끼기 시작함' , 'name':'/080'})
        menu.append({'desc':'81', 'name':'/081'})
        menu.append({'desc':'82', 'name':'/082'})
        menu.append({'desc':'83', 'name':'/083'})
        menu.append({'desc':'84', 'name':'/084'})
        menu.append({'desc':'85, 😩', 'name':'/085'})
        menu.append({'desc':'86', 'name':'/086'})
        menu.append({'desc':'87', 'name':'/087'})
        menu.append({'desc':'88', 'name':'/088'})
        menu.append({'desc':'89, 😫', 'name':'/089'})
        return {'desc':'불쾌지수를 설정합니다', 'menu':menu}
    def menu_timer(self):
        d = datetime.datetime.now()
        menu = []
        m = 30
        d += datetime.timedelta(minutes=30)
        msg = '삽십분 ~ ~ %s' % (d.strftime('%m-%d %H:%M'))
        menu.append({'desc':msg, 'name':'/%03d' % m})
        m += 30
        d += datetime.timedelta(minutes=30)
        msg = '한시간 ~ %s' % (d.strftime('%m-%d %H:%M'))
        menu.append({'desc':msg, 'name':'/%03d' % m})
        m += 30
        d += datetime.timedelta(minutes=30)
        msg = '한시간 삼십분 ~ %s' % (d.strftime('%m-%d %H:%M'))
        menu.append({'desc':msg, 'name':'/%03d' % m})
        m += 30
        d += datetime.timedelta(minutes=30)
        msg = '두시간 ~ %s' % (d.strftime('%m-%d %H:%M'))
        menu.append({'desc':msg, 'name':'/%03d' % m})
        m += 30
        d += datetime.timedelta(minutes=30)
        msg = '두시간 삼십분 ~ %s' % (d.strftime('%m-%d %H:%M'))
        menu.append({'desc':msg, 'name':'/%03d' % m})
        m += 30
        d += datetime.timedelta(minutes=30)
        msg = '세시간 ~ %s' % (d.strftime('%m-%d %H:%M'))
        menu.append({'desc':msg, 'name':'/%03d' % m})
        m += 30
        d += datetime.timedelta(minutes=30)
        msg = '세시간 삼십분 ~ %s' % (d.strftime('%m-%d %H:%M'))
        menu.append({'desc':msg, 'name':'/%03d' % m})
        m += 30
        d += datetime.timedelta(minutes=30)
        msg = '네시간 ~ %s' % (d.strftime('%m-%d %H:%M'))
        menu.append({'desc':msg, 'name':'/%03d' % m})
        m += 30
        d += datetime.timedelta(minutes=30)
        msg = '네시간 삼십분 ~ %s' % (d.strftime('%m-%d %H:%M'))
        menu.append({'desc':msg, 'name':'/%03d' % m})
        m += 30
        d += datetime.timedelta(minutes=30)
        msg = '다섯시간 ~ %s' % (d.strftime('%m-%d %H:%M'))
        menu.append({'desc':msg, 'name':'/%03d' % m})
        m += 30
        d += datetime.timedelta(minutes=30)
        msg = '다섯시간 삼십분 ~ %s' % (d.strftime('%m-%d %H:%M'))
        menu.append({'desc':msg, 'name':'/%03d' % m})
        m += 30
        d += datetime.timedelta(minutes=30)
        msg = '여섯시간 ~ %s' % (d.strftime('%m-%d %H:%M'))
        menu.append({'desc':msg, 'name':'/%03d' % m})
        m += 30
        d += datetime.timedelta(minutes=30)
        msg = '여섯시간 삼십분 ~ %s' % (d.strftime('%m-%d %H:%M'))
        menu.append({'desc':msg, 'name':'/%03d' % m})
        m += 30
        d += datetime.timedelta(minutes=30)
        msg = '일곱시간 ~ %s' % (d.strftime('%m-%d %H:%M'))
        menu.append({'desc':msg, 'name':'/%03d' % m})
        m += 30
        d += datetime.timedelta(minutes=30)
        msg = '일곱시간 삼십분 ~ %s' % (d.strftime('%m-%d %H:%M'))
        menu.append({'desc':msg, 'name':'/%03d' % m})
        m += 30
        d += datetime.timedelta(minutes=30)
        msg = '여덟시간 ~ %s' % (d.strftime('%m-%d %H:%M'))
        menu.append({'desc':msg, 'name':'/%03d' % m})
        m += 30
        d += datetime.timedelta(minutes=30)
        msg = '여덟시간 삼십분 ~ %s' % (d.strftime('%m-%d %H:%M'))
        menu.append({'desc':msg, 'name':'/%03d' % m})
        m += 30
        d += datetime.timedelta(minutes=30)
        msg = '아홉시간 ~ %s' % (d.strftime('%m-%d %H:%M'))
        menu.append({'desc':msg, 'name':'/%03d' % m})
        m += 30
        d += datetime.timedelta(minutes=30)
        msg = '아홉시간 삼십분 ~ %s' % (d.strftime('%m-%d %H:%M'))
        menu.append({'desc':msg, 'name':'/%03d' % m})
        m += 30
        d += datetime.timedelta(minutes=30)
        msg = '열시간 ~ %s' % (d.strftime('%m-%d %H:%M'))
        menu.append({'desc':msg, 'name':'/%03d' % m})
        m += 30
        d += datetime.timedelta(minutes=30)
        msg = '열시간 삼십분 ~ %s' % (d.strftime('%m-%d %H:%M'))
        menu.append({'desc':msg, 'name':'/%03d' % m})
        return {'desc':'⏰ 타이머를 설정합니다', 'menu':menu}
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

class DeviceTemp(DeviceAircon):
    def __init__(self, name, desc, ip):
        DeviceAircon.__init__(self, name, desc, ip)
        self.cmd    = [{'desc':'🌡  온/습도 불쾌지수 보기', 'name':'/status'}]
    def msg(self, m):
        if(m == '/status'):
            return self.rcmd('')
        else:
            return -1

def getInlineButton(chat_id, menu):
    __keyboard = []
    for m in menu['menu']:
        __keyboard.append([InlineKeyboardButton(text=m['desc'], callback_data=m['name'])])
    __keyboard = __keyboard + activemenu.common()
    keyboard = InlineKeyboardMarkup(inline_keyboard=__keyboard)
    bot.sendMessage(chat_id, menu['desc'], reply_markup=keyboard)
    return 

def handle(msg, chat_id):
    global activemenu
    if msg == '/back':
        if activemenu != home:
            activemenu = activemenu.getparent()
        getInlineButton(chat_id, activemenu.menu())
    elif msg == '/start':
        markup = ReplyKeyboardRemove()
        bot.sendMessage(chat_id, '시작합니다', reply_markup=markup)
        activemenu = home
        getInlineButton(chat_id, activemenu.menu())
    else:
        __msg = activemenu.msg(msg)
        if __msg != -1:
            nextmsg = __msg
            if isinstance(nextmsg, Menu):
                activemenu = nextmsg
                getInlineButton(chat_id, activemenu.menu())
            else:
                r = nextmsg
                if type(r) == dict: 
                    getInlineButton(chat_id, r)
                else:
                    bot.sendMessage(chat_id, r)
                    getInlineButton(chat_id, activemenu.menu())
        else:
            msg = '\n\n뭔가 잘못되었어요 ㅠㅠ'
            bot.sendMessage(chat_id, msg)
            getInlineButton(chat_id, activemenu.menu())

def on_chat_message(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)
    handle(msg['text'], chat_id)

def on_callback_query(msg):
    query_id, from_id, query_data = telepot.glance(msg, flavor='callback_query')
    bot.answerCallbackQuery(query_id, text='Got it')
    handle(query_data, from_id)

home    = Menu('/start', '🏠 시작하기')
bedroom = Menu('/bedroom', '🛏  침실 작업')
library = Menu('/library', '💻 서재 작업')
aircon0 = DeviceAircon('/aircon', '❄️  에어컨', '192.168.0.25')
temp0 = DeviceTemp('/temp', '🌡  온습도계', '192.168.0.25')
aircon1 = DeviceAircon('/aircon', '❄️  에어컨', '192.168.0.26')
temp1 = DeviceTemp('/temp', '🌡  온습도계', '192.168.0.26')


home.addchild(bedroom) 
home.addchild(library)

bedroom.setparent(home)
bedroom.addchild(aircon0)
bedroom.addchild(temp0)

library.setparent(home)
library.addchild(aircon1)
library.addchild(temp1)

aircon0.setparent(bedroom)
aircon1.setparent(library)

temp0.setparent(bedroom)
temp1.setparent(library)

bot = telepot.Bot(MYTOKEN)

activemenu = home

MessageLoop(bot, {'chat': on_chat_message,
                  'callback_query': on_callback_query}).run_as_thread()
print('Listening ...')

while 1:
    time.sleep(10)

