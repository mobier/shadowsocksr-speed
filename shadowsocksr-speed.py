import urllib.request
import base64
# import shadowsocksr.shadowsocks
import os
import time
import requests
import ParseSsr #https://www.jianshu.com/p/81b1632bea7f
import re
import youtube_speed
from prettytable import PrettyTable
from colorama import init, Fore, Back, Style

import curses
import sys
import os

import socket
import socks
default_socket = socket.socket

test_option={}
test_option ['ping']=test_option ['network']=test_option ['speed']= test_option ['youtube']=False
max_cols=0
# 访问 youtube 网页加载时间大于设置时间直接退出不进行测速.解决高延迟的节点加载网页太慢问题
youtube_timeout=10
# 使用 访问ip.sb获取外网ip的超时时间,判断节点是否能正常访问网页的依据
network_timeout=15


init (autoreset=False)
class colored(object):
    def red(self,s):
        return Fore.LIGHTRED_EX + s + Fore.RESET
    def greed(self,s):
        return Fore.LIGHTGREEN_EX + s + Fore.RESET
    def yellow(self,s):
        return Fore.LIGHTYELLOW_EX + s + Fore.RESET
    def white(self,s):
        return Fore.LIGHTWHITE_EX + s + Fore.RESET
    def blue(self,s):
        return Fore.LIGHTBLUE_EX + s + Fore.RESET

class DrawTable(object):
    def __init__(self):
        self.table=[]
        header=[
        "name",
        "ip",
        "localPing",
        "ping",
        "upload",
        "download",
        "youtube",
        "network"
        ]
        self.x = PrettyTable(header)
        self.x.reversesort = True
        self.x.sortby = "youtube"
        
    def append(self,*args,**kwargs):
        if(kwargs):
            color=colored()
            kwargs['network'] = color.greed(kwargs['network']) if kwargs['network']=="Success" else color.red(kwargs['network'])
            kwargs['network'] = color.greed(kwargs['network']) if kwargs['youtube']!=1 else color.red("timeout")
            # kwargs['youtube'] = kwargs['youtube'] if kwargs['youtube'] !=1 else color.red("timeout")
            content=[
                kwargs['name'],
                kwargs['ip'],
                kwargs['localPing'],
                kwargs['ping'],
                kwargs['upload'],
                kwargs['download'],
                kwargs['youtube'],
                kwargs['network'],
            ]
            self.x.add_row(content)
    def str(self):
        return str(self.x)
class DrawSelectTable(object):
    def __init__(self):
        self.table=[]
        header=[
        "select",
        "name"
        ]
        self.x = PrettyTable(header)
    def append(self,*args,**kwargs):
        global max_cols
        if(kwargs):
            kwargs['select'] = "√" if kwargs['select'] else "×"
            kwargs['name']=kwargs['name'].split()[0]
            #获取名字,长度大于窗口分辨率进行报错
            if len(kwargs['name'])> max_cols:
                max_cols= len(kwargs['name'])
            content=[
                kwargs['select'],
                kwargs['name'],
            ]
            self.x.add_row(content)
    def str(self):
        return str(self.x)

def TestOption(screen):
    Option=0
    menubar = ["1 - All Test", "2 - Ping", "3 - Network", "4 - Speed", "5 - Youtube"]  
    test_select=[0,0,0,0]
    menu_len=len(menubar)
    while True:
        Option = 0 if Option<0 else Option
        Option = menu_len -1 if Option > menu_len-1 else Option 
        screen.clear()
        menuitem = selectitem = 0
        for m in menubar:  
            if Option == menuitem:  
                screen.addstr(menuitem+2, 4,m , curses.A_REVERSE)  
            else:  
                screen.addstr(menuitem+2, 4, m)  
            menuitem+=1  
        for s in test_select:
            if s:
                screen.addstr(selectitem+3, 2,"*")
            selectitem+=1
        screen.refresh()
        
        key = screen.getch()
        if key in [curses.KEY_UP, ord('w'),
            curses.KEY_DOWN, ord('s'),
            curses.KEY_LEFT, ord('a'),
            curses.KEY_RIGHT, ord('d'),
            ord('g'), ord('G'), ord('0'),
            ord('r'), ord('q'),10,32]:
            if key in [ord('w'), curses.KEY_UP]:
                Option -= 1
            if key in [ord('s'), curses.KEY_DOWN]:
                Option += 1
            if key == ord('q'):
                break
            if key == 10:
                if test_select[0]:
                    test_option['ping'] = True 
                if test_select[1]:
                    test_option['network'] = True
                if test_select[2]:
                    test_option['speed'] = True
                if test_select[3]:
                    test_option['youtube'] = True
                if Option==0:
                    test_option['youtube'] = test_option['ping'] = test_option['speed'] = test_option['network'] =True
                break
            if key in [32, curses.KEY_RIGHT,curses.KEY_LEFT]:
                if(Option!=0):
                    test_select[Option-1]= not test_select[Option-1]

def SelectTable(screen):
    select_table=DrawSelectTable()
    # ssr_config=getss()
    for x in ssr_config:
        x['select']=1
        select_table.append(select=x['select'],name=x['remarks'])
    # print(table)
    help_string1 = 'W(up) S(down)'  'A(select) D(right)'
    help_string2 = 'R(Reverse selection) Q(exit) '
    help_string3 = 'Enter(finish)'
    table_x=4
    table_y=0
    table_line=100
    table_cols=max_cols+30
    if(term_col<table_cols):
        print ("[x] Resize the terminal window more than %s"  % table_cols )
        print ("[x] Current size %dx%d" % (term_col, term_lines))
        os._exit(0)

    ss_select_x=3
    ss_select=3
    max_select=len(ssr_config)+3-1
    max_line=term_lines -1 if term_lines -1 < max_select + 3 else max_select+2
    # print(max_line)
    # while True:
    #   pass
    # print(len(ssr_config))
    while True:
        try:
            if ss_select < ss_select_x : ss_select=ss_select_x 
            if ss_select > max_select : ss_select=max_select

            screen.clear()
            select_x=ss_select if ss_select < max_line else max_line -1 
            screen.addstr(int(select_x),1,str("->"))
            screen.refresh()

            tpad = curses.newpad(table_line, table_cols)
            tpad.scrollok(1)
            tpad.idlok(1)
            tpad.addstr(select_table.str())
            if ss_select >= max_line :
                move_x= ss_select - max_line +1 
            else :
                move_x= 0
            tpad.refresh(move_x,0,table_y,table_x,max_line,table_cols)  
            key = screen.getch()
            if key in [curses.KEY_UP, ord('w'),
                curses.KEY_DOWN, ord('s'),
                curses.KEY_LEFT, ord('a'),
                curses.KEY_RIGHT, ord('d'),
                ord('g'), ord('G'), ord('0'),
                ord('r'), ord('q'),10,32]:
                if key in [ord('w'), curses.KEY_UP]:
                    ss_select -= 1
                if key in [ord('s'), curses.KEY_DOWN]:
                    ss_select += 1
                if key == ord('q'):
                    select_flag = False
                if key == ord('q'):
                    break
                if key == 10:
                    return ssr_config 
                    break
                if key == ord('r'):
                    select_table=DrawSelectTable()
                    for x in ssr_config:
                        x['select']= not x['select']
                        select_table.append(select=x['select'],name=x['remarks'])
                if key in [32, curses.KEY_RIGHT,curses.KEY_LEFT]:
                    ssr_config[ss_select-ss_select_x]['select']= not ssr_config[ss_select-ss_select_x]['select']
                    select_table=DrawSelectTable()
                    for x in ssr_config:
                        select_table.append(select=x['select'],name=x['remarks'])   
        except (KeyboardInterrupt, SystemExit):
            sys.exit("Goodbye!")


def isIP(str):
    p = re.compile('^((25[0-5]|2[0-4]\d|[01]?\d\d?)\.){3}(25[0-5]|2[0-4]\d|[01]?\d\d?)$')
    if p.match(str):
        return True
    else:
        return False

def connect_ssr(ssr):
  result={}
  result['host']=ssr['server']
  result['remarks']=ssr['remarks']
  result['ip']=''
  result['download']=0
  result['upload']=0
  result['ping']=0
  result['ping_pc']=0
  result['youtube']=0
  result['state']="Fail"
  try:
    if not ssr['select']:
        # print ("ss_pass")
        result['state']="pass"
        return result
    port="6667"
    cmd="python shadowsocksr/shadowsocks/local.py -qq -s %s -p %s -k %s -m %s -O %s -o %s -b %s -l %s " % (ssr['server'],ssr['port'],ssr['password'],ssr['method'],ssr['protocol'],ssr['obfs'],"127.0.0.1",port)
    if(len(ssr.get('protoparam',""))>1):
        cmd+="-G %s " % ssr['protoparam']
    if(len(ssr.get('obfsparam',""))>1):
        cmd+="-g %s " % ssr['obfsparam']
    os.system(cmd + " -d stop")
    os.system(cmd + " -d start")
    print(ssr['remarks']+"/"+ssr['server'])

    if test_option['ping']:
        ping_len="7" if isIP(result['host']) else "8"
        cmd="ping -c 5 %s |grep 'time=' | awk '{print $%s}' |cut -b 6-"% (result['host'],ping_len)
        ping_pc=os.popen(cmd).readlines()
        if(len(ping_pc)):
          ping_pc=int(float(ping_pc[0].strip()))
        print("ping_test,localPing:",ping_pc)
        result['ping_pc']=ping_pc

    socks.set_default_proxy(socks.SOCKS5, "127.0.0.1", int(port))
    socket.socket = socks.socksocket
    if test_option['network']:
        ip=requests.get('http://api.ip.sb/ip',timeout=15).text.strip()
        result['ip']=ip
        print("network_test,ip:",result['ip'])

    if test_option['speed']:
        import speedtest
        s = speedtest.Speedtest()
        s.get_best_server()
        s.download()
        s.upload()
        s.results.share()
        results_dict = s.results.dict()
        result['ping']=results_dict['ping']
        result['download']=round(results_dict['download'] / 1000.0 / 1000.0,2)
        result['upload']=round(results_dict['upload'] / 1000.0 / 1000.0 ,2)
        result['state']="Success"
        result['ip']=results_dict['client']['ip']
        print("speed_test,ping:%s,download:%s,upload:%s" % (result['ping'],result['download'],result['upload']))

    if test_option['youtube']:
        socket.socket=default_socket
        youtube=youtube_speed.test_speed(port,youtube_timeout)
        youtube=int(re.sub("\D", "", youtube))
        result['youtube']=youtube
        print("youtube_test,speed:",youtube)
    result['state']="Success"
    return result

  except Exception as e:
    print (e)
    return result

url=input("url:")
ssr_config=[]
speed_result=[]
headers = {'User-Agent':'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0'}
f=urllib.request.Request(url,headers=headers) 

ssr_subscribe = urllib.request.urlopen(f).read().decode('utf-8') #获取ssr订阅链接中数据
ssr_subscribe_decode = ParseSsr.base64_decode(ssr_subscribe)
ssr_subscribe_decode=ssr_subscribe_decode.replace('\r','')
ssr_subscribe_decode=ssr_subscribe_decode.split('\n')

for i in ssr_subscribe_decode:
    if(i):
        decdata=str(i[6:])#去掉"SSR://"
        ssr_config.append(ParseSsr.parse(decdata))#解析"SSR://" 后边的base64的配置信息返回一个字典

term_lines = os.get_terminal_size().lines
term_col = os.get_terminal_size().columns
ssr_config=curses.wrapper(SelectTable)

curses.wrapper(TestOption)
# print("ping:",test_option['ping'],"youtube:",test_option['youtube'],"speed:",test_option['speed'],"network:",test_option['network'])

table=DrawTable()
for s in ssr_config:
  # print(s)
  speed_result=connect_ssr(s)#通过解析后的配置信息链接节点进行测速
  # print(speed_result)
  table.append(
        name=speed_result['remarks'],
        ip=speed_result['ip'],
        localPing=speed_result['ping_pc'],
        ping=speed_result['ping'],
        upload=speed_result['upload'],
        download=speed_result['download'],
        youtube=speed_result['youtube'],
        network=speed_result['state']
    )
  print(table.str())
