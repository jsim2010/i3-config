#!/bin/sh

xrandr --output eDP1 --primary --mode 1920x1080
xrandr --output DP1-2 --mode 1920x1080
xrandr --output DP1-1 --mode 1920x1080 --rotate right
xrandr --output DP1-2 --pos 1080x286
xrandr --output eDP1 --pos 1080x1366
