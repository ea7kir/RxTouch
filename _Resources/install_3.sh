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
echo "-- Cloning RxTouch from github"
echo "-------------------------------"
echo

echo "THIS IS NOT WORKING YET"
# git clone https://github.com/ea7kir/RxTouch.git

echo
echo "-------------------------------"
echo "-- Compiling longmynd"
echo "-------------------------------"
echo

echo "THIS CAN'T BE DONE UNTIL WE'VE CLONED'"
# cd RxTouch/longmynd
# make
# mkfifo longmynd_main_status
# mkfifo longmynd_main_ts
# cd

echo
echo "-------------------------------"
echo "-- Done"
echo "-------------------------------"
echo

echo "Clone from VSCODE and make longmynd manually"
