from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
url = 'http://microdata.sozdata.com/login.html'
driver = webdriver.Chrome('C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe')
driver.implicitly_wait(10)
driver.get(url)
driver.find_element_by_xpath('//*[@id="login_form"]/div[5]/button[2]').click() # IP登陆
driver.find_element_by_xpath('//*[@id="app"]/div[2]/div/ul/li[2]').click() # 选择海关数据
for ele in range(2,18):
	txt='//*[@id="app"]/div[3]/div[1]/div/div[1]/ul/li[{m}]' .format(m = ele)
	driver.find_element_by_xpath(txt).click()  # 选择年份
	driver.find_element_by_xpath('//*[@id="app"]/div[3]/div[1]/div/div[2]/div/div[1]/div/div[3]/div[4]/div[2]').click() #选择贸易流向
	driver.find_element_by_xpath('//*[@id="app"]/div[3]/div[1]/div/div[2]/div/div[1]/div/div[3]/div[4]/div[2]/div[2]/div[3]').click()  # 选择进口
	driver.find_element_by_xpath('//*[@id="app"]/div[3]/div[1]/div/div[2]/div/div[3]/button').click()  # 查询
	sleep(5)
	download = driver.find_element_by_xpath('//*[@id="app"]/div[3]/div[1]/div/div[2]/div/div[3]/div/button[2]')
	nextpage = driver.find_element_by_xpath('//*[@id="page"]/div/ul/li[last()]')
	pages = int(driver.find_element_by_xpath('//*[@id="page"]/div/ul/li[@class][6]').text)
	sleep(5)
	download.click()  # 下载
	currentpage = 1
	while pages - currentpage > 0:
		try:
			nextpage.click()  # 下一页
			try:
				element = WebDriverWait(driver, 10).until(
					EC.presence_of_element_located((By.ID, "app"))
				)
			except:
				continue
			currentpage = int(driver.find_element_by_xpath('//li[@class = "ivu-page-item ivu-page-item-active"][1]').text)
			download.click()  # 下载
		except:
			continue
	driver.back()
	try:
		element = WebDriverWait(driver, 10).until(
			EC.presence_of_element_located((By.ID, "app"))
		)
	except:
		continue
