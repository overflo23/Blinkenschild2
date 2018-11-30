#!/bin/bash

BASEPATH="/home/pi/Blinkenschild2"

echo "SHOWING TWEET: $1"

cd $BASEPATH/bin

sudo ./twitter.py --led-rows=16 --led-cols=32 --led-chain=2  --led-parallel=3 --led-brightness=50 --led-multiplexing=0  -t "$1"

