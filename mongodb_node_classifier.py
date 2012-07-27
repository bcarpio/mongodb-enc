#!/usr/bin/python

from pymongo import *
import yaml
import sys
import pprint

db = 'puppet'
col = 'nodes'
sep = '.'
node = sys.argv[1]
node = node.split('.')[0]
host = 'arch-mongod-s1-02'

def conn_mongodb():
        con = Connection(host)
        db = con.puppet
        col = db.nodes
        d = col.find_one({"node": node})
        print yaml.safe_dump(d['enc'], default_flow_style=False)


conn_mongodb()
