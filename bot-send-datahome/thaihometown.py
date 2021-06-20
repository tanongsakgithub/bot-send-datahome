import requests
import re
import time
import json
import DBtools
from bs4 import BeautifulSoup
def gettype(data):
	type = data.find("div",{"class":"namedes"}).get_text().replace(", ","-")
	return str(type)
def getdetail(data):
	detail = data.find("div",{"class":"tsprice"}).get_text().replace("ตารางวา","ตร.ว.").replace("ตารางเมตร","ตร.ม.")
	result = detail[:(detail.find("ราคา"))]
	return str(result)
def getprice(data):
	#price = data.find("div",{"class":"pirced"}).get_text(strip=True, separator='\n').replace("ราคาขาย","ขาย").replace("ให้เช่า","เช่า").replace("บาท","บ.")
	price = data.find("div",{"class":"pirced"}).get_text(strip=True, separator=' ').replace("ราคาขาย","ขาย").replace("ให้เช่า","เช่า").replace("บาท","บ.")
	return str(price)
def getlink(data):
	owner = data.find_all("a")
	return str(owner[0].attrs.get('href'))
def redata(data):
	jsonobj = {"type":gettype(data),"detail":getdetail(data),"price":getprice(data),"link":getlink(data)}
	return json.dumps(jsonobj)

def getdata():
	start = time.time()
	tablename = "thaihometown"
	urlthaihometown = "https://www.thaihometown.com/search/?Type=&Area=&Unit=&Room1=&FormType=&Selling1=&Rented1=&Selling3=&Selling2=&Rented2=&Rented3=&BTS=&MRT=&PURPLE=&Country=%CA%A7%A2%C5%D2&City=&AirportLink=&Numid=&Keyword=&Submit=Search"
	get_newhome = requests.get(urlthaihometown)
	print(get_newhome)
	soup = BeautifulSoup(get_newhome.content,'html.parser',from_encoding="utf-8")
	find_word = soup.find_all("table",{"class":"tablelist"})
	data_homenew = []
	for i in find_word:
		data_homenew.append(redata(i))
	thaihometown = []
	for line in DBtools.savedata(data_homenew,tablename):
		thaihometown.append(line)
	stop = time.time()
	t = stop-start
	print(tablename+" Time : "+str(t))
	return thaihometown

def bubbletemp(msg):
	bubble = {"type": "bubble","size": "giga","direction": "ltr","header": {
	"type": "box","layout": "vertical","backgroundColor": "#0095E9FF","contents": [
		{"type": "text","text": str(msg),"color": "#FFFFFFFF","align": "start","contents": []}
	]
	},
	"body": {"type": "box","layout": "vertical","contents": []
	}
}
	return bubble
def boxtemp(type,detail,price,link):
	box = {"type": "box","layout": "vertical","contents":
						[
							{"type": "text","text": str(type),"align": "start","contents": []},
							{"type": "text","text": str(price),"wrap": True,"contents": []},
							{"type": "text","text": str(detail),"wrap": True,"contents": []},
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
			addbox = boxtemp(str(row["type"]),str(row["detail"]),str(row["price"]),str(row["link"]))
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
				addbox = boxtemp(str(row["type"]),str(row["detail"]),str(row["price"]),str(row["link"]))
				bubbleset["body"]["contents"].append(addbox)
			else:
				carousel["contents"].append(bubbleset)
				bubbleset = bubbletemp(msg)
				num = 0
				addbox = boxtemp(str(row["type"]),str(row["detail"]),str(row["price"]),str(row["link"]))
				bubbleset["body"]["contents"].append(addbox)
				num += 1
		carousel["contents"].append(bubbleset)
		return json.dumps(carousel)
