#!/usr/bin/python3
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
import logging
from telepot.loop import MessageLoop
from telepot.namedtuple import ReplyKeyboardRemove, InlineKeyboardMarkup, InlineKeyboardButton
from pprint import pprint
from myconfig import *
##
##
logging.basicConfig(filename='telebot.log', level=logging.INFO)
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
        return [[InlineKeyboardButton(text='Home', callback_data='/start'), InlineKeyboardButton(text='Back', callback_data='/back')]]
    def setup(self):
        pass
    def istoday(self, h, d):
        mood=''
        if h>='00' and h<'06':
            mood='AM'
        elif h>='06' and h<'12':
            mood='AM'
        elif h>='12' and h<'18':
            mood='PM'
        elif h>='18' and h<'24':
            mood='PM'

        t = datetime.datetime.now()
        if d ==  t.strftime('%m-%d'):
            mood = 'Today ' + mood
        else:
            mood = 'Tomorrow ' + mood
        return mood
    def handler(self):
        return self
    def msg(self, m):
        child = ''
        if self.child:
            for c in self.child:
                if c.name == m:
                    c.setup()
                    return c.handler()
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
                r += b + ' > '
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
##
class DeviceAntifreeze(Menu):
    def __init__(self, name, desc, ip):
        Menu.__init__(self, name, desc)
        self.ip     = ip
        self.cmd    = [{'desc':'Status', 'name':'/status'}]
        self.timer  = ''
        self.phase  = ''
    def setup(self):
        self.phase = ''
    def menu(self):
        return {'menu':self.cmd, 'desc':self.getbreadcrumb()}
    def remoji(self, status):
        if status == 0:
            __status = 'Off'
        elif status == 1:
            __status = 'On'
        else:
            __status =  status
        return __status
    def rcmd(self, key):
        fcmd = 'http://'
        fcmd += self.ip
        if key != '':
            r = requests.post(fcmd, json={"ctrl":key})  # url is cmd Rest API
        else:
            r = requests.get(fcmd)  # get status
        j = r.json()[u'variables'][0]
        msg = '[%s]' % self.getbreadcrumb()
        msg += '\nHostname:  %s' % j['Hostname']
        msg += '\nCtrl: %s' % self.remoji(j['Ctrl'])
        msg += '\nTemp: %s C'  % self.remoji(j['Temp'])
        return msg
    def msg(self, m):
        if(m == '/status'):
            self.phase = ''
            key = ''
            return self.rcmd(key)
        else:
            self.phase = ''
            return -1
##
class DeviceBulb(Menu):
    def __init__(self, name, desc, ip):
        Menu.__init__(self, name, desc)
        self.ip     = ip
        self.cmd    = [{'desc':'On', 'name':'/on'}, {'desc':'Off', 'name':'/off'}, {'desc':'Status', 'name':'/status'}]
        self.timer  = ''
        self.phase  = ''
    def setup(self):
        self.phase = ''
    def menu(self):
        return {'menu':self.cmd, 'desc':self.getbreadcrumb()}
    def remoji(self, status):
        if status == 0:
            __status = 'Off'
        elif status == 1:
            __status = 'On'
        else:
            __status =  status
        return __status
    def rcmd(self, key):
        fcmd = 'http://'
        fcmd += self.ip
        if key != '':
            r = requests.post(fcmd, json={"ctrl":key})  # url is cmd Rest API
        else:
            r = requests.get(fcmd)  # get status
        j = r.json()[u'variables'][0]
        msg = '[%s]' % self.getbreadcrumb()
        msg += '\nHostname:  %s' % j['Hostname']
        msg += '\nTime left: %s Hrs' % (j['Timer']/60.0/60)
        return msg
    def menu_timer(self):
        menu = []
        msg = ''
        d = datetime.datetime.now()
        for x in range(30, 540, 30):
            d += datetime.timedelta(minutes=30)
            msg = 'Timer %d : %d (%s %s)' % (x/60, x%60, self.istoday(d.strftime('%H'), d.strftime('%m-%d')), d.strftime('%H:%M'))
            menu.append({'desc':msg, 'name':'/%03d' % (x)})
        return {'desc':'Setting timer...', 'menu':menu}
    def msg(self, m):
        if self.phase == 'WAITINGTIMER':
            self.timer = m[1:]
            r = re.match('\d{3}', self.timer)
            if r:
                self.phase = ''
                key = '1' + self.timer
                return self.rcmd(key)
            else: return -1
        elif(m == '/on'):
            self.phase = 'WAITINGTIMER'
            return self.menu_timer()
        elif(m == '/off'):
            self.phase = ''
            key = '0000'
            return self.rcmd(key)
        elif(m == '/status'):
            self.phase = ''
            key = ''
            return self.rcmd(key)
        else:
            self.phase = ''
            return -1
##
class DeviceAircon(Menu):
    def __init__(self, name, desc, ip):
        Menu.__init__(self, name, desc)
        self.ip     = ip
        self.cmd    = [{'desc':'On', 'name':'/on'}, {'desc':'Off', 'name':'/off'}, {'desc':'Status', 'name':'/status'}]
        self.di     = ''
        self.timer  = ''
        self.phase  = ''
    def setup(self):
        self.phase = ''
    def menu(self):
        return {'menu':self.cmd, 'desc':self.getbreadcrumb()}
    def rcmd(self, key):
        fcmd = 'http://'
        fcmd += self.ip
        if key != '':
            r = requests.post(fcmd, json={"ctrl":key})  # url is cmd Rest API
        else:
            r = requests.get(fcmd)  # get status
        j = r.json()[u'variables'][0]
        msg = '%s' % self.getbreadcrumb()
        msg += '\nHostname:  %s' % j['Hostname']
        msg += '\nTemp:  %2.2f c' % j['Temp']
        msg += '\nHumi: %2.2f %%'  % j['Humi']
        msg += '\nDI: %2.2f'  % j['DI']
        msg += '\nDICtrl: %d'  % j['DICtrl']
        msg += '\nTime left: %2.2f Hrs' % (j['Timer']/60.0/60)
        return msg
    def menu_di(self)   :
        menu=[]
        menu.append({'desc':'70', 'name':'/070'})
        menu.append({'desc':'71', 'name':'/071'})
        menu.append({'desc':'72', 'name':'/072'})
        menu.append({'desc':'73', 'name':'/073'})
        menu.append({'desc':'74', 'name':'/074'})
        menu.append({'desc':'75', 'name':'/075'})
        menu.append({'desc':'76', 'name':'/076'})
        return {'desc':'Setting DI...', 'menu':menu}
    def menu_timer(self):
        menu = []
        msg = ''
        d = datetime.datetime.now()
        for x in range(30, 540, 30):
            d += datetime.timedelta(minutes=30)
            msg = 'Timer %d:%d (%s %s)' % (x/60, x%60, self.istoday(d.strftime('%H'), d.strftime('%m-%d')), d.strftime('%H:%M'))
            menu.append({'desc':msg, 'name':'/%03d' % (x)})
        return {'desc':'Setting Timer...', 'menu':menu}
    def msg(self, m):
        if self.phase == 'WAITINGTIMER':
            self.timer = m[1:]
            r = re.match('\d{3}', self.timer)
            if r:
                self.phase = ''
                key = '1' + self.timer + self.di
                return self.rcmd(key)
            else: return -1
        elif self.phase == 'WAITINGDI':
            self.di= m[1:]
            r = re.match('\d{3}', self.di)
            if r:
                self.phase = 'WAITINGTIMER'
                return self.menu_timer()
            else: return -1
        elif(m == '/on'):
            self.phase = 'WAITINGDI'
            return self.menu_di()
        elif(m == '/off'):
            self.phase = ''
            key = '0'
            return self.rcmd(key)
        elif(m == '/status'):
            self.phase = ''
            key = ''
            return self.rcmd(key)
        else:
            self.phase = ''
            return -1
##
class DeviceClimate(DeviceAircon):
    def __init__(self, name, desc, ip):
        DeviceAircon.__init__(self, name, desc, ip)
        self.cmd    = [{'desc':'Status', 'name':'/status'}]
    def handler(self):
        fcmd = 'http://'
        fcmd += self.ip
        fcmd += '/'
        r = requests.get(fcmd)  # get status
        j = r.json()[u'variables'][0]
        msg = '%s' % self.getbreadcrumb()
        msg += '\nHostname:  %s' % j['Hostname']
        msg += '\nTemp:  %2.2f c' % j['Temp']
        msg += '\nHumi: %2.2f %%'  % j['Humi']
        msg += '\nDI: %2.2f'  % j['DI']
        return msg
##
def getInlineButton(chat_id, menu):
    __keyboard = []
    for m in menu['menu']:
        __keyboard.append([InlineKeyboardButton(text=m['desc'], callback_data=m['name'])])
    __keyboard = __keyboard + activemenu.common()
    keyboard = InlineKeyboardMarkup(inline_keyboard=__keyboard)
    bot.sendMessage(chat_id, menu['desc'], reply_markup=keyboard)
    return
##
def handle(msg, chat_id):
    global activemenu
    if chat_id not in ALLOWED_IDS:
        bot.sendMessage(chat_id, 'You are not allowed')
        return
    elif re.match(r'/back', msg):
        if activemenu != home:
            activemenu = activemenu.getparent()
        getInlineButton(chat_id, activemenu.menu())
    elif re.match(r'/start', msg):
        markup = ReplyKeyboardRemove()
        bot.sendMessage(chat_id, 'Starting...', reply_markup=markup)
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
            msg = '\n\nSomething went wrong!'
            bot.sendMessage(chat_id, msg)
            getInlineButton(chat_id, activemenu.menu())
##
def on_chat_message(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)
    handle(msg['text'], chat_id)
##
def on_callback_query(msg):
    query_id, from_id, query_data = telepot.glance(msg, flavor='callback_query')
    bot.answerCallbackQuery(query_id, text='Got it')
    handle(query_data, ROOM_ID)
##
home    = Menu('/start', 'Home')
bedroom = Menu('/bedroom', 'Bedroom')
library = Menu('/library', 'Library')
outdoor = Menu('/outdoor', 'Outdoor')
ac_bedroom = DeviceAircon('/aircon', 'A/C', '192.168.0.25')
temp0 = DeviceClimate('/temp', 'Temp', '192.168.0.25')
ac_library = DeviceAircon('/aircon', 'A/C', '192.168.0.26')
temp1 = DeviceClimate('/temp', 'Temp', '192.168.0.26')
chain_bulb = DeviceBulb('/bulb', 'Light', '192.168.0.28')
antifreeze = DeviceAntifreeze('/antifreeze', 'Heat wire', '192.168.0.27')
##
home.addchild(bedroom)
home.addchild(library)
home.addchild(outdoor)
##
bedroom.setparent(home)
bedroom.addchild(ac_bedroom)
bedroom.addchild(temp0)
##
library.setparent(home)
library.addchild(ac_library)
library.addchild(temp1)
##
outdoor.setparent(home)
outdoor.addchild(chain_bulb)
outdoor.addchild(antifreeze)
##
ac_bedroom.setparent(bedroom)
ac_library.setparent(library)
##
temp0.setparent(bedroom)
temp1.setparent(library)
##
chain_bulb.setparent(outdoor)
antifreeze.setparent(outdoor)
##
bot = telepot.Bot(MYTOKEN)
##
activemenu = home
##
MessageLoop(bot, {'chat': on_chat_message,
                  'callback_query': on_callback_query}).run_as_thread()
logging.info('Listening ...')
##
while 1:
    time.sleep(10)

