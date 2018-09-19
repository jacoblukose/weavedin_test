import json 
import logging
import time
from random import *
from hashlib import md5
from sqlalchemy import *
from time import localtime
from datetime import datetime
from sqlalchemy.orm import Session


from db import DatabaseConnection, DatabaseSession
from entities import EntityConstructor, Item, Variant, Property, Changelog


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

	def activitylogDB(self, data):
		logging.info("changehistoryDB")
		start_time = data['start_time']
		end_time = data['end_time']
		current_time = time.strftime(r'%Y-%m-%d %H:%M:%S', 
									time.localtime())
		total = {}
		result = None
		print time, current_time

		if "user" in data:
			result = self.engine.execute("select * from changelog where created_date > %s AND created_date < %s AND user = %s" , 
																					start_time, end_time, data["user"])
		else:
			result = self.engine.execute("select * from changelog where created_date > %s AND created_date < %s" , 
																					start_time, end_time)
		
		for index,row in enumerate(result):
			result_data = {}
			result_data["id"] = row[0]
			result_data["mode"] = row[1]
			result_data["created_date"] = row[2]
			result_data["user"] = row[3]
			result_data["item_category"] = row[4]
			result_data["variants_category"] = row[5]
			result_data["properties_category"] = row[6]
			result_data["item_data"] = row[7]			
			result_data["variants_data "] = row[8]	
			result_data["properties_data"] = row[9]	
			total[index] = result_data
		result.close()
		return total

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

			changelog = Changelog( mode = "ADD",
								   user = "dummy",
								   item_category = True,
								   item_data = json.dumps({"productcode" : data['productcode']})
								   )
			session.add(changelog)
			session.flush()
			session.commit()
			logging.debug("Wrote activity log for addItem")
			return True
		return False

	def editItemDB(self, data):
		logging.info("editItemDB")
		with DatabaseSession(self.engine) as session:
			item_data = session.query(Item).get(data['productcode'])
			print item_data.name
			if item_data == None:
				return False
			else:
				temp = {}
				if item_data.name != data["name"]:
					item_data.name = data["name"]
					temp["name"] = data["name"]

				if item_data.brand != data["brand"]:
					item_data.brand = data["brand"]
					temp["brand"] = data["brand"]

				if item_data.category != data["category"]:
					item_data.category = data["category"]
					temp["category"] = data["category"]

				session.add(item_data)
				session.commit()

				if temp != {} :

					temp["productcode"] = data["productcode"]

					changelog = Changelog( mode = "EDIT",
										   user = "dummy",
										   item_category = True,
										   item_data = json.dumps(temp)
										)
					session.add(changelog)
					session.flush()
					session.commit()
					logging.debug("Wrote activity log for editItem")

				return True	
		return False


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


			changelog = Changelog( mode = "ADD",
								   user = "dummy",
								   item_category = True,
								   variants_category = True,
								   item_data = json.dumps({"productcode" : data['itemid']}),
								   variants_data = json.dumps({"variant_code" : var_code,
															   "variant_name" : data['name']})
								  )
			session.add(changelog)
			session.flush()
			session.commit()
			logging.debug("Wrote activity log for addVariant")
			return True
		return False

	def editVariantDB(self, data):
		logging.info("editVariantDB")
		with DatabaseSession(self.engine) as session:
			variant_code = md5( data['itemid']  + data['name']  ).hexdigest()
			variant_data = session.query(Variant).get(variant_code)
			if variant_data == None:
				return False
			else:
				temp = {}
				if  variant_data.name != data["name"]:
					 variant_data.name = data["name"]
					 temp["name"] = data["name"]

				print variant_data.sellingPrice, data["sellingprice"] 
				if variant_data.sellingPrice != data["sellingprice"]:
					variant_data.sellingPrice = data["sellingprice"]
					temp["sellingprice"] = data["sellingprice"]

				if variant_data.costPrice != data["costprice"]:
					variant_data.costPrice = data["costprice"]
					temp["costprice"] = data["costprice"]

				if variant_data.quantity != data["quantity"]:
					variant_data.quantity = data["quantity"]
					temp["quantity"] = data["quantity"]

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

				print temp
				if temp != {}:
	
					temp["variant_code"] = variant_code
					changelog = Changelog( mode = "EDIT",
										   user = "dummy",
										   item_category = True,
										   variants_category = True,
										   item_data = json.dumps({"productcode" : data['itemid']}),
										   variants_data = json.dumps(temp)
										  )
					session.add(changelog)
					session.flush()
					session.commit()
					logging.debug("Wrote activity log for editVariant")


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

					changelog = Changelog( mode = "DEL",
										   user = "dummy",
										   variants_category = True,
										   item_category = True,
										   item_data = json.dumps({"productcode" : data['itemid']}),
										   variants_data = json.dumps({"variant_code" : variant_code,
																	   "variant_name" : data['name']})
										   )
					session.add(changelog)
					session.flush()
					session.commit()
					logging.debug("Wrote activity log for delVariant")
					return True








