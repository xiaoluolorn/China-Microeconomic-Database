from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
url = 'http://microdata.sozdata.com/login.html'
driver = webdriver.Chrome('C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe')
driver.implicitly_wait(5)
driver.get(url)
driver.find_element_by_xpath('//*[@id="login_form"]/div[5]/button[2]').click() # IP登陆
driver.find_element_by_xpath('//*[@id="app"]/div[2]/div/ul/li[5]').click() # 选择跨库匹配
driver.find_element_by_xpath('//*[@id="app"]/div[3]/div[1]/div/div[1]/div[2]/div[3]').click() # 选择工企和创新
driver.find_element_by_xpath('//*[@id="app"]/div[3]/div[1]/div/div[3]/div/div[2]/div[2]/p').click() # 去掉海关
driver.find_element_by_xpath('//*[@id="app"]/div[3]/div[1]/div/div[3]/div/div[2]/div[4]').click() # 添加创新
driver.find_element_by_xpath('//*[@id="app"]/div[3]/div[1]/div/div[3]/div/div[3]/button').click() # 确定
for ele in range(12,15):
	txt='//*[@id="app"]/div[3]/div[1]/div/div[2]/div/div[1]/div[1]/div[2]/div[1]/div[1]/div[2]/div[2]/div[{m}]' .format(m = ele)
	click = driver.find_element_by_xpath('//*[@id="app"]/div[3]/div[1]/div/div[2]/div/div[1]/div[1]/div[2]/div[1]/div[1]/div[2]')
	click.click()  # 选择年份
	driver.find_element_by_xpath(txt).click()
	driver.find_element_by_xpath('//*[@id="app"]/div[3]/div[1]/div/div[2]/div/div[1]/div[7]/button').click()  # 查询
	sleep(2)
	download = driver.find_element_by_xpath('//*[@id="app"]/div[3]/div[1]/div/div[2]/div/div[3]/div/button[2]')
	nextpage = driver.find_element_by_xpath('//*[@id="page"]/div/ul/li[last()]')
	pages = int(driver.find_element_by_xpath('//*[@id="page"]/div/ul/li[@class][6]').text)
	download.click()  # 下载
	currentpage = 1
	while pages - currentpage > 0:
		try:
			nextpage.click()  # 下一页
			try:
				WebDriverWait(driver, 10).until(
					EC.element_to_be_clickable([By.XPATH, '//*[@id="app"]/div[3]/div[1]/div/div[2]/div/div[3]/div/button[2]'])
				)
			finally:
				driver.quit()
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
