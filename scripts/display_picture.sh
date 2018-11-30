#!/bin/bash


BASEPATH="/home/pi/Blinkenschild2"

echo "SHOWING PICS WITH SUDO: $1"


sudo $BASEPATH/bin/led-image-viewer --led-rows=16 --led-cols=32 --led-chain=2  --led-parallel=3 --led-brightness=100 --led-multiplexing=0  -C $BASEPATH/Flask/$1
