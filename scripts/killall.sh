#!/bin/bash

sudo killall -9 led-scrolltext
sudo killall -9 led-video
sudo killall -9 led-image-viewer


sudo kill -9 `ps ax | grep twitter.py | grep python | cut -f 2 -d " "`
