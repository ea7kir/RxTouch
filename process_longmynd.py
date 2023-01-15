import subprocess

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

"""
Example to receive the beacon:
cd /home/pi/RxTouch/longmynd
/home/pi/RxTouch/longmynd/longmynd -i 192.168.1.41 7777 -S 0.6 741500 1500 &
"""

def process_read_longmynd_data(longmynd2):
    LM_STOP_START_SCRIPT = '/home/pi/RxTouch/lm_stopstart'
    LM_STOP_SCRIPT = '/home/pi/RxTouch/lm_stop'
    LM_STATUS_PIPE  = '/home/pi/RxTouch/longmynd/longmynd_main_status'
    longmynd_data = LongmyndData()
    while True:
        if longmynd2.poll():
            tune_args = longmynd2.recv()
            if tune_args == 'STOP':
                args = LM_STOP_SCRIPT
                print(args, flush=True)
                p2 = subprocess.run(args)
                longmynd_data.status_msg = 'longmynd has stopped'
                longmynd_data.longmynd_running = False
            else:
                OFFSET = 9750000
                TS_IP = '192.168.1.41' # Apple TV at office.local
                TS_PORT = '7777'
                requestKHzStr = str( int(float(tune_args.frequency) * 1000 - OFFSET) )
                args = [LM_STOP_START_SCRIPT, '-i ', TS_IP, TS_PORT, '-S', '0.6', requestKHzStr, tune_args.symbol_rate]
                p1 = subprocess.run(args) #, cwd='/home/pi/RxTouch/longmynd')
                longmynd_data.status_msg = f'tuned: {requestKHzStr}, {tune_args.symbol_rate}'
                longmynd_data.longmynd_running = True

        if longmynd_data.longmynd_running:
            # read LM_STATUS_PIPE
            sleep(0.5) # temp delay to simulate data reading
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
        else:
            sleep(0.5) # temp delay to simulate data reading
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
        longmynd2.send(longmynd_data)
