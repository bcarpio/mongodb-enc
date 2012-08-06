#!/usr/bin/python
# vim: set expandtab:
"""
**********************************************************************
GPL Licene
***********************************************************************
This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program. If not, see <http://www.gnu.org/licenses/>.

***********************************************************************/

:author: Brian Carpio
:email: bcarpio@thetek.net
:web: http://www.briancarpio.com

"""
from pymongo import Connection
import os
from ConfigParser import SafeConfigParser
import argparse

def main():

    """ This script removes nodes from mongodb """

    parser = SafeConfigParser()
    config = os.path.join(os.path.dirname(__file__),"../conf/conf.ini")
    parser.read(config)
    database = parser.get('mongodb_info', 'mongodb_db_name')
    collection = parser.get('mongodb_info', 'mongodb_collection_name')
    host = parser.get('mongodb_info', 'mongodb_servers')

    con = Connection(host)
    col = con[database][collection]

    cmd_parser = argparse.ArgumentParser(description='Remove Nodes To Mongodb ENC')
    cmd_parser.add_argument('-n', '--node', dest='puppet_node', help='Puppet Node Hostname', required=True)
    args = cmd_parser.parse_args()

    isinode = col.find_one({ "inherit" : args.puppet_node })
    if isinode:
        isinode = col.find({ "inherit" : args.puppet_node })
        for node in isinode:
            print "ERROR: "+args.puppet_node+" is inherited by "+node['node']
    else:
        col.remove({ 'node' : args.puppet_node})

if __name__ == "__main__":
    main()
