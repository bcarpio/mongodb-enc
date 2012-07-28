#!/usr/bin/python

from pymongo import *
import yaml
import sys
from ConfigParser import SafeConfigParser
import argparse
import glob


parser = SafeConfigParser()
config = ['../conf/conf.ini']
found = parser.read(config)
db = parser.get('mongodb_info', 'mongodb_db_name')
col = parser.get('mongodb_info', 'mongodb_db_name')
host = parser.get('mongodb_info', 'mongodb_servers')

def connect_mongodb():
	con = Connection(host)
	db = con.puppet
	col = db.nodes
	return col

def main():

	cmd_parser = argparse.ArgumentParser(description='Add Nodes To Mongodb ENC')
	cmd_parser.add_argument('-n', '--node', dest='puppet_node', required=True)
	cmd_parser.add_argument('-c', '--classes', dest='puppet_classes', required=True)
	cmd_parser.add_argument('-e', '--environment', dest='environment', default='production')
	args = cmd_parser.parse_args()
	col = connect_mongodb()
	d = { 'node' : args.puppet_node, 'enc' : { 'classes': { args.puppet_classes : '' }, 'environment' : args.environment }}
	col.insert(d)
	

if __name__ == "__main__":
	main()
