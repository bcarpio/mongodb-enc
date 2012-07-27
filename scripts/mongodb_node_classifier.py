#!/usr/bin/python
#!/usr/bin/python

from pymongo import *
import yaml
import sys
from ConfigParser import SafeConfigParser
import glob

parser = SafeConfigParser()
config = ['../conf/conf.ini']
found = parser.read(config)
db = parser.get('mongodb_info', 'mongodb_db_name')
col = parser.get('mongodb_info', 'mongodb_db_name')
host = parser.get('mongodb_info', 'mongodb_servers')
#host = ['arch-mongod-s1-01','arch-mongod-s1-02','arch-mongod-s1-03','arch-mongod-s1-04']
sep = '.'
node = sys.argv[1]
node = node.split('.')[0]

def conn_mongodb():
        con = Connection(host)
        db = con.puppet
        col = db.nodes
        d = col.find_one({"node": node})
        if d == None:
                sys.exit(1)
        print yaml.safe_dump(d['enc'], default_flow_style=False)


conn_mongodb()
#print host
