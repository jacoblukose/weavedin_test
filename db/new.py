from sqlalchemy import *
import logging
from sqlalchemy.orm import Session
from db import DatabaseConnection, DatabaseSession
from entities import EntityConstructor, Item, Variant, Property
from hashlib import md5
from time import localtime
from random import *
import json 


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

		logging.info("DB schema created")
		return 

	def getdata(self):
		result = self.engine.execute("select name from tablename")
		for row in result:
			print "name:", row['name']
		result.close()


	def changehistoryDB(self, data):
		with DatabaseSession(self.engine) as session:
			pass 
			

	def addItemDB(self, data):
		with DatabaseSession(self.engine) as session:
			instance = Item( name = data['name'],
							 brand = data['brand'],
							 category = data['category'],
							 productCode = data['productcode'],
							 user = "dummy"
							 )
			session.add(instance)
			session.flush()
			session.commit()

	def editItemDB(self, data):
		with DatabaseSession(self.engine) as session:
			pass 		


	def addVariantDB(self, data):
		with DatabaseSession(self.engine) as session:

			var_code = md5(str(localtime()) + data['itemid']  + data['name'] + str(uniform(1, 1000)) ).hexdigest()
			properties = json.loads(data['properties'])
			instance = Variant( 
								var_code = var_code,
								name = data['name'],
								sellingPrice = data['sellingprice'],
								costPrice = data['costprice'],
								quantity = data['quantity'],
								user = "dummy",
								item_id = data["itemid"]
								)

			

			session.add(instance)
			session.flush()
			session.commit()

			properties = Property( cloth = properties['cloth'],
								   size = properties['size'] ,
								   variant_code = var_code
								  )

			session.add(properties)
			session.flush()
			session.commit()

	def editVariantDB(self, data):
		with DatabaseSession(self.engine) as session:
			pass 	

	def delVariantDB(self, data):
		with DatabaseSession(self.engine) as session:
			pass 







