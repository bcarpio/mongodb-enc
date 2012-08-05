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

	cmd_parser = argparse.ArgumentParser(description='Remove Nodes To Mongodb ENC')
	cmd_parser.add_argument('-n', '--node', dest='puppet_node', help='Puppet Node Hostname', required=True)
	args = cmd_parser.parse_args()

	col = connect_mongodb()
	isInode = col.find_one({ "inherit" : args.puppet_node })
	if isInode:
		isInode = col.find({ "inherit" : args.puppet_node })
		for node in isInode:
			print "ERROR: "+args.puppet_node+" is inherited by "+node['node']
	else:
		col.remove({ 'node' : args.puppet_node})

if __name__ == "__main__":
	main()
