#!/bin/bash

RUNNING_SINKS_INFO=$(pactl list short sinks | grep RUNNING)
SINK=${RUNNING_SINKS_INFO:0:1}
pactl set-sink-volume $SINK $1
