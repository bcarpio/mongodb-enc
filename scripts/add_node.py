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

	cmd_parser = argparse.ArgumentParser(description='Add Nodes To Mongodb ENC')
	cmd_parser.add_argument('-n', '--node', dest='puppet_node', help='Puppet Node Hostname', required=True)
	cmd_parser.add_argument('-c', '--class', dest='puppet_classes', help='Can specify multiple classes each with -c', action='append', required=True)
	cmd_parser.add_argument('-p', '--param', dest='puppet_param', help='Can specify multiple paramaters each with -p', action='append')
	cmd_parser.add_argument('-i', '--inherit', dest='puppet_inherit', help='Define a node to inherit classes from', action='store')
	cmd_parser.add_argument('-e', '--environment', dest='environment', help='Optional, defaults to "production"', default='production')
	args = cmd_parser.parse_args()

	c = {}
	for pclass in args.puppet_classes:
		c[pclass] = ''

	d = { 'node' : args.puppet_node, 'enc' : { 'classes': c , 'environment' : args.environment }}

	if args.puppet_param:
		args.puppet_param = dict([arg.split('=') for arg in args.puppet_param])
		d['enc']['parameters'] = args.puppet_param

	if args.puppet_inherit:
		d['inherit'] = args.puppet_inherit

	col = connect_mongodb()

	check = col.find({ 'node' : args.puppet_node },{'node': 1})
	for document in check:
		node = document['node']
		if node == args.puppet_node:  
			print args.puppet_node+" Exists In Mongodb. Please Remove Node"
			sys.exit(1)

	col.ensure_index('node', unique=True)
	col.insert(d)

if __name__ == "__main__":
	main()
