import urllib.request
import base64
from prettytable import PrettyTable
# from colorama import init, Fore, Back, Style
import os
import time
import requests
import ParseSsr #https://www.jianshu.com/p/81b1632bea7f
import json
import subprocess
import re
import socket
import socks
from sys import argv
default_socket = socket.socket


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
        # "youtube",
        "network"
        ]
        self.x = PrettyTable(header)
        self.x.reversesort = True
        self.x.sortby = "download"
        
    def append(self,*args,**kwargs):
        if(kwargs):
            # color=colored()
            # kwargs['network'] = color.greed(kwargs['network']) if kwargs['network']=="Success" else color.red(kwargs['network'])
            # kwargs['network'] = color.greed(kwargs['network']) if kwargs['youtube']!=1 else color.red("timeout")
            # kwargs['youtube'] = kwargs['youtube'] if kwargs['youtube'] !=1 else color.red("timeout")
            content=[
                kwargs['name'],
                kwargs['ip'],
                kwargs['localPing'],
                kwargs['ping'],
                kwargs['upload'],
                kwargs['download'],
                # kwargs['youtube'],
                kwargs['network'],
            ]
            self.x.add_row(content)
    def str(self):
        return str(self.x)


test_option={}
test_option ['ping']=test_option ['network']=test_option ['speed']= test_option ['youtube']=True
max_cols=0
# 访问 youtube 网页加载时间大于设置时间直接退出不进行测速.解决高延迟的节点加载网页太慢问题
youtube_timeout=10
# 使用 访问ip.sb获取外网ip的超时时间,判断节点是否能正常访问网页的依据
network_timeout=15
# 测试所用端口
ssr_port=6665 



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
		# if not ssr['select']:
		#     result['state']="pass"
		#     return result
		# print("----------------------------")
		print(ssr['remarks']+"/"+ssr['server'])
		if test_option['ping']:
			ret=subprocess.Popen("ping -n 3 %s" % result['host'], shell=True, stdout=subprocess.PIPE) 
			out=ret.stdout.readlines()
			pattern=re.compile(r'\d+')
			# pattern=re.compile(r'= .?ms')
			ping_pc=pattern.findall(out[-1].decode('gbk'))
			print("ping_test,localPing:",ping_pc[-1])
			result['ping_pc']=ping_pc[-1]

		socks.set_default_proxy(socks.SOCKS5, "127.0.0.1", 6665)
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

		result['state']="Success"
		return result

	except Exception as e:
		print (e)
		return result


# 将订阅的数据写入到配置文件中
def write_json(write_config):
	# 打开ssr config json
	json_path="win/gui-config.json"
	json_config=None
	with open(json_path,'r',encoding='utf-8') as f:
		json_config=json.load(f)
	# 清空configs列表
	json_config['configs']=[]
	json_config['configs'].append(write_config)
	if 'protoparam' in json_config['configs'][0]:
		json_config['configs'][0]['protocolparam']=json_config['configs'][0]['protoparam']
	if 'port' in json_config['configs'][0]:
		json_config['configs'][0]['server_port']=json_config['configs'][0]['port']
	# ssr_port=json_config['configs'][0]['port']
	# 将订阅的数据写入的配置文件
	with open(json_path,'w',encoding='utf-8') as f:
		json.dump(json_config,f,indent=4)

#subprocess.call('taskkill /f /im ShadowsocksR-dotnet4.0-speedtest.exe',stdout=subprocess.PIPE)
#subprocess.Popen("ShadowsocksR-dotnet4.0.exe")

# 运行 ssr
def run_ssr():
	ssr_path="win/ShadowsocksR-dotnet4.0-speedtest.exe"
	subprocess.Popen(ssr_path)
# 关闭ssr
def close_ssr():
	subprocess.call('taskkill /f /im ShadowsocksR-dotnet4.0-speedtest.exe',stdout=subprocess.PIPE)


ssr_config=[]
speed_result=[]

if len(argv)>1:
	print(argv[1])
	# file_path="win/gui-config.json"
	file_path=argv[1]
	file_config=None
	with open(file_path,'r',encoding='utf-8') as f:
		file_config=json.load(f)
	# print(file_config['configs'])
	for x in file_config['configs']:
		ssr_config.append(x)
		# print(x)
		# print(x)
else:
	url=input("url:")
	headers = {'User-Agent':'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0'}
	f=urllib.request.Request(url,headers=headers)
	ssr_subscribe = urllib.request.urlopen(f).read().decode('utf-8') #获取ssr订阅链接中数据
	ssr_subscribe_decode = ParseSsr.base64_decode(ssr_subscribe)
	ssr_subscribe_decode=ssr_subscribe_decode.replace('\r','')
	ssr_subscribe_decode=ssr_subscribe_decode.split('\n')
	for i in ssr_subscribe_decode:
		if(i):
			decdata=str(i[6:])#去掉"SSR://"K
			ssr_config.append(ParseSsr.parse(decdata))#解析"SSR://" 后边的base64的配置信息返回一个字典
table=DrawTable()
for x in ssr_config:
	# print(x)
	run_ssr()
	write_json(x)
	speed_result=connect_ssr(x)
	os.system('cls')
	table.append(
		name=speed_result['remarks'],
		ip=speed_result['ip'],
		localPing=speed_result['ping_pc'],
		ping=speed_result['ping'],
		upload=speed_result['upload'],
		download=speed_result['download'],
		# youtube=speed_result['youtube'],
		network=speed_result['state']
	)
	print(table.str())
	close_ssr()
