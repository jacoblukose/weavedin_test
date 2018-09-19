import json
import logging 
from hashlib import md5
from time import localtime
from random import *
import logging 



class UtilityTools():

	def readJson(self,filename):
		try:
			with open(filename) as json_data:
				file_handle = json.load(json_data)
		except (OSError, IOError) as e:
			logging.error("Cant open config file")
			raise 
		return file_handle 

	def KeylookUP(self, key):
		try:
			return key
		except KeyError as e:
			logging.error("KEY NOT FOUND")
			raise	
			