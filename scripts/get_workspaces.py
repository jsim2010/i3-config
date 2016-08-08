#!/usr/bin/env python

import i3ipc

i3 = i3ipc.Connection()
tree = i3.get_tree()

for w in tree.workspaces():
    print(w.name)
