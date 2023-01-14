import random # ONLY NEEDED TO SIMULATE DATA VALUES DURING DEVELOPMENT
from time import sleep # ONLY NEEDED TO SIMULATE FETCH TIMES DURING DEVELOPMENT

class LongmyndData:
    def __init__(self):
        self.frequency: int = 0
        self.symbol_rate: int = 0
        self.constellation: str = ''
        self.fec: str = ''
        self.codecs: str = ''
        self.db_mer: float = 0
        self.db_margin: float = 0
        self.dbm_power: int = 0
        self.null_ratio: int = 0
        self.provider: str = ''
        self.service: str = ''
        self.status_msg: str = 'xxx'
        self.longmynd_running: bool = False

MODE = [
    'Seaching',
    'Locked',
    'DVB-S',
    'DVB-S2',
]

# TODO: STOP & STARTING THE LONGMYND BINARY
# p = subprocess.run(cmd, 
# print(p.stdout)
# print(p.returncode)

import subprocess

"""
The process module allow you to spawn new processes,
connect to their input/output/error pipes, and obtain their return codes.
eg: df -h
subprocess.Popen
"""

"""
      longmynd -i 192.168.1.1 87 -r 5000 145000,146000 35,66,125
              As above but after 5000 milliseconds with no TS data the  Tuner  configuration
              will be cycled to the next of the following combinations:
               * 145 MHz, 35 Ks/s
               * 145 MHz, 66 Ks/s
               * 145 MHz, 125 Ks/s
               * 146 MHz, 35 Ks/s
               * 146 MHz, 66 Ks/s
               * 146 MHz, 125 Ks/s
               * [repeat from start]

    cd /home/pi/RxTouch/longmynd
    /home/pi/RxTouch/longmynd/longmynd -i 192.168.1.41 7777 -S 0.6 741500 1500 &
"""

def process_read_longmynd_data(longmynd2):
    longmynd_data = LongmyndData()
    while True:
        if longmynd2.poll():
            tune_args = longmynd2.recv()
            if tune_args == 'STOP':
                # NOTE: should try p1.terminate()
                args = ['/usr/bin/killall', 'longmynd']
                print(args, flush=True)
                #p2 = subprocess.run(args)
                longmynd_data.status_msg = 'longmynd has stopped'
                longmynd_data.longmynd_running = False
            else:
                # NOTE: this works, but it blocks.  Adding an & thinks it's an extra sybol rate !
                OFFSET = 9750000
                TS_IP = '192.168.1.41' # Apple TV at office.local
                TS_PORT = '7777'
                requestKHzStr = str( int(float(tune_args.frequency) * 1000 - OFFSET) )
                args = ['/home/pi/RxTouch/longmynd/longmynd', '-i ', TS_IP, TS_PORT, '-S', '0.6', requestKHzStr, tune_args.symbol_rate]
                print(args, flush=True)
                #p1 = subprocess.run(args, cwd='/home/pi/RxTouch/longmynd')
                longmynd_data.status_msg = f'{args}'
                longmynd_data.longmynd_running = True

        if longmynd_data.longmynd_running:
            sleep(1.0) # temp delay to simulate data reading
            longmynd_data.frequency = '10491.551'
            longmynd_data.symbol_rate = '1500'
            longmynd_data.mode = MODE[2]
            longmynd_data.constellation = 'QPSK'
            longmynd_data.fec = '4/5'
            longmynd_data.codecs = 'H264 MP3'
            longmynd_data.db_mer = '8.9'
            longmynd_data.db_margin = '4.1'
            longmynd_data.dbm_power = '-60'
            longmynd_data.null_ratio = random.randint(40, 60) # ONLY NEEDED TO SIMULATE DATA DURING DEVELOPMENT
            longmynd_data.provider = 'A71A'
            longmynd_data.service = 'QARS'
            #longmynd_data.status_msg = 'online'
        else:
            sleep(1.0) # temp delay to simulate data reading
            longmynd_data.frequency = '-'
            longmynd_data.symbol_rate = '-'
            longmynd_data.mode = '-'
            longmynd_data.constellation = '-'
            longmynd_data.fec = '-'
            longmynd_data.codecs = '-'
            longmynd_data.db_mer = '-'
            longmynd_data.db_margin = '-'
            longmynd_data.dbm_power = '-'
            longmynd_data.null_ratio = 0
            longmynd_data.provider = '-'
            longmynd_data.service = '-'
            #longmynd_data.status_msg = 'offline'
        longmynd2.send(longmynd_data)
    #stop()
