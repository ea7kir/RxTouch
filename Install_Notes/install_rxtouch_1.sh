#!/bin/bash

# RxTouch installer by EA7KIR Michael Naylor 2022-11-15

cd

# Check current user
whoami | grep -q pi
if [ $? != 0 ]; then
  echo "Install must be performed as user pi"
  exit
fi

echo
echo "-------------------------------"
echo "----- Updateing the OS --------"
echo "-------------------------------"
echo

sudo apt update
sudo apt -y upgrade
sudo apt -y full-upgrade
sudo rpi-eeprom-update -a

# from https://raspberrytips.com/install-latest-python-raspberry-pi/

sudo apt update
sudo apt upgrade -y
apt install wget build-essential libreadline-dev libncursesw5-dev libssl-dev libsqlite3-dev tk-dev libgdbm-dev libc6-dev libbz2-dev libffi-dev zlib1g-dev -y
wget https://www.python.org/ftp/python/3.11.0/Python-3.11.0.tar.xz
tar -xf Python-3.11.0.tar.xz
cd Python-3.11.0/
./configure --enable-optimizations
sudo make altinstall

echo
echo "--------------------------------"
echo "----- Rebooting ----------------"
echo "--------------------------------"
echo
echo "After reboot, log in again."
echo "and run ./install_rxtouch_2.sh"
echo

sleep 1
sudo reboot

