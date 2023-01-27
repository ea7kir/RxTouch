# Installing Pi OS

NOTE: CURRENTLY REQUIRES PIOS BULLSEYE 64-BIT FULL DESKTOP

## Using Raspberry Pi Imager:

```
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
```

Insert the card and login. Wait for the software update icon to appear, and proceed to update and reboot.

## Login

Clone the repro.

```
cd
git clone https://github.com/ea7kir/RxTouch.git
```

Change permissions for the 3 install scrpits.

```
chmod +x RxTouch/_Resources/install_*
```

Exeute the 3 install scrpits in order.

```
./RxTouch/_Resources/install_1.sh
./RxTouch/_Resources/install_2.sh
./RxTouch/_Resources/install_3.sh
```
