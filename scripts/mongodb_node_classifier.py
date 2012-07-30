#!/usr/bin/python

from pymongo import *
import yaml
import sys, os
from ConfigParser import SafeConfigParser
import glob


if (len(sys.argv) < 2):
    print "ERROR: Please Supply A Hostname or FQDN"
    sys.exit(1)

parser = SafeConfigParser()
config = os.path.join(os.path.dirname(__file__),"../conf/conf.ini")
found = parser.read(config)
database = parser.get('mongodb_info', 'mongodb_db_name')
collection = parser.get('mongodb_info', 'mongodb_collection_name')
host = parser.get('mongodb_info', 'mongodb_servers')
sep = '.'
node = sys.argv[1]
node = node.split('.')[0]

def yaml_dump_mongodb():
	con = Connection(host)
	default = con[database][collection].find_one({"node": "default"})
	dclass = default['enc']['classes']
	d = con[database][collection].find_one({"node": node}) 
	if d == None:
		print "ERROR: Node "+node+" Not Found In ENC" 
		sys.exit(1)
	d['enc']['classes'].update(dclass)
	print yaml.safe_dump(d['enc'], default_flow_style=False)

yaml_dump_mongodb()
