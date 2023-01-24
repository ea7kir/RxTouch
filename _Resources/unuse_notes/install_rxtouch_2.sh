#!/bin/bash

"""
RxTouch installer by EA7KIR Michael Naylor 2022-11-15

NOTE: CURRENTLY REQUIRES PIOS BULLSEYE 64-BIT FULL DESKTOP VERSION

Using Raspberry Pi Imager:
CHOOSE OS:	Raspberry Pi OS (64-bit)
CONFIGURE:
	Set hostname:			rxtouch
	Enable SSH
		Use password authentication
	Set username and password
		Username:			pi
		Password: 			<password>
	Set locale settings
		Time zone:			<Europe/Madrid>
		Keyboard layout:	<us>
	Eject media when finished
SAVE and WRITE

Insert car and login, wait until the software update icon to appear,
then proceed with updates and reboot.

Login and copy this file to the Raspberry Pi and execute.

"""

#sudo apt update
#sudo apt upgrade
#reboot

echo
echo "-------------------------------"
echo "----- Installing pyenv ---------"
echo "-------------------------------"
echo

sudo apt-get update; sudo apt-get install make build-essential libssl-dev zlib1g-dev \
libbz2-dev libreadline-dev libsqlite3-dev wget curl llvm \
libncursesw5-dev xz-utils tk-dev libxml2-dev libxmlsec1-dev libffi-dev liblzma-dev

git clone https://github.com/pyenv/pyenv.git ~/.pyenv
echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.bashrc
echo 'export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.bashrc
echo -e 'if command -v pyenv 1>/dev/null 2>&1; then\n eval "$(pyenv init --path)"\nfi' >> ~/.bashrc
exec $SHELL

echo
echo "-------------------------------"
echo "----- Installing Python3.11.0--"
echo "-------------------------------"
echo

pyenv install 3.11.0

echo
echo "-------------------------------"
echo "----- Setting env to 3.11.0----"
echo "-------------------------------"
echo

pyenv globall 3.11.0

echo
echo "-------------------------------"
echo "----- Upgrading pip -----------"
echo "-------------------------------"
echo

pip install --upgrade pip

echo
echo "-------------------------------"
echo "----- Installing PySimpleGUI --"
echo "-------------------------------"
echo

pip install pysimplegui

echo
echo "-------------------------------"
echo "----- Preparing for RxTouch ---"
echo "-------------------------------"
echo

cd
mkdir RxTouch

echo
echo "-------------------------------"
echo "----- Installing LongMynd -----"
echo "-------------------------------"
echo

sudo apt -y install make gcc libusb-1.0-0-dev libasound2-dev

cd RxTouch
wget https://github.com/BritishAmateurTelevisionClub/longmynd/archive/refs/heads/master.zip
unzip master.zip
rm master.zip
mv longmynd-master longmynd
cd longmynd
echo "IT'S NOW NECCESSARY TO COMMENT LINE 22 IN THE Makfile"
exit

make
mkfifo longmynd_main_status
cd


echo
echo "-----------------------------# --"
echo "----- Installing More -----"
echo "----------------------------"
echo

#sudo apt -y install git
#sudo apt -y install cmake
#sudo apt -y install libusb-1.0-0-dev
#sudo apt -y install vlc
#sudo apt -y install libasound2-dev
#sudo apt -y install ir-keytable
#sudo apt -y install python3-dev
#sudo apt -y install python3-pip
#sudo apt -y install python3-yaml
#sudo apt -y install python3-pygame
#sudo apt -y install python3-vlc
#sudo apt -y install python3-evdev
#sudo apt -y install python3-pil
#sudo apt -y install python3-gpiozero
#sudo apt -y install libfftw3-dev libjpeg-dev  # for DVB-T
#sudo apt -y install fbi netcat imagemagick    # for DVB-T
#sudo apt -y install python3-urwid             # for Ryde Utils
#sudo apt -y install python3-librtmp           # for Stream RX
#sudo apt -y install vlc-plugin-base           # for Stream RX
