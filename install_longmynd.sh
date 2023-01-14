#!/bin/bash

sudo apt-get install make gcc libusb-1.0-0-dev libasound2-dev

cd /home/pi/RxTouch/longmynd

make

mkfifo longmynd_main_status

mkfifo longmynd_main_ts
