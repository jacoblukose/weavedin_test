from flask import json
import logging
from flask import Response


class Webserver():
	"""
	Class implements web server functions. 
	"""

	def __init__(self, db):
		self.ws_url = 'localhost'
		self.db = db
		logging.info("Webserver Instance created")
		return 
		
	def status_check(self):
		return json.dumps({"Status": True})


	def change_history(self, data):
		temp = {}
		for key,val in data.iteritems():
				temp[key] = val

		result = self.db.changehistoryDB(temp)
		if result:
			js = json.dumps(result)
			resp = Response(js, status=200, mimetype='application/json')
			return resp

	def add_item(self, data):
		temp = {}
		for key,val in data.iteritems():
				temp[key] = val
		self.db.addItemDB(temp)
		return json.dumps({"edit_item": True})

	def edit_item(self, data):
		temp = {}
		for key,val in data.iteritems():
				temp[key] = val
		self.db.editItemDB(temp)
		return json.dumps({"edit_item": True})

	def edit_variant(self, data):
		temp = {}
		for key,val in data.iteritems():
				temp[key] = val
		self.db.editVariantDB(temp)
		return json.dumps({"edit_variant": True})

	def add_variant(self, data):
		temp = {}
		for key,val in data.iteritems():
				temp[key] = val
		self.db.addVariantDB(temp)
		return json.dumps({"add_variant": True})

	def del_variant(self, data):
		temp = {}
		for key,val in data.iteritems():
				temp[key] = val
		self.db.delVariantDB(temp)
		return json.dumps({"del_variant": True})


