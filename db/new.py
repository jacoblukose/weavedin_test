from sqlalchemy import *
import logging


class Mysql(): 

	def __init__(self):
		self.url = 'mysql+pymysql://root:helloworld@localhost:3306/sample_db?charset=utf8&use_unicode=0'
		engine = create_engine(self.url, pool_recycle=3600)
		try:
			connection = engine.connect()
		except Exception, error_info:
			logging.error("Mysql not initialised \n ERROR : %s", error_info)
			raise
		logging.info("Mysql Instance created")
		return 

	def status(self):
		pass 