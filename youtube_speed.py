# form https://blog.yasking.org/a/you2be-connection-speed.html
# https://github.com/peter6888/tf_tv/blob/31a11d81976786ec172509aba8e28d501652bf19/youtube.py
import time 
from pyvirtualdisplay import Display
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains

from selenium.webdriver.support.ui import WebDriverWait                            # available since 2.4.0
from selenium.webdriver.support import expected_conditions as EC           # available since 2.26.0
from selenium.webdriver.common.by import By

from selenium.common.exceptions import TimeoutException

Deubg=False 

def isAD(drive):
    try:
        if(drive.find_element_by_xpath('//div[text() = "跳过广告"]').get_attribute('innerHTML')=="跳过广告"):
        	return True
        else:
        	return False
    except:
        return False
def isVIP(drive):
    try:
        if(drive.find_element_by_xpath('//*[text() = "不用了"]').get_attribute('innerHTML')=="不用了"):
            return True
        else:
            return False
    except:
        return False
def ifButton(drive):
    try:
        if(drive.find_element_by_xpath('//div[text() = "画质"]').get_attribute('innerHTML')=="画质"):
            return True
        else:
            return False
    except:
        return False
def ifFlash(drive):
    try:
        drive.find_element_by_id('movie_player')
        return True
    except:
        return False
def yt_check(drive):
    try:
        if(isVIP(drive)):
            if Deubg : print("yt_check")
            return True
        else:
            return False
    except:
        if Deubg : print("not found flash")
        return False


def test_speed(proxy_port,out_time=15):
    try:
        chromeOptions = webdriver.ChromeOptions()
        # 设置后台运行
        display = Display(visible=0, size=(800, 600))
        display.start()

        # 设置代理
        # chromeOptions.add_argument("--proxy-server=socks5://127.0.0.1:1080")
        chromeOptions.add_argument("--proxy-server=socks5://127.0.0.1:%s" % proxy_port)
        chromeOptions.add_argument("--mute-audio")
        chromeOptions.add_argument("--no-sandbox")
        chromeOptions.add_argument('lang=zh_CN.UTF-8')
        browser = webdriver.Chrome(chrome_options = chromeOptions)
        # 设置才超时时间
        # browser.implicitly_wait(1)
        # browser.manage().timeouts().pageLoadTimeout(2, TimeUnit.SECONDS);
        # browser.manage().timeouts().pageLoadTimeout(10,TimeUnit.SECONDS);
        browser.set_page_load_timeout(out_time)
        browser.set_script_timeout(out_time)#这两种设置都进行才有效
        # 访问视频
        browser.get('https://www.youtube.com/watch?v=TmDKbUrSYxQ')
        time.sleep(2)


        #判断是否有广告
        if isAD(browser):

            if Deubg : print("youtube_ad")
            time.sleep(6)
            # WebDriverWait(browser, 20).until(EC.presence_of_element_located((By.xpath,'//div[text() = "跳过广告"]')))
            browser.find_element_by_xpath('//div[text() = "跳过广告"]').click()
            time.sleep(1)
        #判断是否有youtube 推荐会员
        if isVIP(browser):
            if Deubg : print("youtube_vip")
            # time.sleep(1)
            # browser.find_element_by_xpath('//*[text() = "不用了"]').click()
            # time.sleep(1)
        if Deubg : print("check_end")
        # 点击右键，显示速度信息
        browser.implicitly_wait(30)
        ifFlash(browser);
        ele = browser.find_element_by_id('movie_player')
        action_chains = ActionChains(browser)
        action_chains.move_to_element_with_offset(ele, 50, 50).context_click().perform()
        time.sleep(1)
        browser.find_element_by_xpath('//div[text() = "详细统计信息"]').click()
        time.sleep(1)

        # 设置4K画质
        # video_set=browser.find_element_by_class_name("ytp-right-controls")
        # video_set.find_elements_by_xpath('.//button')[1].click()
        # set_button = browser.find_element_by_xpath('//div[@class = "ytp-chrome-controls"]')
        # move_chains = ActionChains(browser)
        # move_chains.move_to_element_with_offset(set_button, 0, 10).perform()
        # time.sleep(0.5)
        # move_chains.move_to_element_with_offset(set_button, 487, 10).click().perform()
        # time.sleep(1.5)
        # move_chains.move_to_element_with_offset(set_button, 487, -100).click().perform()

        browser.find_element_by_xpath('//button[@title = "设置"]').click()
        time.sleep(0.5)
        if not ifButton:
            if Deubg : print("ifButton")
        browser.find_element_by_xpath('//div[text() = "画质"]').click()
        time.sleep(1)
        browser.find_element_by_xpath('//span[text() = "2160p"]').click()
        time.sleep(5)



        # if Deubg : print(browser.find_element_by_xpath('//*[@id="movie_player"]'))
        # if Deubg : print(browser.find_element_by_css_selector(".html5-video-info-panel-content"))
        # if Deubg : print(browser.find_element_by_css_selector(".html5-video-info-panel-content > div:nth-child(0)"))
        # 获取速度
        infopanel = browser.find_element_by_class_name("html5-video-info-panel-content")
        youtube_speed=infopanel.find_elements_by_xpath('.//span')[10].get_attribute('innerHTML')
        if Deubg : print(youtube_speed)
        # if Deubg : print("-----------------------------------")

        # if Deubg : print(video_set.find_elements_by_xpath('.//button')[1].get_attribute('innerHTML'))

        # data=browser.find_element_by_xpath('//*[@id="movie_player"]/div[2]/div/div[7]/span/span[2]')
        # data=browser.find_element_by_xpath('//*[@id="movie_player"]/div[2]/div/div[10]/span/span[2]')
        # if Deubg : print(data)
        # if Deubg : print(browser.page_source)
        # 退出浏览器
        browser.quit()
        display.stop()
        return youtube_speed
    except TimeoutException:
        # print("youtube_timeout")
        browser.quit()
        display.stop()
        return "1"
    except Exception as e:
        print(e)
        browser.quit()
        display.stop()
        # while(1):
        #     pass
    # except Exception as e:
    #     if Deubg : print(e)
    #     if Deubg : print("======================================")
    #     if Deubg : print(browser.page_source)
    #     if Deubg : print("======================================")
    #     browser.quit()
    #     return 0

# test_speed("1080")
