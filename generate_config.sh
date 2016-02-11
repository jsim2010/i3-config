#!/bin/bash
LOCAL_CONFIG=$HOME/.config/i3/config.local

if [ ! -f $LOCAL_CONFIG ]; then
    touch $LOCAL_CONFIG
fi

cat $LOCAL_CONFIG $HOME/.config/i3/config.base > $HOME/.config/i3/config
