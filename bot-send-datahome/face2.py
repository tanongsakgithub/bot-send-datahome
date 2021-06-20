from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
import requests
import re
import time
import json
import lxml
import random
import os
import DBtools
import ast
from bs4 import BeautifulSoup
tablename = "facebook"
def getprice(data):
	price = data.find("div",{"class":"a8nywdso e5nlhep0 rz4wbd8a ecm0bbzt btwxx1t3 j83agx80"}).get_text()
	return str(price)
def getaddress(data):
	address = data.find("span",{"class":"a8c37x1j ni8dbmo4 stjgntxs l9j0dhe7 ltmttdrg g0qnabr5"}).get_text()
	return str(address)
def getdetail(data):
	detail = data.find("span",{"class":"a8c37x1j ni8dbmo4 stjgntxs l9j0dhe7"}).get_text()
	return str(detail)
def getimg(data):
	img = data.find("img",{"class":"idiwt2bm bixrwtb6 ni8dbmo4 stjgntxs k4urcfbm"})
	return str(img.attrs.get('src'))
def getlink(data):
	a = data.find("a")
	herf = str(a.attrs.get('href'))
	link = herf.find("/?ref=category")
	new = herf[0:link]
	return "https://www.facebook.com" + str(new)
def redata(data):
	jsonobj = {"detail":getdetail(data),"price":getprice(data),"address":getaddress(data),"link":getlink(data),"img":getimg(data)}
	return json.dumps(jsonobj)

def getabout(data):
	try:
		about = data.find("span",{"class":"d2edcug0 hpfvmrgz qv66sw1b c1et5uql lr9zc1uh a8c37x1j keod5gw0 nxhoafnm aigsh9s9 d3f4x2em fe6kdd0r mau55g9w c8b282yb iv3no6db jq4qci2q a3bd9o3v knj5qynh oo9gr5id"}).get_text().replace("ดูน้อยลง","").replace("\n\n","")
	except:
		about = "-"
	return str(about)

def getweb(data):
	row = ast.literal_eval(data)
	url = str(row["link"])
	print(url)
	chrome_options = webdriver.ChromeOptions()
	chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
	chrome_options.add_argument("--window-size=1920,1200")
	chrome_options.add_argument("--incognito")
	chrome_options.add_argument("--headless")
	#chrome_options.add_argument("--disable-dev-shm-usage")
	chrome_options.add_argument("--no-sandbox")
	driver = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), chrome_options=chrome_options)


	#options = Options()
	#options.headless = False
	#options.add_argument("--window-size=1920,1200")
	#options.add_argument("--incognito")
	#DRIVER_PATH = "C:\Program Files (x86)\chromedriver.exe"
	#driver = webdriver.Chrome(options=options, executable_path=DRIVER_PATH)
	driver.get(url)
	time.sleep(5)
	try:
		elem = driver.find_element_by_xpath('//span[@class="d2edcug0 hpfvmrgz qv66sw1b c1et5uql lr9zc1uh jq4qci2q a3bd9o3v lrazzd5p oo9gr5id"]').click()
	except:
		print("Not click")
	time.sleep(1)
	soup = BeautifulSoup(driver.page_source,"lxml")
	driver.quit()
	find_word = soup.find("div",{"class":"dati1w0a qt6c0cv9 hv4rvrfc jb3vyjys"})
	print(find_word)
	about = getabout(find_word)
	return about

def getbypage(data):
	result = []
	rowid = []
	if(len(data) <= 2):
		for loop in range(0,len(data)):
			print("Get by page "+str(loop+1))	
			about = getweb(data[loop][1])
			rowid.append(data[loop][0])
			line = ast.literal_eval(data[loop][1])
			new = {"detail":line["detail"],"price":line["price"],"address":line["address"],"about":about,"link":line["link"]}
			result.append(json.dumps(new))
	else:
		for loop in range(0,2):
			print("Get by page "+str(loop+1))	
			about = getweb(data[loop][1])
			rowid.append(data[loop][0])
			line = ast.literal_eval(data[loop][1])
			new = {"detail":line["detail"],"price":line["price"],"address":line["address"],"about":about,"link":line["link"]}
			result.append(json.dumps(new))
	DBtools.update_status(tablename,rowid)
	return result

def getdata():
	print("Facebook Get Web")
	start = time.time()
	
	chrome_options = webdriver.ChromeOptions()
	chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
	chrome_options.add_argument("--incognito")
	chrome_options.add_argument("--headless")
	#chrome_options.add_argument("--disable-dev-shm-usage")
	chrome_options.add_argument("--no-sandbox")
	driver = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), chrome_options=chrome_options)

	#options = Options()
	#options.headless = True
	#options.add_argument("--window-size=1920,1200")
	#options.add_argument("--incognito")
	#DRIVER_PATH = "C:\Program Files (x86)\chromedriver.exe"
	#driver = webdriver.Chrome(options=options, executable_path=DRIVER_PATH)
	#body = driver.find_element_by_css_selector('body')
	#body.send_keys(Keys.END)
	#time.sleep(0.5)
	#body.send_keys(Keys.END)
	#time.sleep(0.5)

	driver.get("https://www.facebook.com/marketplace/114630248548655/propertyforsale")
	time.sleep(2)
	soup = BeautifulSoup(driver.page_source,"lxml")
	driver.quit()
	find_word = soup.find_all("div",{"class":"kbiprv82"})
	data_new = []
	for i in find_word:
		data_new.append(redata(i))
	facebook = []
	for i in DBtools.savedata_havestatus(data_new,tablename):
		facebook.append(i)
	stop = time.time()
	t = stop-start
	print(tablename+" Time : "+str(t))
	return facebook

def getdata2():
	#datawait = DBtools.getdata_havestatus(tablename)
	#data_sent = []
	facebook = getbypage(DBtools.getdata_havestatus(tablename))
	print(facebook)
	return facebook

def bubbletemp(msg):
	bubble = {
  "type": "bubble",
  "size": "kilo",
  "direction": "ltr",
  "header": {
	"type": "box",
	"layout": "vertical",
	"backgroundColor": "#0095E9FF",
	"contents": [
	  {"type": "text","text": str(msg),"color": "#FFFFFFFF","align": "start","contents": []}
	]
  },
  "body": {
	"type": "box",
	"layout": "vertical",
	"contents": [
	  
	]
  }
}
	return bubble
def boxtemp(detail,about,price,address,link):
	box = {"type": "box","layout": "vertical","contents":
					  [
						  {"type": "text","text": str(detail),"align": "start","contents": []},
						  {"type": "text","text": str(about),"contents": []},
						  {"type": "text","text": str(price),"contents": []},
						  {"type": "text","text": str(address),"contents": []},
						  {"type": "button","action": {"type": "uri","label": "เพิ่มเติม","uri": str(link)}}
					 ]}
	return box

def flexobj(data,msg):
	carousel = {"type": "carousel","contents": []}
	bubble = {"type": "bubble","size": "kilo","direction": "ltr","header": {
	"type": "box","layout": "vertical","backgroundColor": "#0095E9FF","contents": [
	  {"type": "text","text": str(msg),"color": "#FFFFFFFF","align": "start","contents": []}
	]
  },
  "body": {"type": "box","layout": "vertical","contents": [
	  
	]
  }
}
	lendata = len(data)
	if(lendata <= 10):		
		for row in data:
			rowline = ast.literal_eval(row)
			addbox = boxtemp(str(rowline["detail"]),str(rowline["about"]),str(rowline["price"]),str(rowline["address"]),str(rowline["link"]))
			bubble["body"]["contents"].append(addbox)
		return json.dumps(bubble)
	else:
		num = 0
		bubbleset = bubbletemp(msg)
		rowperbubble = 0
		if(lendata <= 60):
			rowperbubble = 5
		else:
			rowperbubble = 10
		for row in data:
			num += 1
			if(num <= rowperbubble):
				rowline = ast.literal_eval(row)
				addbox = boxtemp(str(rowline["detail"]),str(rowline["about"]),str(rowline["price"]),str(rowline["address"]),str(rowline["link"]))
				bubble["body"]["contents"].append(addbox)
			else:
				carousel["contents"].append(bubbleset)
				bubbleset = bubbletemp(msg)
				num = 0
				rowline = ast.literal_eval(row)
				addbox = boxtemp(str(rowline["detail"]),str(rowline["about"]),str(rowline["price"]),str(rowline["address"]),str(rowline["link"]))
				bubble["body"]["contents"].append(addbox)
				num += 1
		carousel["contents"].append(bubbleset)
		return json.dumps(carousel)
