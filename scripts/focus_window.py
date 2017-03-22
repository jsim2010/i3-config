#!/usr/bin/env python

import i3ipc
import os
import re
from neovim import attach
from subprocess import check_output
from sys import exit
from sys import argv

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


def buffer_is_term(nvim):
    return re.search(r"^term://", nvim.eval('bufname("%")'))


def prepare_new_nvim_buffer(nvim):
    if buffer_is_term(nvim) and nvim.eval('mode()') == 'n':
        nvim.input('i')


if (len(argv) < 2):
    print "ERROR: %s was not provided 1 argument." % argv[0]
    exit(1)

sibling_commands = ["next", "prev"]
visible_commands = ["down", "up", "left", "right"]
nvim_window_classes = ["NyaoVim", "Hyper", "xterm"]

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
    original_window = tree.find_focused()

    if original_window.window_class in nvim_window_classes:
        register_filename = os.environ.get("HOME") \
            + "/.config/i3/data/" + str(original_window.id)
        register_file = open(register_filename, "r")
        addr = register_file.read()
        nvim = attach("socket", path=addr)

        nvim_cmd = "wincmd "

        if argv[1] == "left":
            nvim_cmd += "h"
        elif argv[1] == "down":
            nvim_cmd += "j"
        elif argv[1] == "up":
            nvim_cmd += "k"
        elif argv[1] == "right":
            nvim_cmd += "l"

        original_nvim_winnr = nvim.eval('winnr()')
        nvim.command(nvim_cmd)

        # If we change our winnr, we focus to a new nvim window;
        # else we should see if i3 can focus to a new window.
        if original_nvim_winnr != nvim.eval('winnr()'):
            prepare_new_nvim_buffer(nvim)
            exit(1)

    visible_workspace_names = get_visible_workspace_names()
    visible_window_ids = get_visible_window_ids()
    command = "focus %s" % argv[1]

    i3.command(command)
    # Must refresh i3ipc connection after command to find new focused_window.
    focused_window = i3ipc.Connection().get_tree().find_focused()

    while focused_window.id not in visible_window_ids:
        i3.command(command)
        focused_window = i3ipc.Connection().get_tree().find_focused()

    nvim = None

    if focused_window.window_class in nvim_window_classes:
        register_filename = os.environ.get("HOME") \
            + "/.config/i3/data/" + str(focused_window.id)
        register_file = open(register_filename, "r")
        addr = register_file.read()
        nvim = attach("socket", path=addr)

    if focused_window.id != original_window.id:
        # We might have hidden original_window, so make it visible again before
        # focusing directly to focused_window
        i3.command('[con_id=%s] focus' % original_window.id)
        i3.command('[con_id=%s] focus' % focused_window.id)

        # If we changed i3 windows to a nvim window,
        # make sure we move to the correct one.
        if nvim is not None:
            nvim_cmd = "wincmd "

            # We want to make sure we are in the window farthest towards
            # the opposite direction
            if argv[1] == "left":
                nvim_cmd += "l"
            elif argv[1] == "down":
                nvim_cmd += "k"
            elif argv[1] == "up":
                nvim_cmd += "j"
            elif argv[1] == "right":
                nvim_cmd += "h"

            while True:
                original_nvim_winnr = nvim.eval('winnr()')
                nvim.command(nvim_cmd)

                if original_nvim_winnr == nvim.eval('winnr()'):
                    break

    if focused_window.window_class in nvim_window_classes:
        prepare_new_nvim_buffer(nvim)
else:
    print "ERROR: Usage is incorrect."
    print "  %s<dir>" % argv[0]
    print "    <dir> = 'up' or 'down'"
    exit(1)
