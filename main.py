import logging
import signal 
import sys
from argparse import ArgumentParser
from utility import UtilityTools 
from flask import render_template,request,Flask,json
from webserver.new import Webserver as ws 
from db.new import Mysql as mysql

class GracefulController(object):
	"""
	Class ensure graceful shutdown of the server and instances. 
	"""
	def __init__(self, confObj = None):
		self.conf = confObj

	def __enter__(self):
		# set up signals here
		# store old signal handlers as instance variables
		logging.info("GracefulController __enter__")
		signal.signal(signal.SIGINT, self.sigint_handler)
		signal.signal(signal.SIGTERM, self.sigint_handler)
		self.chief = Initialise(self.conf)
		return self.chief

	def sigint_handler(self, signal, frame):
		""" 
			Handle signals from kernel 
		"""
		logging.info("signal captured %s %s", signal, frame)
		sys.exit(0)

	def __exit__(self, type, value, traceback):
		logging.info("GracefulController __Delete__")


class Initialise(object):

	
	def __init__(self,conf):

		#Initialise web server object
		self.ws = ws()
		self.ws.ws_url = UtilityTools().KeylookUP(CONF["server"]["host"])

		#Initialise database object
		self.db = mysql()



if __name__ == "__main__":
	
	PARSER = ArgumentParser()
	PARSER.add_argument("-c", "--config", required=True,
						action="store", dest="conf_file_path",
						help="Pass the config file")

	PARSER.add_argument("-l", "--loglevel", required=False,
						action="store", dest="cli_loglevel",
						help="Set loglevel")
	ARGS = PARSER.parse_args()

	CONF_PATH     = ARGS.conf_file_path
	CONF          = UtilityTools().readJson(CONF_PATH)
	LOG_LEVEL     = UtilityTools().KeylookUP(CONF["general"]["loglevel"])
	
	if ARGS.cli_loglevel is not None:
		LOG_LEVEL = ARGS.cli_loglevel
	logging.root.handlers = []
	logging.basicConfig(level = LOG_LEVEL, 
					format='%(asctime)s %(name)s.%(funcName)s +%(lineno)s:%(levelname)-8s  %(message)s',
					datefmt='%m/%d/%Y %I:%M:%S %p')

	logging.info('Starting app')

	with GracefulController(CONF) as chief:
		app = Flask(__name__, static_folder='static')

		@app.route('/status',methods=['GET'])
		def status():
			return chief.ws.status_check()
		
		@app.route('/changehistory',methods=['GET','POST'])
		def change_history():
			return chief.ws.change_history()

		app.debug = True
		app.run(host=chief.ws.ws_url, threaded=True)

