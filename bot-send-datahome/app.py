from flask import Flask, request, abort
import requests
import re
import time
import json
import DBtools
import baania
import kaidee
import thaihometown
import facebook
import os
from bs4 import BeautifulSoup
from linebot import (
	LineBotApi, WebhookHandler
)
from linebot.exceptions import (
	InvalidSignatureError
)
from linebot.models import (
	MessageEvent, TextMessage, TextSendMessage,FlexSendMessage
)

app = Flask(__name__)


pushtoken = os.environ['LINE_GROUP_ID']
line_bot_api = LineBotApi(os.environ['YOUR_CHANNEL_ACCESS_TOKEN'])
handler = WebhookHandler(os.environ['YOUR_CHANNEL_SECRET'])


@app.route("/callback", methods=['POST'])
def callback():
	# get X-Line-Signature header value
	signature = request.headers['X-Line-Signature']
	# get request body as text
	body = request.get_data(as_text=True)
	app.logger.info("Request body: " + body)
	# handle webhook body
	try:
		handler.handle(body, signature)
	except InvalidSignatureError:
		print("Invalid signature. Please check your channel access token/channel secret.")
		abort(400)
	return 'OK'

#@handler.add(MessageEvent)
def handler_message():
	nonewdata = []
	botstart = time.time()
	try:
		datakaidee = kaidee.getdata()
		countdatakaidee = len(datakaidee)
		if(countdatakaidee == 0):
			nonewdata.append("Kaidee")
			#line_bot_api.push_message(pushtoken,TextSendMessage(text="ไม่มีข้อมูลใหม่สำหรับ kaidee"))
		else:
			msg = str(countdatakaidee)+" รายการจาก kaidee"
			resultobj = json.loads(kaidee.flexobj(datakaidee,msg))
			print("kaidee >> "+str(countdatakaidee))
			line_bot_api.push_message(pushtoken,FlexSendMessage(alt_text=msg, contents=resultobj))
	except:
		print("Error Kaidee")
		#line_bot_api.push_message(pushtoken,TextSendMessage(text="ข้อผิดพลาด kaidee"))

	try:
		databaania = baania.getdata()
		countdatabaania = len(databaania)
		if(countdatabaania == 0):
			nonewdata.append("Baania")
			#line_bot_api.push_message(pushtoken,TextSendMessage(text="ไม่มีข้อมูลใหม่สำหรับ baania"))
		else:
			msg = str(countdatabaania)+" รายการจาก baania"
			resultobj = json.loads(baania.flexobj(databaania,msg))
			print("baania >> "+str(countdatabaania))
			line_bot_api.push_message(pushtoken,FlexSendMessage(alt_text=msg, contents=resultobj))
	except:
		print("Error Baania")
		#line_bot_api.push_message(pushtoken,TextSendMessage(text="ข้อผิดพลาด baania"))

	try:
		datathaihometown = thaihometown.getdata()
		countdatathaihometown = len(datathaihometown)
		if(countdatathaihometown == 0):
			nonewdata.append("ThaiHomeTown")
			#line_bot_api.push_message(pushtoken,TextSendMessage(text="ไม่มีข้อมูลใหม่สำหรับ ThaiHomeTown"))
		else:
			msg = str(countdatathaihometown)+" รายการจาก ThaiHomeTown"
			resultobj = json.loads(thaihometown.flexobj(datathaihometown,msg))
			print("ThaiHomeTown >> "+str(countdatathaihometown))
			message = FlexSendMessage(alt_text=msg, contents=resultobj)
			line_bot_api.push_message(pushtoken,message)
	except:
		print("Error ThaiHomeTown")
		#line_bot_api.push_message(pushtoken,TextSendMessage(text="ข้อผิดพลาด ThaiHomeTown"))
	try:
		datafacebook = facebook.getdata()
		countdatafacebook = len(datafacebook)
		if(countdatafacebook == 0):
			nonewdata.append("Facebook")
			#line_bot_api.push_message(pushtoken,TextSendMessage(text="ไม่มีข้อมูลใหม่สำหรับ facebook"))
		else:
			msg = str(countdatafacebook)+" รายการจาก facebook"
			print("facebook >> "+str(countdatafacebook))
			resultobj = json.loads(facebook.flexobj(datafacebook,msg))
			message = FlexSendMessage(alt_text=msg, contents=resultobj)
			line_bot_api.push_message(pushtoken,message)
	except:
		print("Error Facebook")
		#line_bot_api.push_message(pushtoken,TextSendMessage(text="ข้อผิดพลาด facebook"))

	msg = "ไม่มีข้อมูลใหม่สำหรับ "
	if(len(nonewdata) > 0):
		for web in nonewdata:
			msg = msg + str(web) + " "
		line_bot_api.push_message(pushtoken,TextSendMessage(text=msg))
	botstop = time.time()
	total = botstop-botstart
	print("total Time : "+str(total))

@app.route("/Bot", methods=['POST'])
def push_msg():
	handler_message()
	return 'OK'

@app.route("/wake", methods=['GET'])
def app_wake():
	time.sleep(1)
	return 'OK'

@handler.add(MessageEvent)
def handle_2(event):
	if(event.message.text == "start"):
		time.sleep(1)
		line_bot_api.reply_message(event.reply_token,TextSendMessage(text="OK"))
	if(event.message.text == "kaidee"):
		try:
			datakaidee = kaidee.getdata()
			countdatakaidee = len(datakaidee)
			if(countdatakaidee == 0):
				line_bot_api.reply_message(event.reply_token,TextSendMessage(text="ไม่มีข้อมูลใหม่สำหรับ kaidee"))
			else:
				msg = str(countdatakaidee)+" รายการจาก kaidee"
				resultobj = json.loads(kaidee.flexobj(datakaidee,msg))
				print("Kaidee >> "+str(countdatakaidee))
				message = FlexSendMessage(alt_text=msg, contents=resultobj)
				line_bot_api.reply_message(event.reply_token,message)
		except:
			line_bot_api.reply_message(event.reply_token,TextSendMessage(text="ข้อผิดพลาด kaidee"))
	if(event.message.text == "baania"):
		try:
			databaania = baania.getdata()
			countdatabaania = len(databaania)
			if(countdatabaania == 0):
				line_bot_api.reply_message(event.reply_token,TextSendMessage(text="ไม่มีข้อมูลใหม่สำหรับ baania"))
			else:
				msg = str(countdatabaania)+" รายการจาก baania"
				resultobj = json.loads(baania.flexobj(databaania,msg))
				print("baania >> "+str(countdatabaania))
				message = FlexSendMessage(alt_text=msg, contents=resultobj)
				line_bot_api.reply_message(event.reply_token,message)
		except:
			line_bot_api.reply_message(event.reply_token,TextSendMessage(text="ข้อผิดพลาด baania"))
	if(event.message.text == "thaihometown"):
		try:
			datathaihometown = thaihometown.getdata()
			countdatathaihometown = len(datathaihometown)
			if(countdatathaihometown == 0):
				line_bot_api.reply_message(event.reply_token,TextSendMessage(text="ไม่มีข้อมูลใหม่สำหรับ ThaiHomeTown"))
			else:
				msg = str(countdatathaihometown)+" รายการจาก ThaiHomeTown"
				resultobj = json.loads(thaihometown.flexobj(datathaihometown,msg))
				print("ThaiHomeTown >> "+str(countdatathaihometown))
				message = FlexSendMessage(alt_text=msg, contents=resultobj)
				line_bot_api.reply_message(event.reply_token,message)
		except:
			line_bot_api.reply_message(event.reply_token,TextSendMessage(text="ข้อผิดพลาด ThaiHomeTown"))

	if(event.message.text == "facebook"):
		try:
			datafacebook = facebook.getdata()
			countdatafacebook = len(datafacebook)
			if(countdatafacebook == 0):
				line_bot_api.reply_message(event.reply_token,TextSendMessage(text="ไม่มีข้อมูลใหม่สำหรับ facebook"))
			else:
				msg = str(countdatafacebook)+" รายการจาก facebook"
				resultobj = json.loads(facebook.flexobj(datafacebook,msg))
				print("facebook >> "+str(countdatafacebook))
				message = FlexSendMessage(alt_text=msg, contents=resultobj)
				line_bot_api.reply_message(event.reply_token,message)
		except:
			line_bot_api.reply_message(event.reply_token,TextSendMessage(text="ข้อผิดพลาด facebook"))

	if(event.message.text == "kaidee-del"):
		time.sleep(1)
		try:
			DBtools.cleartable("kaidee")
			line_bot_api.reply_message(event.reply_token,TextSendMessage(text="Clear Table kaidee"))
		except:
			line_bot_api.reply_message(event.reply_token,TextSendMessage(text="Clear Table Error"))
	if(event.message.text == "baania-del"):
		time.sleep(1)
		try:
			DBtools.cleartable("baania")
			line_bot_api.reply_message(event.reply_token,TextSendMessage(text="Clear Table baania"))
		except:
			line_bot_api.reply_message(event.reply_token,TextSendMessage(text="Clear Table Error"))
	if(event.message.text == "thaihometown-del"):
		time.sleep(1)
		try:
			DBtools.cleartable("thaihometown")
			line_bot_api.reply_message(event.reply_token,TextSendMessage(text="Clear Table thaihometown"))
		except:
			line_bot_api.reply_message(event.reply_token,TextSendMessage(text="Clear Table Error"))
	if(event.message.text == "facebook-del"):
		time.sleep(1)
		try:
			DBtools.cleartable("facebook")
			line_bot_api.reply_message(event.reply_token,TextSendMessage(text="Clear Table facebook"))
		except:
			line_bot_api.reply_message(event.reply_token,TextSendMessage(text="Clear Table Error"))
	if(event.message.text == "dbrow"):
		time.sleep(1)
		try:
			rowkaidee = DBtools.Tablerowlen("kaidee")
			rowbaania = DBtools.Tablerowlen("baania")
			rowthaihometown = DBtools.Tablerowlen("ThaiHomeTown")
			rowfacebook = DBtools.Tablerowlen("facebook")
			msg = "Kaidee > "+str(rowkaidee)+"\n"+"baania > "+str(rowbaania)+"\n"+"ThaiHomeTown > "+str(rowthaihometown)+"\n"+"facebook > "+str(rowfacebook)
			line_bot_api.reply_message(event.reply_token,TextSendMessage(text=msg))
		except:
			line_bot_api.reply_message(event.reply_token,TextSendMessage(text="Check DB Row Error"))

if __name__ == "__main__":
	#app.run()
	port = int(os.environ.get("PORT", 5000))
	app.run(host='0.0.0.0', port=port)