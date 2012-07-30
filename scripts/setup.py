#!/usr/bin/python
from pymongo import *
import yaml
import sys, os
from ConfigParser import SafeConfigParser
import argparse
import glob


parser = SafeConfigParser()
config = os.path.join(os.path.dirname(__file__),"../conf/conf.ini")
found = parser.read(config)
database = parser.get('mongodb_info', 'mongodb_db_name')
collection = parser.get('mongodb_info', 'mongodb_collection_name')
host = parser.get('mongodb_info', 'mongodb_servers')

def connect_mongodb():
	con = Connection(host)
	col = con[database][collection]
	return col

def main():

	cmd_parser = argparse.ArgumentParser(description='Add Default Node To Mongodb ENC')
	cmd_parser.add_argument('-u', '--update', dest='puppet_update', help='Update Default Node')
	cmd_parser.add_argument('-o', '--overwrite', dest='puppet_over', help='Overwrite Default Node') 
	cmd_parser.add_argument('-c', '--class', dest='puppet_classes', help='Can specify multiple classes each with -c', action='append', required=True)
	args = cmd_parser.parse_args()


	if not (args.puppet_update, args.puppet_over):
		print Error
		sys.exit(1)
	c = {}
	for pclass in args.puppet_classes:
		c[pclass] = ''

	d = { 'node' : 'default', 'enc' : { 'classes': c }}

	col = connect_mongodb()
	check = col.find({ 'node' : 'default' },{'node': 1})

	print d
#	col.ensure_index('node', unique=True)
#	col.insert(d)

if __name__ == "__main__":
	main()
