#!/usr/bin/python

from pymongo import *
import yaml
import sys, os
from ConfigParser import SafeConfigParser
import glob


def main():

	if (len(sys.argv) < 2):
   	 print "ERROR: Please Supply A Hostname or FQDN"
   	 sys.exit(1)

	# Import conf.ini
	parser = SafeConfigParser()
	config = os.path.join(os.path.dirname(__file__),"../conf/conf.ini")
	found = parser.read(config)
	database = parser.get('mongodb_info', 'mongodb_db_name')
	collection = parser.get('mongodb_info', 'mongodb_collection_name')
	host = parser.get('mongodb_info', 'mongodb_servers')

	# Probably want to remove this. This is because I don't use FQDNs in my current puppet manifest. 
	# also made this easier for me to test.
	sep = '.'
	node = sys.argv[1]
	node = node.split('.')[0]

	# Connect to mongodb
	con = Connection(host)
	col = con[database][collection]
	
	# Find the node given at a command line argument
	d = con[database][collection].find_one({"node": node}) 
	if d == None:
		print "ERROR: Node "+node+" Not Found In ENC" 
		sys.exit(1)

	# Check if the node requiers inheritance
	inherit = col.find_one({"node": node})
	if 'inherit' in inherit:
		inode = inherit['inherit']
		if not col.find_one({"node" : inode}):
			print "ERROR: Inheritance Node "+inode+" Not Found In ENC"
			sys.exit(1)
		iclass = col.find_one({"node": inode})
		iclass = iclass['enc']['classes']
		d['enc']['classes'].update(iclass)
	else:
		d['enc']['classes']

	print yaml.safe_dump(d['enc'], default_flow_style=False)


if __name__ == "__main__":
        main()
