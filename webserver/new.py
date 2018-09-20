from flask import json
import logging
from flask import Response


class Webserver():
	"""
	Class implements web server functions. 

	200 OK
	
	409 Conflict - if server will not process request, 
	but reason for that is not client's fault

	400 Bad Request - when server will not process 
	request because it's obvious client fault
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


	def activity_log(self, user, stime, etime):
		temp = {}
		temp["user"] = user
		temp["start_time"] = stime
		temp["end_time"] = etime
 
		result = self.db.activitylogDB(temp)
		if result:
			js = json.dumps(result)
			resp = Response(js, status=200, mimetype='application/json')
			return resp
		else: 
			js = json.dumps({"ACTIVITY_LOG": "EMPTY"})
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
		else:
			js = json.dumps({"ADD_ITEM": "ITEM ALREADY EXISTS"})
			resp = Response(js, status=409, mimetype='application/json')
			return resp



	def edit_item(self, data, item_product_code):
		temp = {}
		temp["productcode"] = item_product_code
		for key,val in data.iteritems():
				temp[key] = val
		if self.db.editItemDB(temp):
			js = json.dumps({"EDIT_ITEM": "SUCCESS"})
			resp = Response(js, status=200, mimetype='application/json')
			return resp



	def edit_variant(self, item_product_code, variant_name, data):
		temp = {}
		temp['name'] = variant_name
		temp['itemid'] = item_product_code
		for key,val in data.iteritems():
				temp[key] = val
		if self.db.editVariantDB(temp):
			js = json.dumps({"EDIT_VARIANT": "SUCCESS"})
			resp = Response(js, status=200, mimetype='application/json')
			return resp		


	def add_variant(self, item_product_code, data):
		temp = {}
		temp['itemid'] = item_product_code
		for key,val in data.iteritems():
				temp[key] = val
		if self.db.addVariantDB(temp):
			js = json.dumps({"ADD_VARIANT": "SUCCESS"})
			resp = Response(js, status=200, mimetype='application/json')
			return resp	
		else:
			js = json.dumps({"ADD_VARIANT": "VARIANT ALREADY EXISTS"})
			resp = Response(js, status=409, mimetype='application/json')
			return resp	


	def del_variant(self, data):
		temp = {}
		for key,val in data.iteritems():
				temp[key] = val
		if self.db.delVariantDB(temp):
			js = json.dumps({"DEL_VARIANT": "SUCCESS"})
			resp = Response(js, status=200, mimetype='application/json')
			return resp	
		else:
			js = json.dumps({"DEL_VARIANT": "VARIANT ALREADY DELETED"})
			resp = Response(js, status=409, mimetype='application/json')
			return resp	





