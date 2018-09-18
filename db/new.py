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
		logging.info("changehistoryDB")
		with DatabaseSession(self.engine) as session:
			pass 


	def addItemDB(self, data):
		logging.info("addItemDB")
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
		logging.info("editItemDB")
		with DatabaseSession(self.engine) as session:
			item_data = session.query(Item).get(data['productcode'])
			if item_data == None:
				return False
			else:
				item_data.name = data["name"]
				item_data.brand = data["brand"]
				item_data.category = data["category"]
				item_data.productCode = data["productcode"]
				session.add(item_data)
				session.commit()
				return True	


	def addVariantDB(self, data):
		logging.info("addVariantDB")
		with DatabaseSession(self.engine) as session:

			var_code = md5( data['itemid']  + data['name']  ).hexdigest()
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
		logging.info("editVariantDB")
		with DatabaseSession(self.engine) as session:
			variant_code = md5( data['itemid']  + data['name']  ).hexdigest()
			variant_data = session.query(Variant).get(variant_code)
			if variant_data == None:
				return False
			else:
				properties = json.loads(data['properties'])
				variant_data.name = data["name"]
				variant_data.sellingPrice = data["sellingprice"]
				variant_data.costPrice = data["costprice"]
				variant_data.quantity = data["quantity"]

				session.add(variant_data)
				session.flush()
				session.commit()
				session.query(Property).filter(Property.variant_code==variant_code).update({ "size":properties['size'],
										"cloth": properties['cloth'] }, 
										synchronize_session='fetch')
				session.commit()
				return True     
	

	def delVariantDB(self, data):
		logging.info("delVariantDB")
		with DatabaseSession(self.engine) as session:
				variant_code = md5(data['itemid']  + data['name']).hexdigest()
				variant_data = session.query(Variant).get(variant_code)
				if variant_data == None:
					return False
				else:
					session.query(Property).filter(Property.variant_code==variant_code).delete(synchronize_session='fetch')
					session.delete(variant_data)
					session.commit()
					return True








