#!/bin/bash

i3-msg workspace $($HOME/.config/i3/scripts/get_workspaces.py | dmenu)
