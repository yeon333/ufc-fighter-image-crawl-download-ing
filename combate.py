# -*- coding: utf-8 -*- 
from selenium import webdriver  #pip install selenium
from selenium.webdriver.common.keys import Keys
import time
#import urllib.request
import requests  # pip install requests
#beautiful soup
from bs4 import BeautifulSoup
from urllib.request import urlopen

#import subprocess

driver = webdriver.Chrome()
driver.get('https://kr.ufc.com/athletes/all')
time.sleep(2)
fe_athle=driver.find_element_by_xpath('/html/body/div[1]/div/main/div[1]/div/div/div/div/div/div/div/div/div[2]/div/div/form/div/div[1]/div/div[2]')
fe_athle.click()
time.sleep(3)
 
SCROLL_PAUSE_TIME = 3.5
# Get scroll height
last_height = driver.execute_script("return document.body.scrollHeight")
while True:
	# Scroll down to bottom
	driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
	# Wait to load page
	time.sleep(SCROLL_PAUSE_TIME)
	# Calculate new scroll height and compare with last scroll height
	new_height = driver.execute_script("return document.body.scrollHeight")
	if new_height == last_height:
		try:
			more_athle=driver.find_element_by_xpath('/html/body/div[1]/div/main/div[1]/div/div/div/div/div/div/div/div/div[2]/div/div/div/ul/li/a')
			more_athle.click()
		except:
			break
	last_height =new_height
html=driver.page_source 
soup=BeautifulSoup(html,'lxml')   #pip install lxml.

athlete_num = 1 #for counting athlete print 
c_mem=10
driver.get("https://www.google.co.kr/imghp?hl=ko&tab=wi&ogbl")



for anchor in soup.select("div.c-listing-athlete-flipcard__text__back span.c-listing-athlete__name"): #bring soup data and download 50ish img
	if athlete_num>c_mem:
		driver.quit()
		#subprocess.call("TASKKILL /f  /IM  C:/sel/selenium/chromedriver.exe")  
		print( "%s memory resting" %(str(c_mem)) )
		time.sleep(10)
		driver = webdriver.Chrome()
		driver.get("https://www.google.co.kr/imghp?hl=ko&tab=wi&ogbl")
		c_mem+=10
	
	print(  "%s: %s"  %(str(athlete_num) ,anchor.get_text()) )
	athlete_num+=1
	elem=driver.find_element_by_name("q")
	driver.find_element_by_tag_name('body').send_keys(Keys.CONTROL + Keys.HOME) #scroll up 
	elem.clear()
	time.sleep(2)
	elem.send_keys(anchor.get_text())
	time.sleep(3)
	athele_data=driver.find_element_by_css_selector(".JSAgYe").get_attribute("value") #athlete name
	images=driver.find_elements_by_css_selector(".rg_i.Q4LuWd")
	pic_count=1		#count download img
	for image in images: 
		try:
			image.click()
			time.sleep(2)
			imgUrl=driver.find_element_by_xpath('/html/body/div[2]/c-wiz/div[3]/div[2]/div[3]/div/div/div[3]/div[2]/c-wiz/div/div[1]/div[1]/div/div[2]/a/img').get_attribute("src")
			cookies = dict(BCPermissionLevel='PERSONAL')
	
			with open(  '%s %s .jpg' %(athele_data, str(pic_count)), 'wb') as handle:
				response = requests.get(imgUrl, headers={"User-Agent": "Mozilla/5.0"}, cookies=cookies,stream=True)
				if not response.ok:
					print (response)

				for block in response.iter_content(1024):
					if not block:
						break
				handle.write(block)
			pic_count+=1
		except:
			pass    

print("misson complete!!")
driver.quit()
	#subprocess.call("TASKKILL /f  /IM  CHROMEDRIVER.EXE") 



