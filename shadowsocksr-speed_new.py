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

ping_test=True
network_test=True
speed_test=True
youtube_test=True

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
        if(kwargs):
            kwargs['select'] = "√" if kwargs['select'] else "×"
            content=[
                kwargs['select'],
                kwargs['name'],
            ]
            self.x.add_row(content)
    def str(self):
        return str(self.x)
        
def SelectTable(screen):
    select_table=DrawSelectTable()
    ssr_config=getss()
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
    table_cols=100
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
            # print(key)
            # window.addstr(ts.table_to_str())
            # swin = curses.newwin(9, 20,20,10)
            # swin.border(0, 0, 0, 0, 0, 0, 0, 0)

            # curses.newwin(nlines, ncols)
            # curses.newwin(nlines, ncols, begin_y, begin_x)
            # Return a new window, whose left-upper corner is at (begin_y, begin_x), and whose height/width is nlines/ncols
            if ss_select < ss_select_x : ss_select=ss_select_x 
            if ss_select > max_select : ss_select=max_select

            # wisn=curses.newwin(0, 4,0,0)
            # twin = curses.newpad(table_line, table_cols)
            screen.clear()
            select_x=ss_select if ss_select < max_line else max_line -1 
            screen.addstr(int(select_x),1,str("->"))
            screen.refresh()
            # window.refresh([pminrow, pmincol, sminrow, smincol, smaxrow, smaxcol])

            # screen.clear()
            # screen.addstr(0,0 , data)
            # screen.refresh()
            spad = curses.newpad(1, 2)
            spad.scrollok(1)
            spad.idlok(1)
            spad.addstr(str(">"))
            # spad.refresh(ss_select,0,0,1,max_line,table_cols) 
            # twin.getch()
            tpad = curses.newpad(table_line, table_cols)
            tpad.scrollok(1)
            tpad.idlok(1)
            tpad.addstr(select_table.str())
            if ss_select >= max_line :
                move_x= ss_select - max_line +1 
            else :
                move_x= 0
            tpad.refresh(move_x,0,table_y,table_x,max_line,table_cols)  

            # twin = curses.newwin(table_line, table_cols,table_y,table_x)
            # # twin.border(0)
            # twin.scrollok(1)
            # twin.idlok(1)
            # # for x in range(0,20):
            # #     twin.addstr(0,2,str(x))
            # #     twin.scroll(1)
            # twin.addstr(select_table.str())
            # # twin.scroll(20)
            # twin.refresh()
            # twin.refresh(0,0,0,4,3,80)    
            # twin.getch()

            # mypadn = curses.newpad(30,4,10,0)
            # mypadn.scrollok(1)
            # mypadn.idlok(1)
            # for x in range(1,10):
            #   mypadn.addstr(10,1, str(x))
            #   mypadn.scroll(1)
            # mypadn.refresh(0,0, 0,4, 2, 4+4)

            # screen.refresh()

            # swin = curses.newwin(9, 20,10,10)
            # swin.border(0, 0, 0, 0, 0, 0, 0, 0)
            # swin.addstr(2, 4, "Time:          ")
            # swin.addstr(4, 4, "Mines:         ")
            # swin.refresh()
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
                    # test_ssr=ssr_config
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

    # screen.erase()
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
    port="6667"
    if('protoparam' in ssr):
        cmd="python shadowsocksr/shadowsocks/local.py -qq -s %s -p %s -k %s -m %s -O %s -G %s -o %s -g %s -b %s -l %s" % (ssr['server'],ssr['port'],ssr['password'],ssr['method'],ssr['protocol'],ssr['protoparam'],ssr['obfs'],ssr['obfsparam'],"127.0.0.1",port)
    else:
        cmd="python shadowsocksr/shadowsocks/local.py -qq -s %s -p %s -k %s -m %s -O %s -o %s -g %s -b %s -l %s" % (ssr['server'],ssr['port'],ssr['password'],ssr['method'],ssr['protocol'],ssr['obfs'],ssr['obfsparam'],"127.0.0.1",port)
    os.system(cmd + " -d stop")
    os.system(cmd + " -d start")

    print("----------------------------")
    print(ssr['remarks']+"/"+ssr['server'])

    if ping_test:
        ping_len="7" if isIP(result['host']) else "8"
        cmd="ping -c 5 %s |grep 'time=' | awk '{print $%s}' |cut -b 6-"% (result['host'],ping_len)
        ping_pc=os.popen(cmd).readlines()
        if(len(ping_pc)):
          ping_pc=int(float(ping_pc[0].strip()))
        print("ping_test,localPing:",ping_pc)
        result['ping_pc']=ping_pc

    socks.set_default_proxy(socks.SOCKS5, "127.0.0.1", int(port))
    socket.socket = socks.socksocket
    if network_test:
        ip=requests.get('http://api.ip.sb/ip',timeout=15).text.strip()
        result['ip']=ip
        print("network_test,ip:",result['ip'])

    if speed_test:
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

    if youtube_test:
        socket.socket=default_socket
        youtube=youtube_speed.test_speed(port)
        youtube=int(re.sub("\D", "", youtube))
        result['youtube']=youtube
        print("youtube_test,speed:",youtube)
    result['state']="Success"
    return result

  except Exception as e:
    # cmd="ping -c 5 %s |grep 'time=' | awk '{print $8}' |cut -b 6-"% result['host']
    # ping_pc=os.popen(cmd).readlines()#.strip()
    # if(len(ping_pc)):
    #   ping_pc=ping_pc[0].strip()
    # result['ping_pc']=ping_pc
    # print("ping_local",ping_pc)
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
sss=curses.wrapper(SelectTable)

# for s in ssr_config:
#   speed_result.append(connect_ssr(s))#通过解析后的配置信息链接节点进行测速
#   # print(speed_result)

# #将测速结果生产为表格
# table=PrettyTable(["name","ip","localPing","ping","upload","download","youtube"])
# table.sortby = "youtube"#以"download"下载速度为排序根据
# table.reversesort = True
# for t in speed_result:
#     table.add_row([t['remarks'],t['ip'],t['ping_pc'],t['ping'],t['upload'],t['download'],t['youtube']])
# print(table)

table=DrawTable()

for s in ssr_config:
  speed_result=connect_ssr(s)#通过解析后的配置信息链接节点进行测速
  print(speed_result)
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

