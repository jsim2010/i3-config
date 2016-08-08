#!/bin/bash

current=$(synclient -l | grep "TouchpadOff" | cut -d = -f 2)
if [ $current -eq 0 ] ; then
    synclient TouchpadOff=1
else
    synclient TouchpadOff=0
fi
