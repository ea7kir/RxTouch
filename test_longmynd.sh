# Apple TV: 192.168.1.41

#./lomgmynd -I 192.168.1.41 7777 -S 0.6 kHz allSRs

# requested_mHz = float(frequency) # where frequenct ia a string in mHz

# requested_kHz = 1000.0 * requested_mHz

# requested_kHz = int(requested_kHz - 9750000) # where offset = 9750000

# requested_kHz_str = f'{requested_kHz}'

# requested_symbol_rate = 333,500 # etc

# For the Beacon, where f = 10491.50 and sr = 1500

# 10491.50 * 1000 - 9750000 = 741500

cd /home/pi/RxTouch/longmynd
/home/pi/RxTouch/longmynd/longmynd -i 192.168.1.41 7777 -S 0.6 741500 1500 &

