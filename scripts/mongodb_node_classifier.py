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
import yaml
import sys
import config

def main():
    """ This script is called by puppet  """
    if (len(sys.argv) < 2):
        print "ERROR: Please Supply A Hostname or FQDN"
        sys.exit(1)

    col = config.main()

    # Probably want to remove this. This is because I don't use FQDNs in my current puppet manifest. 
    # also made this easier for me to test.
    node = sys.argv[1]
    #node = node.split('.')[0]

    # Find the node given at a command line argument
    d = col.find_one({"node": node}) 
    if d == None:
        print "ERROR: Node "+node+" Not Found In ENC" 
        sys.exit(1)

    # Check if the node requiers inheritance
    n = col.find_one({"node": node})
    if 'inherit' in n:
        i = True
        while i == True:
            inode = n['inherit']
            if not col.find_one({"node" : inode}):
                print "ERROR: Inheritance Node "+inode+" Not Found In ENC"
                sys.exit(1)
            idict = col.find_one({"node": inode})
            if 'classes' in idict['enc']:
                iclass = idict['enc']['classes']
                if 'classes' in n['enc']:
                    d['enc']['classes'].update(iclass)
                else:
                    d['enc']['classes'] = iclass 
            n = col.find_one({"node": inode})
            if 'inherit' not in n:
                i = False

    print yaml.safe_dump(d['enc'], default_flow_style=False)


if __name__ == "__main__":
    main()
