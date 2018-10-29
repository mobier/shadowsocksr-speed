# SSR 批量测速

通过SSR的订阅链接解析，从大量的节点中判断存活并根据下载带宽进行排序生产表格，可从中选出最适合的节点  
目前调用的是speedtest的测速接口，后期会加入youtube，以及自定义服务器的测试功能  
使用独立端口进行测速，不会影响正常浏览体验，建议非游戏用户以下载带宽优先  
目前支持sspanel/v2/v3版本，443/常规订阅链接
测试速度的话单个节点，ping和模拟请求需要5S，带宽测试~22S，Youtube~20s

## 同类型的工具

SSR的windows版本中有“服务器链接统计”功能。能检测出有效节点和最高带宽。但是在实际环境中并不能很好的测试到准确的带宽大小，并且在测速中会影响正常的浏览，SSTap中也仅仅只有延迟测试，并且两个工具都只能在win的环境中使用。而我只有极少数的情况下会使用win就比较尴尬了

## 使用

```
$ sudo apt-get install xvfb
$ https://chromedriver.storage.googleapis.com   //!!!!! 根据浏览器版本下载chromedriver
$ sudo cp chromedriver /usr/bin/
$ pip3 install PySocks prettytable pyvirtualdisplay selenium
$ sudo python3 shadowsocksr-speed.py
url: //输入入SSR订阅链接
```

![](https://file-temp.oss-cn-beijing.aliyuncs.com/201810280012.png)
