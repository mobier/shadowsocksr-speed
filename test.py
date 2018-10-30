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
default_socket = socket.socket
socks.set_default_proxy(socks.SOCKS5, "127.0.0.1", 1080)
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