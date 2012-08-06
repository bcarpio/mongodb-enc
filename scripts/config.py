#!/usr/bin/python
# vim: set expandtab:
"""
**********************************************************************
GPL License
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

def main():
    """ This script adds nodes to the mongodb enc """

    parser = SafeConfigParser()
    config = os.path.join(os.path.dirname(__file__),"../conf/conf.ini")
    parser.read(config)
    database = parser.get('mongodb_info', 'mongodb_db_name')
    collection = parser.get('mongodb_info', 'mongodb_collection_name')
    host = parser.get('mongodb_info', 'mongodb_servers')
    con = Connection(host)
    col = con[database][collection]
    return col

if __name__ == "__main__":
    main()
