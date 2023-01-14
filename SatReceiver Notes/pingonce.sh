#!/bin/bash

# usage: pingonce.sh office.local
# returns: a valid IP4 Address or not
TXT=$(/usr/bin/ping -c1 $1)
A=${TXT#*(}
B=${A%%)*}
echo -n $B
