from flask import json
import logging

class Webserver():
	"""
	Class implements web server functions. 
	"""

	def __init__(self):
		self.ws_url = 'localhost'
		logging.info("Webserver Instance created")
		return 
		
	def status_check(self):
		return json.dumps({"Status": True})


	def change_history(self):
		return json.dumps({"change_history": True})


	def edit_item(self, data):
		return json.dumps({"edit_item": True})

	def edit_variant(self, data):
		return json.dumps({"edit_variant": True})

	def add_variant(self, data):
		return json.dumps({"add_variant": True})

	def del_variant(self, data):
		return json.dumps({"del_variant": True})


