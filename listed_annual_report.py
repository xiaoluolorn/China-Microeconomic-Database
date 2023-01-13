# -*- coding: utf-8 -*-
# @Time    : 2023/01/12
# @Author  : Chaoyang Luo


# 导入必要的包
import pandas as pd
import json
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver import ChromeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.service import Service
import time

# 获取所有A股上市公司名录
json_url = 'http://www.cninfo.com.cn/new/data/szse_stock.json'
df = pd.read_json(json_url, encoding='utf-8')
df = df['stockList'].apply(pd.Series)
df = df[df['category']=='A股']
list_comp = df['zwjc'].tolist()


path = Service(r'C:\Program Files\Google\chromedriver.exe')  # chromedriver.exe 文件路径

# 目标网页：巨潮资讯网
Url = 'http://www.cninfo.com.cn/new/index'


class Crawler(object):
    # 初始化浏览器配置
    def __init__(self, url, name, start_date, end_date):
        option = ChromeOptions()
        # 反屏蔽
        option.add_experimental_option('excludeSwitches', ['enable-automation'])
        option.add_experimental_option('useAutomationExtension', False)
        option.binary_location = 'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe'
        option.add_argument('--ignore-certificate-errors')
        option.add_argument('--ignore-ssl-errors')
        # 修改下载地址
        option.add_experimental_option("prefs",
                                       {"download.default_directory": "E:\\Annual_Report"})
        self.browser = webdriver.Chrome(options=option,executable_path='C:\\Program Files\\Google\\chromedriver.exe') # chromedriver.exe 文件路径
        self.browser.execute_cdp_cmd('Page.addScriptToEvaluateOnNewDocument',
                                     {'source': 'Object.defineProperty(navigator, "webdriver", {get: () => undefined})'})
        # 隐式等待，直到网页加载完毕，最长等待时间为20s
        self.browser.implicitly_wait(20)

        # 目标网页：url
        self.url = url
        # 目标银行名称
        self.name = name
        # 起止日期
        self.start_date, self.end_date = start_date, end_date

    # 提交查询命令
    def search(self):
        # 填写“企业名称”
        element = self.browser.find_element(By.XPATH,'//*[@id="searchTab"]/div[2]/div[2]/div/div[1]/div/div[1]/input')
        ActionChains(self.browser).double_click(element).perform()
        element.send_keys(self.name)
        ActionChains(self.browser).move_by_offset(0, 0).click().perform() 
        time.sleep(0.5)
        # 修改“开始日期”
        element = self.browser.find_element(By.XPATH,'//div[@class="ct-line"]/div[1]/input[@placeholder="开始日期"]')
        ActionChains(self.browser).double_click(element).perform()
        element.clear()
        element.send_keys(self.start_date)
        ActionChains(self.browser).move_by_offset(0, 0).click().perform() 
        # 修改“结束日期”
        element = self.browser.find_element(By.XPATH,'//div[@class="ct-line"]/div[1]/input[@placeholder="结束日期"]')
        ActionChains(self.browser).double_click(element).perform()
        element.clear()
        element.send_keys(self.end_date)
        ActionChains(self.browser).move_by_offset(0, 0).click().perform() 
        # 修改“分类”
        self.browser.find_element(By.XPATH,'//*[@id="searchTab"]/div[2]/div[2]/div/div[2]/span/button').click()
        self.browser.find_element(By.CSS_SELECTOR,'span[title="年报"]').click()
        # self.browser.find_element(By.CSS_SELECTOR,'span[title="三季报"]').click()
        # self.browser.find_element(By.CSS_SELECTOR,'span[title="半年报"]').click()
        # self.browser.find_element(By.CSS_SELECTOR,'span[title="一季报"]').click()
        self.browser.find_element(By.XPATH,'//div[@class="ft"]/button').click()
        # 提交“查询”
        self.browser.find_element(By.XPATH,'//*[@id="searchTab"]/div[2]/div[5]/button').click()

    # 下载每一页的pdf
    def download_pdf(self):
        # 提取当前页面所有待点击的子链接
        sublink_list = self.browser.find_elements(By.XPATH,'//span[@class="ahover"]')
        max_node_num = len([node for node in sublink_list])
        print('max_node_num: ', max_node_num)
        for node_num in range(1, max_node_num + 1):
            subpath = '//tbody/tr[{}]/td[3]/div/span/a'.format(node_num)  # 获取子链接
            sub_link = self.browser.find_element(By.XPATH,subpath)  # 点击子链接
            if sub_link.text.find('摘要')>0: # 年报摘要不下载
                continue
            elif sub_link.text.find('H股')>0: # H股年报不下载
                continue
            elif sub_link.text.find('补充')>0: # 补充年报不下载
                continue
            elif sub_link.text.find('取消')>0: # 已取消年报不下载
                continue
            elif sub_link.text.find('英文')>0: # 英文年报不下载
                continue
            else:
                self.browser.execute_script("arguments[0].click();", sub_link)
                self.browser.switch_to.window(self.browser.window_handles[-1])  # 切换到最新打开的窗口（文件下载页面）
                try:
                    self.browser.find_element(By.XPATH,
                   '//*[@id="noticeDetail"]/div/div[1]/div[3]/div[1]/button').click()  # 点击“下载”，文件保存到默认下载路径
                except:
                    print('该文件不可下载')

            time.sleep(1)  # 根据网速快慢调整，网速慢调大参数
            self.browser.close()  # 关闭当前窗口
            self.browser.switch_to.window(self.browser.window_handles[0])  # 返回起始窗口
            print('当前页面已下载到第', node_num, '条')

    # 提交查询并下载
    def search_and_download(self):
        self.browser.get(self.url)
        # 先关闭浮窗
        # self.browser.find_element_by_css_selector('span[class="close-btn"]').click()
        # 输入检索条件
        self.search()
        page = 1
        while True:
            time.sleep(0.5)
            # 翻页循环
            print('开始下载第', page, '页')
            self.download_pdf()  # 下载当前页面所有pdf文件
            try:
                a = self.browser.find_element(By.XPATH,'//button[@class="btn-next" and @disabled="disabled"]')
                print('已下载到最后一页')
                time.sleep(5)   # 根据网速调整，网速慢需要将参数调大
                break
            except:
                next_page_button = self.browser.find_element(By.XPATH,'//button[@class="btn-next"]')
                next_page_button.click()  
                page += 1
                time.sleep(1)
        self.browser.close()
        time.sleep(1)


# 一次下载不完，分多次下载
last_down = ''  #填入最一个已经下载好的上市公司名，如：平安银行

if last_down != '':
    notyet = list_comp.index(last_down) + 1
else:
    notyet = 0

length = len(list_comp) - 1
list_comp = list_comp[notyet:length]

for listing in list_comp:
    print('开始下载：', listing)
    Juchaozixun = Crawler(Url, listing, '2000-01-01', '2022-12-31')  # 后两个参数分别对应查询起止日期，可自行修改
    Juchaozixun.search_and_download()
