#!/usr/bin/python

from pymongo import *
import yaml
import sys
from ConfigParser import SafeConfigParser
from optparse import OptionParser
import glob


if (len(sys.argv) < 2):
    print "ERROR: Please Supply A Hostname or FQDN"
    sys.exit(1)

parser = SafeConfigParser()
config = ['../conf/conf.ini']
found = parser.read(config)
db = parser.get('mongodb_info', 'mongodb_db_name')
col = parser.get('mongodb_info', 'mongodb_db_name')
host = parser.get('mongodb_info', 'mongodb_servers')

cmd_parser = OptionParser()
cmd_parser.add_option("-n", "--node", dest="node", help="Node To Add To ENC", metavar="NODE")
cmd_parser.add_option("-c", "--class", dest="class", help="Class(s) To Be Added To Node In ENC", metavar="CLASS")

#doc = { 'node' : node, 'enc' : { 'classes': 
