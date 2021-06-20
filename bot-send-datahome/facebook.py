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
	return str(detail.replace('"',"").replace("'",""))



def getlink(data):
	a = data.find("a")
	herf = str(a.attrs.get('href'))
	link = herf.find("/?ref=category")
	new = herf[0:link]
	return "https://www.facebook.com" + str(new)
def redata(data):
	jsonobj = {"detail":getdetail(data),"price":getprice(data),"address":getaddress(data),"link":getlink(data)}
	return json.dumps(jsonobj)

def getdata():
	print("Facebook Get Web")
	start = time.time()
	chrome_options = webdriver.ChromeOptions()
	chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
	chrome_options.add_argument("--incognito")
	chrome_options.add_argument("--headless")
	chrome_options.add_argument("--no-sandbox")
	driver = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), chrome_options=chrome_options)
	driver.get("https://www.facebook.com/marketplace/114630248548655/propertyforsale")
	time.sleep(2)
	soup = BeautifulSoup(driver.page_source,"lxml")
	driver.quit()
	find_word = soup.find_all("div",{"class":"kbiprv82"})
	data_new = []
	for i in find_word:
		data_new.append(redata(i))
	facebook = []
	for i in DBtools.savedata(data_new,tablename):
		facebook.append(i)
	stop = time.time()
	t = stop-start
	print(tablename+" Time : "+str(t))
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
def boxtemp(detail,price,address,link):
	box = {"type": "box","layout": "vertical","contents":
					  [
						  {"type": "text","text": str(detail),"wrap": True,"align": "start","contents": []},
						  {"type": "text","text": str(price)+" บาท","wrap": True,"contents": []},
						  {"type": "text","text": str(address),"wrap": True,"contents": []},
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
			addbox = boxtemp(str(row["detail"]),str(row["price"]),str(row["address"]),str(row["link"]))
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
				addbox = boxtemp(str(row["detail"]),str(row["price"]),str(row["address"]),str(row["link"]))
				bubbleset["body"]["contents"].append(addbox)
			else:
				carousel["contents"].append(bubbleset)
				bubbleset = bubbletemp(msg)
				num = 0
				addbox = boxtemp(str(row["detail"]),str(row["price"]),str(row["address"]),str(row["link"]))
				bubbleset["body"]["contents"].append(addbox)
				num += 1
		carousel["contents"].append(bubbleset)
		return json.dumps(carousel)