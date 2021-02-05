# -*- coding: utf-8 -*- 
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
#import urllib.request
import requests
#beautiful soup
from bs4 import BeautifulSoup
from urllib.request import urlopen

driver1 = webdriver.Chrome()
driver1.get('https://kr.ufc.com/athletes/all')
time.sleep(2)
fe_athle=driver1.find_element_by_xpath('/html/body/div[1]/div/main/div[1]/div/div/div/div/div/div/div/div/div[2]/div/div/form/div/div[1]/div/div[2]')
fe_athle.click()
time.sleep(3)
 
SCROLL_PAUSE_TIME = 3
# Get scroll height
last_height = driver1.execute_script("return document.body.scrollHeight")

while True:
	# Scroll down to bottom
	driver1.execute_script("window.scrollTo(0, document.body.scrollHeight);")
	# Wait to load page
	time.sleep(SCROLL_PAUSE_TIME)
	# Calculate new scroll height and compare with last scroll height
	new_height = driver1.execute_script("return document.body.scrollHeight")
	if new_height == last_height:
		try:
			more_athle=driver1.find_element_by_xpath('/html/body/div[1]/div/main/div[1]/div/div/div/div/div/div/div/div/div[2]/div/div/div/ul/li/a')
			more_athle.click()
		except:
			break
	last_height =new_height

html=driver1.page_source 
soup=BeautifulSoup(html,'lxml')  
#soup = BeautifulSoup(html, 'html.parser') 
athlete_num = 1 #for counting athlete print 
for anchor in soup.select("div.c-listing-athlete-flipcard__text__back span.c-listing-athlete__name"):
	print(str(athlete_num) + ": " + anchor.get_text())
	athlete_num+=1
	driver = webdriver.Chrome()

	driver.get("https://www.google.co.kr/imghp?hl=ko&tab=wi&ogbl")
	elem=driver.find_element_by_name("q")
	elem.send_keys(anchor.get_text())
	
	
	time.sleep(3)

	athele_data=driver.find_element_by_css_selector(".JSAgYe").get_attribute("value")
	images=driver.find_elements_by_css_selector(".rg_i.Q4LuWd")
	pic_count=1		#count download img
	for image in images: 
		try:
			image.click()
			time.sleep(2)
			imgUrl=driver.find_element_by_xpath('/html/body/div[2]/c-wiz/div[3]/div[2]/div[3]/div/div/div[3]/div[2]/c-wiz/div[1]/div[1]/div/div[2]/a/img').get_attribute("src")
			cookies = dict(BCPermissionLevel='PERSONAL')
	
			with open(athele_data+str(pic_count)+'.jpg', 'wb') as handle:
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
	driver.close()

