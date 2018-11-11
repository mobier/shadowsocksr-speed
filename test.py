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

import youtube_speed

import socket
import socks
import time
import subprocess
import signal
# import shlex 

default_socket = socket.socket
socks.set_default_proxy(socks.SOCKS5, "127.0.0.1", 1080)
# cmd ="python /home/null/.config/electron-ssr/shadowsocksr/shadowsocks/local.py -s kr2.pyjiaoyi.cf -p 10384 -k EoWjVthG -m chacha20-ietf -O auth_aes128_md5 -o http_simple -g download.windowsupdate.com -b 127.0.0.1 -l 1088"
# # cmd = shlex(cmd)
# ss_s = subprocess.Popen(cmd, shell=True)
# # os.system(cmd)
# # p=os.popen(cmd)
# print("sadsd")
# print(a.pid)
# time.sleep(5)

# # os.killpg(os.getpgid(a.pid+1), 9) 
# os.kill(a.pid, signal.SIGKILL)
# os.kill(a.pid+1	, signal.SIGKILL)
# # a.send_signal(signal.CTRL_C_EVENT)
# # a.terminate()
# print("close")

# while True:
# 	print("asdsad")
# socket.socket = socks.socksocket
# socket.socket='socket.socket'
# print(default_socket)
# print(type('socket.socket'))
# # import socket
# import socks
# default_socket = socket.socket
# socket.socket=default_socket

# socket.shut_rdwr()
# help(socket)

youtube_speed.test_speed("1080")