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
	cmd_parser.add_argument('-a', '--action', dest='puppet_action', choices=['append', 'new'], help='Append Or Recreate Default Node', required=True)
	cmd_parser.add_argument('-c', '--class', dest='puppet_classes', help='Can specify multiple classes each with -c', action='append', required=True)
	args = cmd_parser.parse_args()


	c = {}
	col = connect_mongodb()
	col.ensure_index('node', unique=True)

	for pclass in args.puppet_classes:
		c[pclass] = ''

	if args.puppet_action == 'append':
		d = { 'node' : 'default', 'enc' : { 'classes': c }}
		check = col.find_one({ 'node' : 'default' },{'node': 1})
		if not check:
			print "Default Node Doesn't Exist, Please Add It First"
			sys.exit(1)
		ec = col.find_one({ 'node' : 'default'})
		ec['enc']['classes']
		ec['enc']['classes'].update(c)
		col.remove({ 'node' : 'default'})
		col.insert(ec)

	if args.puppet_action == 'new':
		d = { 'node' : 'default', 'enc' : { 'classes': c }}
		check = col.find_one({ 'node' : 'default' },{'node': 1})
		if check:
			col.remove({ 'node' : 'default'})
		col.insert(d)

if __name__ == "__main__":
	main()
