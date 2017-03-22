#!/bin/bash

if [ -f /usr/local/bin/hyper ]; then
    hyper term://bash
else
    xterm
fi
