#!/bin/bash

echo "Installing RxTouch Part 1"

echo
echo "-------------------------------"
echo "-- Updateing the OS"
echo "-------------------------------"
echo

sudo apt update; sudo apt -y full-upgrade
#sudo apt update
#sudo apt full-upgrade -y
sudo apt autoremove -y
sudo apt clean

echo
echo "-------------------------------"
echo "-- Updating eeprom firmware"
echo "-------------------------------"
echo

sudo rpi-eeprom-update -a

echo
echo "-------------------------------"
echo "-- Rebooting in 5 seconds"
echo "--"
echo "-- Then run install_2.sh"
echo "-------------------------------"
echo

sleep 5

sudo reboot
