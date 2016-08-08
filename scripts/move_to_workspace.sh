#!/bin/bash

WORKSPACE=$($HOME/.config/i3/scripts/get_workspaces.py | dmenu)
i3-msg move container to workspace $WORKSPACE
i3-msg workspace $WORKSPACE
