#!/usr/bin/env python

import i3ipc
import os
from sys import argv
from sys import exit

if len(argv) < 2:
    print "ERROR: not enough arguments"
    exit(1)

i3_dir = os.environ.get("HOME") + "/.config/i3"
data_dir = i3_dir + "/data"

if not os.path.isdir(data_dir):
    os.chdir(i3_dir)
    os.mkdir("data")

i3 = i3ipc.Connection()
tree = i3.get_tree()

register_file = open(data_dir + "/" + str(tree.find_focused().id), "w")
register_file.write(argv[1])
register_file.close()
