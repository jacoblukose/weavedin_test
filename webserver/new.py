from flask import json
import logging

class Webserver():
	def __init__(self):
		self.ws_url = 'localhost'
		logging.info("Webserver Instance created")
		return 
		
	def status_check(self):
		return json.dumps({"Status": True})


	def change_history(self):
		return json.dumps({"Default": True})


