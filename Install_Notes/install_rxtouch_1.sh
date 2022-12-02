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
sudo ap -y upgrade
sudo apt -y full-upgrade
sudo rpi-eeprom-update -a

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

