#!/usr/bin/python

from pymongo import *
import yaml
import sys
from ConfigParser import SafeConfigParser
import glob


parser = SafeConfigParser()
config = ['../conf/conf.ini']
found = parser.read(config)
db = parser.get('mongodb_info', 'mongodb_db_name')
col = parser.get('mongodb_info', 'mongodb_db_name')
host = parser.get('mongodb_info', 'mongodb_servers')

def search_mongodb():
	con = Connection(host)
	db = con.puppet
	col = db.nodes
	d = col.find({}, { '_id' : 0 } )
	if d == None:
		print "ERROR: No Nodes Found In ENC" 
		sys.exit(1)
	for document in d:
#		print document
#		print yaml.safe_dump(document, default_flow_style=False)
		print yaml.safe_dump(document)

search_mongodb()
