# longmynd_manager.py

import random # ONLY NEEDED TO SIMULATE DATA DURING DEVELOPMENT

#from dataclasses import dataclass

#@dataclass
#class LmStatus:
#    frequency: int = 0
#    symbol_rate: int = 0
#    constellation: str = ''
#    fec: str = ''
#    codecs: str = ''
#    db_mer: float = 0
#    db_margin: float = 0
#    dbm_power: int = 0
#    null_ratio: int = 0
#    provider: str = ''
#    service: str = ''

MODE = [
    'Seaching',
    'Locked',
    'DVB-S',
    'DVB-S2',
]

class LongmyndManager():
    def __init__(self):
        self.running = False
#        self.status_available = True
#        self.frequency: int = 0
#        self.symbol_rate: int = 0
#        self.constellation: str = ''
#        self.fec: str = ''
#        self.codecs: str = ''
#        self.db_mer: float = 0
#        self.db_margin: float = 0
#        self.dbm_power: int = 0
#        self.null_ratio: int = 0
#        self.provider: str = ''
#        self.service: str = ''
        self.read_status()
        self.status_msg: str = ''

    def start_longmynd(self, frequency, rate_list):
        if self.running:
            self.stop_longmynd
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
        self.running = True
        self.status_msg = '{0}'.format(params)

    def stop_longmynd(self):
        if not self.running:
            return
        self.status_msg = 'stopping longmynd'
        self.running = False
        #time.sleep(2)
        self.status_msg = 'longmynd stopped'

    def read_status(self): # THIS IS A DUMMY READ, PENDING GETTING longmynd WORKING !
        if self.running:
            self.frequency = '10491.551'
            self.symbol_rate = '1500'
            self.mode = MODE[0]
            self.constellation = 'QPSK'
            self.fec = '4/5'
            self.codecs = 'H264 MP3'
            self.db_mer = '8.9'
            self.db_margin = '4.1'
            self.dbm_power = '-60'
            self.null_ratio = random.randint(40, 60) # ONLY NEEDED TO SIMULATE DATA DURING DEVELOPMENT
            self.provider = 'A71A'
            self.service = 'QARS'
        else:
            self.frequency = '-'
            self.symbol_rate = '-'
            self.mode = '-'
            self.constellation = '-'
            self.fec = '-'
            self.codecs = '-'
            self.db_mer = '-'
            self.db_margin = '-'
            self.dbm_power = '-'
            self.null_ratio = 0
            self.provider = '-'
            self.service = '-'
  

longmynd_manager = LongmyndManager()