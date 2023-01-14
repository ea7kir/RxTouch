## Download the Longmynd Code to the Mac.

From `https://github.com/BritishAmateurTelevisionClub/longmynd`

Rename it from `longmynd-master` to `longmynd` and copy it to the Pi.

### Dependencies

```
sudo apt-get install make gcc libusb-1.0-0-dev libasound2-dev
```


To run longmynd without requiring root, unplug the minitiouner and then install the udev rules file with:
```
cd longmynd
sudo cp minitiouner.rules /etc/udev/rules.d/
```

### Compile Longmynd

First, edit the `Makefile` and comment the line `COPT_RPI34 = -mfpu=neon-fp-armv8` as it's not required on arm64.

```
cd ~/longmynd
nano Makefile
```

then

```
make
```

Then read the `~/longmynd/README.md` instructions and `man -l longmynd.1`

### FIFO and LAN

SatReceiver needs to read the Minitiouner status, so create a FIFO.

```
mkfifo longmynd_main_status
```

However, we need the video stream to be accessible over tha LAN.

With a few more options, this also outputs the Status Information on UDP to localhost on port 4002 (`-I 127.0.0.1 4002`), MPEG Transport Stream on UDP to another machine (192.168.2.34) on port 4003 (`-i 192.168.2.34 4003`), and selects the other (Bottom) NIM input socket (`-w`).

So, for example, run with the `'` flag.

```
./longmynd -i 192.168.2.34 4003 -w -p v 1296500 2000
```

A video player (e.g. VLC) can be set to listen for the incoming MPEG-TS UDP, on localhost or another machine on the network with: `vlc udp://@:4003`

