import requests
import re
import time
import json
import DBtools
from bs4 import BeautifulSoup

def gettype(data):
	type = data.find("div",{"class":"small text-muted text-truncate"}).get_text().split('โครงการ · ')
	return str(type[1])
def getname(data):
	name = data.find("h3",{"class":"size-1 mb-2 text-truncate"}).get_text()
	return str(name)
def getprice(data):
	price = data.find("div",{"class":"mb-2 size-1 text-truncate f-prompt"}).get_text()
	return str(price)
def getaddress(data):
	address = data.find_all("small",{"class":"_1S48_yUNpEI4uNY2-Bq_6R text-dark"})
	return str(address[0].get_text())
def getowner(data):
	owner = data.find_all("small",{"class":"_1S48_yUNpEI4uNY2-Bq_6R text-dark"})
	return str(owner[1].get_text())
def getlink(data):
	owner = data.find("a")
	return "https://www.baania.com/" + str(owner.attrs.get('href'))
def redata(data):
	jsonobj = {"type":gettype(data),"name":getname(data),"price":getprice(data),"address":getaddress(data),"owner":getowner(data),"link":getlink(data)}
	return json.dumps(jsonobj)

def getdata():
	start = time.time()
	tablename = "baania"
	urlnewhome = "https://www.baania.com/th/s/%E0%B8%97%E0%B8%B1%E0%B9%89%E0%B8%87%E0%B8%AB%E0%B8%A1%E0%B8%94/project?bedroomEq&max_price&min_price&propertyType&province=9128&sellState=on-sale&sort.updated=desc"
	get_newhome = requests.get(urlnewhome)
	print(get_newhome)
	soup = BeautifulSoup(get_newhome.text,'html.parser')
	find_word = soup.find_all("div",{"class":"card"})
	data_homenew = []
	for i in find_word:
		data_homenew.append(redata(i))
	baania = []

	for line in DBtools.savedata(data_homenew,tablename):
		baania.append(line)
	stop = time.time()
	t = stop-start
	print(tablename+" Time : "+str(t))
	return baania

def bubbletemp(msg):
	bubble = {"type": "bubble","size": "kilo","direction": "ltr","header": {
	"type": "box","layout": "vertical","backgroundColor": "#0095E9FF","contents": [
		{"type": "text","text": str(msg),"color": "#FFFFFFFF","align": "start","contents": []}
	]
	},
	"body": {"type": "box","layout": "vertical","contents": []
	}
}
	return bubble
def boxtemp(type,name,price,address,owner,link):
	box = {"type": "box","layout": "vertical","contents":
						[
							{"type": "text","text": "ประเภท " + str(type),"align": "start","contents": []},
							{"type": "text","text": "ราคา "+str(price)+" บาท","contents": []},
							{"type": "text","text": "ชื่อ "+str(name),"contents": []},
							{"type": "text","text": str(owner),"contents": []},
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
			addbox = boxtemp(str(row["type"]),str(row["name"]),str(row["price"]),str(row["address"]),str(row["owner"]),str(row["link"]))
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
				addbox = boxtemp(str(row["type"]),str(row["name"]),str(row["price"]),str(row["address"]),str(row["owner"]),str(row["link"]))
				bubbleset["body"]["contents"].append(addbox)
			else:
				carousel["contents"].append(bubbleset)
				bubbleset = bubbletemp(msg)
				num = 0
				addbox = boxtemp(str(row["type"]),str(row["name"]),str(row["price"]),str(row["address"]),str(row["owner"]),str(row["link"]))
				bubbleset["body"]["contents"].append(addbox)
				num += 1
		carousel["contents"].append(bubbleset)
		return json.dumps(carousel)
