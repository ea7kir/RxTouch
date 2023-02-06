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
echo "-- Install xinit"
echo "-------------------------------"
echo

sudo apt install xinit
sudo apt autoremove

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
echo "Compile longmynd"
echo "# cd RxTouch/longmynd"
echo "# make"
echo "# mkfifo longmynd_main_status"
echo "# mkfifo longmynd_main_ts"
echo "# cd .."
echo
echo "To run RxTouch, type: ./rxtouch"

