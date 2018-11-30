#!/bin/bash


BASEPATH="/home/pi/Blinkenschild2"

echo "SHOWING TEXT  SUDO: $1 $2"



sudo $BASEPATH/bin/./led-scrolltext  --led-rows=16 --led-cols=32 --led-chain=2  --led-parallel=3 --led-brightness=100 --led-multiplexing=0  -y 12 -f $BASEPATH/bin/fonts/9x18B.bdf -C $2  -O $3 -S 2 $1 
