import urllib.request
import base64
# import shadowsocksr.shadowsocks
import os
import time
import requests
import ParseSsr #https://www.jianshu.com/p/81b1632bea7f
from prettytable import PrettyTable

def connect_ssr(ssr):
  try:
    port="6667"
    cmd="python shadowsocksr/shadowsocks/local.py -qq -s %s -p %s -k %s -m %s -O %s -o %s -g %s -b %s -l %s" % (ssr['server'],ssr['port'],ssr['password'],ssr['method'],ssr['protocol'],ssr['obfs'],ssr['obfsparam'],"127.0.0.1",port)
    os.system(cmd + " -d stop")
    os.system(cmd + " -d start")

    print("----------------------------")
    print(ssr['remarks']+"/"+ssr['server'])
    import socket
    import socks
    socks.set_default_proxy(socks.SOCKS5, "127.0.0.1", int(port))
    socket.socket = socks.socksocket
    ip=requests.get('http://api.ip.sb/ip',timeout=30).text

    result={}
    result['host']=ssr['server']
    result['remarks']=ssr['remarks']
    result['ip']=ip.strip()
    print(result['ip'])
    cmd="ping -c 1 %s |grep 'time=' | awk '{print $8}' |cut -b 6-"% result['host']
    ping_pc=os.popen(cmd).readlines()#.strip()
    if(len(ping_pc)):
      ping_pc=ping_pc[0].strip()
    print("ping_pc",ping_pc)

    import speedtest
    s = speedtest.Speedtest()
    s.get_best_server()
    s.download()
    s.upload()
    s.results.share()
    results_dict = s.results.dict()
    result['ping_pc']=ping_pc
    result['ping']=results_dict['ping']
    result['download']=round(results_dict['download'] / 1000.0 / 1000.0,2)
    result['upload']=round(results_dict['upload'] / 1000.0 / 1000.0 ,2)
    result['action']="Success"
    print(result['ping'],"/",result['ping_pc'])
    print(result['download'],"Mbit/s")
    print(result['upload'],"Mbit/s")
    return result

  except Exception as e:
    result={}
    result['host']=ssr['server']
    result['remarks']=ssr['remarks']
    result['ip']=''
    result['download']=0
    result['upload']=0
    result['ping']=0
    result['action']="Fail"
    cmd="ping -c 1 %s |grep 'time=' | awk '{print $8}' |cut -b 6-"% result['host']
    ping_pc=os.popen(cmd).readlines()#.strip()
    if(len(ping_pc)):
      ping_pc=ping_pc[0].strip()
    result['ping_pc']=ping_pc
    print (e)

    return result
    

url=input("url:")
ssr_config=[]
speed_result=[]
headers = {'User-Agent': 'User-Agent:Mozilla/5.0'}
f=urllib.request.Request(url,headers=headers) 
ssr_subscribe = urllib.request.urlopen(f).read() #获取ssr订阅链接中数据
ssr_subscribe_decode = base64.b64decode(ssr_subscribe).decode('utf-8')
ssr_subscribe_decode=ssr_subscribe_decode.split('\r\n')

for i in ssr_subscribe_decode:
	if(i):
		decdata=str(i[6:])#去掉"SSR://"
		ssr_config.append(ParseSsr.parse(decdata))#解析"SSR://" 后边的base64的配置信息返回一个字典
for s in ssr_config:
  speed_result.append(connect_ssr(s))#通过解析后的配置信息链接节点进行测速


#将测速结果生产为表格
table=PrettyTable(["name","ip","localPing","ping","upload","download"])
table.sortby = "download"#以"download"下载速度为排序根据
table.reversesort = True
for t in speed_result:
  table.add_row([t['remarks'],t['ip'],t['ping_pc'],t['ping'],t['upload'],t['download']])
print(table)

