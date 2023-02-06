#!/bin/bash

# to copy this file from Mac to Rpi, type
# scp install_3.sh pi@rxtouch.local/install_3.sh

echo "Installing RxTouch Part 3"

echo
echo "-------------------------------"
echo "-- Installing Python 3.11.1"
echo "--"
echo "-- this will take some time..."
echo "-------------------------------"
echo

pyenv install 3.11.1

echo
echo "-------------------------------"
echo "-- Setting env to Python 3.11.1"
echo "-------------------------------"
echo

pyenv global 3.11.1
pyenv versions

echo
echo "-------------------------------"
echo "-- Updrading PIP"
echo "-------------------------------"
echo

pip install --upgrade pip

echo
echo "-------------------------------"
echo "-- Installing PySimpleGUI, websockets & PyYAML"
echo "-------------------------------"
echo

pip install pysimplegui websockets PyYAML

echo
echo "-------------------------------"
echo "-- Install longmynd dependences"
echo "-------------------------------"
echo

sudo apt -y install make gcc libusb-1.0-0-dev libasound2-dev

echo
echo "-------------------------------"
echo "-- Install xinit"
echo "-------------------------------"
echo

sudo apt install xinit
sudo apt autoremove

echo "Suggested packages: (not installed)"
echo "xfonts-100dpi | xfonts-75dpi xfonts-scalable xinput firmware-amd-graphics xserver-xorg-video-r128 xserver-xorg-video-mach64"

echo
echo "-------------------------------"
echo "-- Done"
echo "-------------------------------"
echo

echo "To run RxTouch from my Mac,"
echo "edit /etc/X11/Xwrapper.config"
echo "and change allowed_users = console to allowed_users = anybody"
echo
echo "Clone TxTouch from within VSCODE"
echo "using: https://github.com/ea7kir/RxTouch.git"
echo
echo "NOTE: currently using longmynd BATC version. Eg:"
echo "cd /home/pi/RxTouch"
echo "wget https://github.com/BritishAmateurTelevisionClub/longmynd/archive/refs/heads/master.zip"
echo "unzip master.zip"
echo "rm master.zip"
echo "mv longmynd-master longmynd"
echo "COMMENT LINE 22 IN THE Makefile"
echo
echo "Compile longmynd"
echo "# cd RxTouch/longmynd"
echo "# make"
echo "# mkfifo longmynd_main_status"
echo "# mkfifo longmynd_main_ts"
echo "# cd .."
echo
echo "To run RxTouch, type: ./rxtouch"

