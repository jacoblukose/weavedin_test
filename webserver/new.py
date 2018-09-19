from flask import json
import logging
from flask import Response


class Webserver():
	"""
	Class implements web server functions. 
	"""

	def __init__(self, db, url):
		self.ws_url = url
		self.db = db
		logging.info("Webserver Instance created")
		return 
		
	def status_check(self):
		js = json.dumps({"Status": "OK"})
		resp = Response(js, status=200, mimetype='application/json')
		return resp


	def activity_log(self, data):
		temp = {}
		for key,val in data.iteritems():
				temp[key] = val

		result = self.db.activitylogDB(temp)
		if result:
			js = json.dumps(result)
			resp = Response(js, status=200, mimetype='application/json')
			return resp
		else: 
			js = json.dumps({"ACTIVITY_LOG": "FAILED"})
			resp = Response(js, status=421, mimetype='application/json')
			return resp


	def add_item(self, data):
		temp = {}
		for key,val in data.iteritems():
				temp[key] = val
		if self.db.addItemDB(temp):
			js = json.dumps({"ADD_ITEM": "SUCCESS"})
			resp = Response(js, status=200, mimetype='application/json')
			return resp



	def edit_item(self, data):
		temp = {}
		for key,val in data.iteritems():
				temp[key] = val
		if self.db.editItemDB(temp):
			js = json.dumps({"EDIT_ITEM": "SUCCESS"})
			resp = Response(js, status=200, mimetype='application/json')
			return resp


	def edit_variant(self, data):
		temp = {}
		for key,val in data.iteritems():
				temp[key] = val
		if self.db.editVariantDB(temp):
			js = json.dumps({"EDIT_VARIANT": "SUCCESS"})
			resp = Response(js, status=200, mimetype='application/json')
			return resp		


	def add_variant(self, data):
		temp = {}
		for key,val in data.iteritems():
				temp[key] = val
		if self.db.addVariantDB(temp):
			js = json.dumps({"ADD_VARIANT": "SUCCESS"})
			resp = Response(js, status=200, mimetype='application/json')
			return resp	


	def del_variant(self, data):
		temp = {}
		for key,val in data.iteritems():
				temp[key] = val
		if self.db.delVariantDB(temp):
			js = json.dumps({"DEL_VARIANT": "SUCCESS"})
			resp = Response(js, status=200, mimetype='application/json')
			return resp	



