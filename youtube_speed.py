# form https://blog.yasking.org/a/you2be-connection-speed.html
# https://github.com/peter6888/tf_tv/blob/31a11d81976786ec172509aba8e28d501652bf19/youtube.py
import time 
from pyvirtualdisplay import Display
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains


def isAD(drive):
    try:
        if(drive.find_element_by_xpath('//div[text() = "跳过广告"]').get_attribute('innerHTML')=="跳过广告"):
        	return True
        else:
        	return False
    except:
        return False

def test_speed(proxy_port):
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
        browser = webdriver.Chrome(chrome_options = chromeOptions)
        # 访问视频
        browser.get('https://www.youtube.com/watch?v=TmDKbUrSYxQ')
        time.sleep(2)
        #ads
        #div class="video-ads"
        #div videoAdUiSkipButtonExperimentalText videoAdUiFixedPaddingSkipButtonText 跳过广告
        #div videoAdUi
        # print(browser.find_element_by_xpath('//div[text() = "跳过广告"]').get_attribute('innerHTML'))

        #判断是否有广告
        if isAD(browser):
        	# print("ad")
        	time.sleep(6)
        	browser.find_element_by_xpath('//div[text() = "跳过广告"]').click()
        	time.sleep(1)

        # 设置4K画质
        # video_set=browser.find_element_by_class_name("ytp-right-controls")
        # video_set.find_elements_by_xpath('.//button')[1].click()
        browser.find_element_by_xpath('//button[@title = "设置"]').click()
        time.sleep(0.5)
        browser.find_element_by_xpath('//div[text() = "画质"]').click()
        time.sleep(0.5)
        browser.find_element_by_xpath('//span[text() = "2160p"]').click()
        time.sleep(1)

        # 点击右键，显示速度信息
        ele = browser.find_element_by_id('movie_player')
        action_chains = ActionChains(browser)
        action_chains.move_to_element_with_offset(ele, 100, 100).context_click().perform()
        time.sleep(1)
        browser.find_element_by_xpath('//div[text() = "详细统计信息"]').click()
        time.sleep(5)


        # print(browser.find_element_by_xpath('//*[@id="movie_player"]'))
        # print(browser.find_element_by_css_selector(".html5-video-info-panel-content"))
        # print(browser.find_element_by_css_selector(".html5-video-info-panel-content > div:nth-child(0)"))
        # 获取速度
        infopanel = browser.find_element_by_class_name("html5-video-info-panel-content")
        youtube_speed=infopanel.find_elements_by_xpath('.//span')[11].get_attribute('innerHTML')
        print(youtube_speed)
        # print("-----------------------------------")

        # print(video_set.find_elements_by_xpath('.//button')[1].get_attribute('innerHTML'))

        # data=browser.find_element_by_xpath('//*[@id="movie_player"]/div[2]/div/div[7]/span/span[2]')
        # data=browser.find_element_by_xpath('//*[@id="movie_player"]/div[2]/div/div[10]/span/span[2]')
        # print(data)
        # print(browser.page_source)
        # 退出浏览器
        browser.quit()
        return youtube_speed
    except Exception as e:
        print(e)
        return 0

# test_speed("1080")