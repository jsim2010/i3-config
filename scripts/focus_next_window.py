#!/usr/bin/env python

import i3ipc
import sys

if (len(sys.argv) < 2):
    print "ERROR: %s was not provided 1 argument." % sys.argv[0]
    sys.exit(1)

i3 = i3ipc.Connection()
focused = i3.get_tree().find_focused()
siblings = focused.parent.descendents()
index = siblings.index(focused)
new_index = 0

if sys.argv[1] == "down":
    if (index + 1) != len(siblings):
        new_index = index + 1
elif sys.argv[1] == "up":
    if index == 0:
        new_index = len(siblings)
    else:
        new_index = index - 1
else:
    print "ERROR: Usage is incorrect."
    print "  %s<dir>" % sys.argv[0]
    print "    <dir> = 'up' or 'down'"
    sys.exit(1)

i3.command('[con_id=%s] focus' % siblings[new_index].id)
