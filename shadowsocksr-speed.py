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

import socket
import socks
default_socket = socket.socket

only_check_network=False

def isIP(str):
    p = re.compile('^((25[0-5]|2[0-4]\d|[01]?\d\d?)\.){3}(25[0-5]|2[0-4]\d|[01]?\d\d?)$')
    if p.match(str):
        return True
    else:
        return False

def connect_ssr(ssr):
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

    socks.set_default_proxy(socks.SOCKS5, "127.0.0.1", int(port))
    socket.socket = socks.socksocket
    ip=requests.get('http://api.ip.sb/ip',timeout=15).text

    result={}
    result['host']=ssr['server']
    result['remarks']=ssr['remarks']
    result['ip']=ip.strip()
    print(result['ip'])
    if isIP(result['host']):
        ping_len="7"
    else:
        ping_len="8"
    cmd="ping -c 1 %s |grep 'time=' | awk '{print $%s}' |cut -b 6-"% (result['host'],ping_len)

    ping_pc=os.popen(cmd).readlines()#.strip()
    if(len(ping_pc)):
      ping_pc=ping_pc[0].strip()
    print("ping_pc",ping_pc)
    result['ping_pc']=ping_pc
    if not only_check_network:
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
        print(result['ping'],"/",result['ping_pc'])
        print(result['download'],"Mbit/s")
        print(result['upload'],"Mbit/s")
        socket.socket=default_socket
        youtube=youtube_speed.test_speed(port)
        youtube=int(re.sub("\D", "", youtube))
        result['youtube']=youtube
    else:
        socket.socket=default_socket
        result['youtube']=youtube_speed.test_speed(port)
        result['download']=0
        result['upload']=0
        result['ping']=0
        result['youtube']=0
        result['state']="Success"
    return result

  except Exception as e:
    result={}
    result['host']=ssr['server']
    result['remarks']=ssr['remarks']
    result['ip']=''
    result['download']=0
    result['upload']=0
    result['ping']=0
    result['youtube']=0
    result['state']="Fail"
    cmd="ping -c 1 %s |grep 'time=' | awk '{print $8}' |cut -b 6-"% result['host']
    ping_pc=os.popen(cmd).readlines()#.strip()
    if(len(ping_pc)):
      ping_pc=ping_pc[0].strip()
    result['ping_pc']=ping_pc
    print("ping_local",ping_pc)
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
for s in ssr_config:
  speed_result.append(connect_ssr(s))#通过解析后的配置信息链接节点进行测速
speed_result.append(connect_ssr(ssr_config[4]))#通过解析后的配置信息链接节点进行测速

#将测速结果生产为表格
table=PrettyTable(["name","ip","localPing","ping","upload","download","youtube"])
table.sortby = "youtube"#以"download"下载速度为排序根据
table.reversesort = True
for t in speed_result:
    table.add_row([t['remarks'],t['ip'],t['ping_pc'],t['ping'],t['upload'],t['download'],t['youtube']])
print(table)


# for s in ssr_config:
#   speed_result=connect_ssr(s)#通过解析后的配置信息链接节点进行测速
#   print(speed_result)
#   table.add_row([speed_result['remarks'],speed_result['ip'],speed_result['ping_pc'],speed_result['ping'],speed_result['upload'],speed_result['download'],speed_result['youtube']])
#   print(table)

