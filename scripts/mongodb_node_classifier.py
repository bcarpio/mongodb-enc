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
from pymongo.read_preferences import ReadPreference


def parse_input(input):
    if len(input) < 2:
        print "ERROR: Please Supply a Hostname or FQDN"
        sys.exit(1)


def find_node(conf, node):
    node_info = conf.find_one(
        {"node": node},
        read_preference=ReadPreference.PRIMARY
    )
    if node_info is None:
        print "ERROR: Node "+node+" Not Found In ENC"
        sys.exit(1)

    return node_info


def merge_dict(a, b, path=None):
    # Merges b into a, in case of conflict, b wins
    if path is None: path = []
    for key in b:
        if key in a:
            if isinstance(a[key], dict) and isinstance(b[key], dict):
                # Merges dict keys recursively
                merge_dict(a[key], b[key], path + [str(key)])
            elif a[key] == b[key]:
                # Leaves a[key] set if values are identical
                pass
            else:
                # Takes the value for b[key] in case of conflict
                a[key] = b[key] 
        else:
            # If key is not already in a, adds it
            a[key] = b[key]
    return a


def main():
    """ This script is called by puppet  """

    parse_input(sys.argv)
    conf = config.main()

    # This is because we don't use FQDNs in our current puppet manifests
    # Probably want to remove this
    node = (sys.argv[1]).split('.')[0]

    # Finds the input node
    node_info = find_node(conf, node)

    # Default the final_node_info to the input node
    final_node_info = node_info

    # Check if the input node has inheritance set
    if 'inherit' in node_info:
        inheritance = True

        while inheritance:
            # Finds the node being inherited from
            inherit_node_info = find_node(conf, node_info['inherit'])

            # Updates the final node enc info by merging inherited and final node enc info recursively
            final_node_info['enc'] = merge_dict(inherit_node_info['enc'], final_node_info['enc'])

            # Sets the node_info to the inherited node, to recurse through the inherited node's inheritance
            node_info = find_node(conf, node_info['inherit'])

            # Breaks out of while once a node with no inheritance is found
            if 'inherit' not in node_info:
                inheritance = False

    print yaml.safe_dump(final_node_info['enc'], default_flow_style=False)


if __name__ == "__main__":
    main()
