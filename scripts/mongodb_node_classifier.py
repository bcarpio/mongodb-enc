#!/usr/bin/python

from pymongo import *
import yaml
import sys
from ConfigParser import SafeConfigParser
import glob


if (len(sys.argv) < 2):
    print "ERROR: Please Supply A Hostname or FQDN"
    sys.exit(1)

parser = SafeConfigParser()
config = ['../conf/conf.ini']
found = parser.read(config)
database = parser.get('mongodb_info', 'mongodb_db_name')
collection = parser.get('mongodb_info', 'mongodb_collection_name')
host = parser.get('mongodb_info', 'mongodb_servers')
sep = '.'
node = sys.argv[1]
node = node.split('.')[0]

def yaml_dump_mongodb():
	con = Connection(host)
	d = con[database][collection].find_one({"node": node}) 
	if d == None:
		print "ERROR: Node "+node+" Not Found In ENC" 
		sys.exit(1)
	print yaml.safe_dump(d['enc'], default_flow_style=False)

yaml_dump_mongodb()
