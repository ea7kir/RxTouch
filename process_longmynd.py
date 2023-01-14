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
        self.status_msg: str = 'status message'
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

#import subprocess
import os

"""
The process module allow you to spawn new processes,
connect to their input/output/error pipes, and obtain their return codes.
eg: df -h
subprocess.Popen
"""

def process_read_longmynd_data(longmynd2):
    longmynd_data = LongmyndData()

    def run_command(cmd):
        print(f'WILL RUN ({cmd})', flush=True)
#        p1 = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
#        out, err = p1.communicate()
#        print(f'start out: {out}', flush=True)
#        print(f'start err: {err}', flush=True)
#        if p1.returncode == 0:
#            print('start command : success', flush=True)
#        else:
#            print('start command : failed', flush=True)
        longmynd_data.longmynd_running = True
        result = os.system(cmd)
        print(f'result = {result}', flush=True)

    def stop_longmynd():
        if not longmynd_data.longmynd_running:
            return
        print('WILL STOP')
        cmd = '/usr/bin/killall longmynd'
#        p2 = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
#        out, err = p2.communicate()
#        print(f'stop out: {out}', flush=True)
#        print(f'stop err: {err}', flush=True)
#        if p2.returncode == 0:
#            print('stop command : success', flush=True)
#        else:
#            print('stop command : failed', flush=True)
#        longmynd_data.status_msg = 'longmynd has stopped'
        run_command(cmd)
        longmynd_data.longmynd_running = False
        #print(longmynd_data.status_msg, flush=True)

    # cd /home/pi/RxTouch/longmynd
    # /home/pi/RxTouch/longmynd/longmynd -i 192.168.1.41 7777 -S 0.6 741500 1500 &

    def start_longmynd(frequency, rate_list):
        print('WILL START')
        stop_longmynd()
        # assemble the command line arguments
        # params = ["-i", TS_IP, TS_Port, "-S", "0.6", requestKHzStr, allSrs]
        OFFSET = 9750000
        TS_IP = '192.168.1.41' # Apple TV at office.local
        TS_PORT = '7777'
        requestKHzStr = str(float(frequency) * 1000 - OFFSET)
        params = ['-i ', TS_IP, TS_PORT, '-S', '0.6', requestKHzStr, rate_list]
        cmd = f'cd /home/pi/RxTouch/longmynd; ./longmynd -i {TS_IP} {TS_PORT} -S 0.6 {requestKHzStr} {rate_list}'
        run_command(cmd)
        longmynd_data.status_msg = f'longmynd is running : {cmd}'
        longmynd_data.longmynd_running = True
        #print(longmynd_data.status_msg, flush=True)

    #longmynd_data.longmynd_running = True # TEMP for testing

    while True:
        sleep(1.0) # temp delay to simulate data reading
        if longmynd2.poll():
            tune_args = longmynd2.recv()
            if tune_args == 'STOP':
                stop_longmynd() 
            else:
                start_longmynd(tune_args.frequency, tune_args.symbol_rate)
        if longmynd_data.longmynd_running:
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
            longmynd_data.status_msg = 'online'
        else:
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
            longmynd_data.status_msg = 'offline'
        longmynd2.send(longmynd_data)
    stop()
