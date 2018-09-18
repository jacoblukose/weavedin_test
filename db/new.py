from sqlalchemy import *
import logging
from sqlalchemy.orm import Session
from db import DatabaseConnection
from entities import EntityConstructor


class Mysql(): 
	"""
	Class implemenets mysql functions.
	"""

	def __init__(self, host, user, password, dbname):

		self.host = host
		self.user = user
		self.password = password
		self.dbname = dbname
		self.url = "mysql+pymysql://" + self.user + ":"	+ self.password + "@" + self.host + "/" + self.dbname + "?charset=utf8&use_unicode=0"
		
		with DatabaseConnection(self.url) as db:
			self.dbconn , self.engine = db[0], db[1]
		
		logging.info("Mysql Instance created")

		self.en = EntityConstructor(self.engine)
		self.en.create()

		logging.info("DB instances created")
		return 


	def getdata(self):
		result = self.engine.execute("select name from tablename")
		for row in result:
			print "name:", row['name']
		result.close()
