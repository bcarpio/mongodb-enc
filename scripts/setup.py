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
import sys, os
from ConfigParser import SafeConfigParser
import argparse


def main():
    """ This script creates the default node definition """

    parser = SafeConfigParser()
    config = os.path.join(os.path.dirname(__file__),"../conf/conf.ini")
    parser.read(config)
    database = parser.get('mongodb_info', 'mongodb_db_name')
    collection = parser.get('mongodb_info', 'mongodb_collection_name')
    host = parser.get('mongodb_info', 'mongodb_servers')

    con = Connection(host)
    col = con[database][collection]

    cmd_parser = argparse.ArgumentParser(description='Add Default Node To Mongodb ENC')
    cmd_parser.add_argument('-a', '--action', dest='puppet_action', choices=['append', 'new'], help='Append Or Recreate Default Node', required=True)
    cmd_parser.add_argument('-c', '--class', dest='puppet_classes', help='Can specify multiple classes each with -c', action='append', required=True)
    args = cmd_parser.parse_args()


    c = {}
    col.ensure_index('node', unique=True)

    for pclass in args.puppet_classes:
        c[pclass] = ''

    if args.puppet_action == 'append':
        d = { 'node' : 'default', 'enc' : { 'classes': c }}
        check = col.find_one({ 'node' : 'default' }, {'node': 1})
        if not check:
            print "Default Node Doesn't Exist, Please Add It First"
            sys.exit(1)
        ec = col.find_one({ 'node' : 'default'})
        ec['enc']['classes'].update(c)
        col.remove({ 'node' : 'default'})
        col.insert(ec)

    if args.puppet_action == 'new':
        d = { 'node' : 'default', 'enc' : { 'classes': c }}
        check = col.find_one({ 'node' : 'default' }, {'node': 1})
        if check:
            col.remove({ 'node' : 'default'})
        col.insert(d)

if __name__ == "__main__":
    main()
