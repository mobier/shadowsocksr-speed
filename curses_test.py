import urllib.request
import requests
import ParseSsr #https://www.jianshu.com/p/81b1632bea7f
from prettytable import PrettyTable
from colorama import init, Fore, Back, Style

import time
import curses
import sys
import os

test_option={}
test_option ['ping']=test_option ['network']=test_option ['speed']= test_option ['youtube']=False

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
color=colored()

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
				# break

# test_ssr=[]
def drawtable(screen):
	# print(max_line)
	# while True:
	# 	pass
	select_table=DrawSelectTable()
	ssr_config=getss()
	for x in ssr_config:
		x['select']=1
		select_table.append(select=x['select'],name=x['remarks'])
	# print(table)
	help_string1 = 'W(up) S(down) A(left) D(right)'
	help_string2 = '      R(restart) Q(exit)'
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
	# 	pass
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
			# spad = curses.newpad(1, 2)
			# spad.scrollok(1)
			# spad.idlok(1)
			# spad.addstr(str(">"))
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
			# # 	twin.addstr(0,2,str(x))
			# # 	twin.scroll(1)
			# twin.addstr(select_table.str())
			# # twin.scroll(20)
			# twin.refresh()
			# twin.refresh(0,0,0,4,3,80)	
			# twin.getch()

			# mypadn = curses.newpad(30,4,10,0)
			# mypadn.scrollok(1)
			# mypadn.idlok(1)
			# for x in range(1,10):
			# 	mypadn.addstr(10,1, str(x))
			# 	mypadn.scroll(1)
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

def getss():
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
	return ssr_config


if __name__ == "__main__":
	term_lines = os.get_terminal_size().lines
	term_col = os.get_terminal_size().columns
	sss=curses.wrapper(drawtable)
	curses.wrapper(TestOption)
	print(test_option['ping'],test_option['network'],test_option['speed'],test_option['youtube'])

	# from pprint import pprint
	# pprint((sss))
	
	# print("asdas")
	# table=PrettyTable(["name","select"])
	# ssr_config=getss()
	# for x in ssr_config:
	# 	table.add_row([x['remarks'],"X"])
	# print(table)
	# print(ssr_config[''])
