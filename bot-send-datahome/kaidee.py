import requests
import re
import time
import json
import DBtools
from bs4 import BeautifulSoup
def getprice(data):
	price = data.find("div",{"class":"c4fc20ba"}).get_text()
	return str(price)

def getaddress(data):
	address = data.find("div",{"class":"_7afabd84"}).get_text()
	return str(address.replace(",","-").replace(" ",""))

def gettype(data):
	type = data.find("div",{"aria-label":"Type"}).get_text()
	return str(type)

def getbeds(data):
	beds = data.find_all("span",{"aria-label":"Beds"})
	if(len(beds) == 0):
		return str("-")
	else:
		return str(beds[0].get_text())

def getbaths(data):
	baths = data.find_all("span",{"aria-label":"Baths"})
	if(len(baths) == 0):
		return str("-")
	else:
		return str(baths[0].get_text())

def getarea(data):
	area = data.find("span",{"aria-label":"Area"}).get_text()
	return str(area)
def getlink(data):
	owner = data.find("a")
	return "https://baan.kaidee.com" + str(owner.attrs.get('href'))
def redata(data):
	jsonobj = {"type":gettype(data),"price":getprice(data),"address":getaddress(data),"area":getarea(data),"beds":getbeds(data),"baths":getbaths(data),"link":getlink(data)}
	return json.dumps(jsonobj)

def getdata():
	start = time.time()
	tablename = "kaidee"
	urlnewhome = "https://baan.kaidee.com/c2p57-realestate/songkhla?sort=date_desc"
	get_newhome = requests.get(urlnewhome)
	print(get_newhome)
	soup = BeautifulSoup(get_newhome.text,'html.parser')
	find_word = soup.find_all("article",{"class":"ca2f5674"})
	data_new = []
	for i in find_word:
		data_new.append(redata(i))
	kaidee = []
	for line in DBtools.savedata(data_new,tablename):
		kaidee.append(line)
	stop = time.time()
	t = stop-start
	print(tablename+" Time : "+str(t))
	return kaidee

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
def boxtemp(type,price,area,beds,baths,address,link):
	box = {"type": "box","layout": "vertical","contents":
					  [
						  {"type": "text","text": "ประเภท " + str(type),"align": "start","contents": []},
						  {"type": "text","text": "ราคา "+str(price)+" บาท","contents": []},
						  {"type": "text","text": "พื้นที่ "+str(area),"contents": []},
						  {"type": "text","text": "ห้องนอน "+str(beds)+" ห้อง","contents": []},
						  {"type": "text","text": "ห้องน้ำ "+str(baths)+" ห้อง","contents": []},
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
			addbox = boxtemp(str(row["type"]),str(row["price"]),str(row["area"]),str(row["beds"]),str(row["baths"]),str(row["address"]),str(row["link"]))
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
				addbox = boxtemp(str(row["type"]),str(row["price"]),str(row["area"]),str(row["beds"]),str(row["baths"]),str(row["address"]),str(row["link"]))
				bubbleset["body"]["contents"].append(addbox)
			else:
				carousel["contents"].append(bubbleset)
				bubbleset = bubbletemp(msg)
				num = 0
				addbox = boxtemp(str(row["type"]),str(row["price"]),str(row["area"]),str(row["beds"]),str(row["baths"]),str(row["address"]),str(row["link"]))
				bubbleset["body"]["contents"].append(addbox)
				num += 1
		carousel["contents"].append(bubbleset)
		return json.dumps(carousel)