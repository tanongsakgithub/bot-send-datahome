import os
import psycopg2
import json
import time
from psycopg2 import sql
DATABASE_URL = os.environ['DATABASE_URL']
#DATABASE_URL = "postgres://oojklvlvpoqxsh:5274c2b5bf702997fa25b8c7d92f252cdc7885284467bf97da2afa72e470ddb6@ec2-18-211-97-89.compute-1.amazonaws.com:5432/d9h18d2emkk6jd"
def CheckTableEmpty(tablename):
	conn = psycopg2.connect(DATABASE_URL, sslmode='require')
	cur = conn.cursor()
	sql = 'select count(*) from '+tablename+';'
	cur.execute(sql)
	result = cur.fetchone()
	if(result[0] <= 0):
		return True
	else:
		return False
	conn.commit()
	cur.close()
	conn.close()

def checksizetable(tablename):
	print("Check Size Data in Table "+tablename)
	conn = psycopg2.connect(DATABASE_URL, sslmode='require')
	cur = conn.cursor()
	sql1 = 'select rowid from '+tablename+';'
	cur.execute(sql1)
	data = []
	for i in cur.fetchall():
		data.append(i[0])
	totalcount = len(data)
	max = 100
	countdel = totalcount-50
	if(totalcount >= max):
		for i in range(0,int(countdel)):
			query = sql.SQL("DELETE FROM {table} WHERE rowid = (%s)").format(table=sql.Identifier(tablename))
			cur.execute(query,[data[i]])
			#cur.execute("""DELETE FROM kaidee WHERE rowid = (%s)""",[data[i]])
	conn.commit()
	cur.close()
	conn.close()

def duplicate(data,tablename):
	result = []
	print("Check Duplicate Data in Table " + tablename)
	conn = psycopg2.connect(DATABASE_URL, sslmode='require')
	cur = conn.cursor()
	query = sql.SQL("select data from {table}").format(table=sql.Identifier(tablename))
	cur.execute(query)
	datatable = cur.fetchall()
	dataintable = []
	for i in datatable:
		dataintable.append(i)
	for dataline in data:
		duplicate = False
		for row in dataintable:
			if(str(json.loads(dataline)) == row[0]):
				duplicate = True
				break
		if(duplicate == False):
			result.append(dataline)	
	conn.commit()
	cur.close()
	conn.close()
	return result

def savedata(data,tablename):
	result = []
	conn = psycopg2.connect(DATABASE_URL, sslmode='require')
	cur = conn.cursor()
	try:
		if(CheckTableEmpty(tablename) == True):
			print("Is Empty Table")
			for line in data:
				result.append(json.loads(line))
				query = sql.SQL("insert into {table} (data) values (%s)").format(table=sql.Identifier(tablename))
				cur.execute(query,[str(json.loads(line))])
		else:
			print("Is Not Empty Table")
			checksizetable(tablename)
			duplicateresult = duplicate(data,tablename)
			if(len(duplicateresult) >0 ):
				for line in duplicateresult:
					result.append(json.loads(line))
					query = sql.SQL("insert into {table} (data) values (%s)").format(table=sql.Identifier(tablename))
					cur.execute(query,[str(json.loads(line))])
		conn.commit()
		cur.close()
		conn.close()
		return result
	except:
		conn.commit()
		cur.close()
		conn.close()
		return data	

def cleartable(tablename):
	print("Clear table "+tablename)
	conn = psycopg2.connect(DATABASE_URL, sslmode='require')
	cur = conn.cursor()
	query = sql.SQL("DELETE FROM {table}").format(table=sql.Identifier(tablename))
	cur.execute(query)
	conn.commit()
	cur.close()
	conn.close()

def Tablerowlen(tablename):
	conn = psycopg2.connect(DATABASE_URL, sslmode='require')
	cur = conn.cursor()
	sql = 'select count(*) from '+tablename+';'
	cur.execute(sql)
	result = cur.fetchone()
	numrow = result[0]
	conn.commit()
	cur.close()
	conn.close()
	return numrow