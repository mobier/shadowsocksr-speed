# SSR 批量测速

通过SSR的订阅链接解析，从大量的节点中判断存活并根据下载带宽进行排序生产表格，可从中选出最适合的节点  
目前调用的是speedtest的测速接口，模拟浏览器读取youtube加载视频速度，后期会加入自定义服务器的测试功能  
使用独立端口进行测速，不会影响正常浏览体验，建议非游戏用户以下载带宽优先  
目前支持sspanel/v2/v3版本，443/常规订阅链接    
测试速度的话单个节点，ping和模拟请求需要5S，带宽测试22S，Youtube 20s   

## 同类型的工具

SSR的windows版本中有“服务器链接统计”功能。能检测出有效节点和最高带宽。但是在实际环境中并不能很好的测试到准确的带宽大小，并且在测速中会影响正常的浏览，SSTap中也仅仅只有延迟测试，并且两个工具都只能在win的环境中使用。而我只有极少数的情况下会使用win就比较尴尬了

## 使用
### Linux 用户

```
$ sudo apt-get install xvfb
$ https://chromedriver.storage.googleapis.com //!!!!! 根据浏览器版本下载chromedriver
$ sudo cp chromedriver /usr/bin/
$ pip3 install PySocks prettytable pyvirtualdisplay selenium colorama
$ git clone https://github.com/mobier/shadowsocksr-speed.git
$ cd shadowsocksr-speed
$ sudo python3 shadowsocksr-speed.py
url: //输入入SSR订阅链接
```

### macOS 用户

```
$ brew cask install chromedriver //!!!!! 建议使用 Homebrew cask 安装 chromedriver
$ pip3 install PySocks prettytable pyvirtualdisplay selenium colorama
$ git clone https://github.com/mobier/shadowsocksr-speed.git
$ cd shadowsocksr-speed
$ sudo python3 shadowsocksr-speed.py
url: //输入入SSR订阅链接
选择测试节点以及测速选项
```

### 菜单选择
W(up) S(down) 上下移动光标  
A(left) D(right) 空格 选择节点/测速选项  
Q退出,R 反向选择 ,回车确认表单  

----------------------

同上面操作,可以单独测速,或者组合测速  
1 - All Test    下面选项全部测试   
2 - Ping        调用本地ping 测试延迟  
3 - Network    使用节点网络访问ip.sb判断是否可用  
4 - Speed        调用speedtest脚本测试准确上下行带宽  
5 - Youtube    模拟浏览器访问4k视频获取加载视频速度(有一定几率报错)  


![](https://file-temp.oss-cn-beijing.aliyuncs.com/2.png)
