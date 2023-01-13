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

def process_read_longmynd_data(send_longmynd_data):
    longmynd_data = LongmyndData()

    def stop():
        if not longmynd_data.longmynd_running:
            return
        longmynd_data.status_msg = 'longmynd not running'
        longmynd_data.longmynd_running = False

    def start(frequency, rate_list):
        stop_longmynd()
        # assemble the command line arguments
        # params = ["-i", TS_IP, TS_Port, "-S", "0.6", requestKHzStr, allSrs]
        OFFSET = 9750000
        TS_IP = '192.168.1.36'
        TS_PORT = '7777'
        requestKHzStr = str(float(frequency) * 1000 - OFFSET)
        allSrs = rate_list[0]
        for i in range(1, len(rate_list)):
            allSrs += f',{rate_list[i]}'
        params = ['-i ', TS_IP, TS_PORT, '-S', '0.6', requestKHzStr, allSrs]
        # TODO: execute longmynd with args see: https://youtu.be/VlfLqG_qjx0
        #time.sleep(2)
        longmynd_data.status_msg = 'longmynd is running'
        longmynd_data.longmynd_running = True

    longmynd_data.longmynd_running = True # TEMP for testing

    while True:
        sleep(1.0) # temp delay to simulate data reading
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
        send_longmynd_data.send(longmynd_data)
    stop()
