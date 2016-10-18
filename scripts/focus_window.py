#!/usr/bin/env python

import i3ipc
from sys import exit
from sys import argv
from subprocess import check_output

i3 = i3ipc.Connection()
tree = i3.get_tree()


def get_visible_workspace_names():
    visible_workspace_names = []

    for output in i3.get_outputs():
        if output.active:
            visible_workspace_names.append(output.current_workspace)

    return visible_workspace_names


def is_window_visible(window):
    if window.window is not None:
        command = ['xprop', '-id', str(window.window)]
        xprop = check_output(command).decode(encoding='UTF-8')

        return '_NET_WM_STATE_HIDDEN' not in xprop

    return False


def get_visible_window_ids():
    visible_window_ids = []

    for workspace in tree.workspaces():
        if workspace.name in visible_workspace_names:
            for window in workspace.descendents():
                if is_window_visible(window):
                    visible_window_ids.append(window.id)

    return visible_window_ids


if (len(argv) < 2):
    print "ERROR: %s was not provided 1 argument." % argv[0]
    exit(1)

sibling_commands = ["next", "prev"]
visible_commands = ["down", "up"]

if argv[1] in sibling_commands:
    focused_window = tree.find_focused()
    siblings = focused_window.parent.descendents()
    index = siblings.index(focused_window)
    new_index = -1

    if argv[1] == "next" and (index + 1) != len(siblings):
        # focused_window is not the last sibling
        new_index = index + 1
    elif argv[1] == "prev" and index != 0:
        # focused_window is not the first sibling
        new_index = index - 1

    if new_index != -1:
        i3.command('[con_id=%s] focus' % siblings[new_index].id)
elif argv[1] in visible_commands:
    visible_workspace_names = get_visible_workspace_names()
    visible_window_ids = get_visible_window_ids()
    command = "focus %s" % argv[1]
    original_window = tree.find_focused()

    i3.command(command)
    # Must refresh i3ipc connection after command to find new focused_window.
    focused_window = i3ipc.Connection().get_tree().find_focused()

    while focused_window.id not in visible_window_ids:
        i3.command(command)
        focused_window = i3ipc.Connection().get_tree().find_focused()

    # We might have hidden original_window, so make it visible again before
    # focusing directly to focused_window
    i3.command('[con_id=%s] focus' % original_window.id)
    i3.command('[con_id=%s] focus' % focused_window.id)
else:
    print "ERROR: Usage is incorrect."
    print "  %s<dir>" % argv[0]
    print "    <dir> = 'up' or 'down'"
    exit(1)
