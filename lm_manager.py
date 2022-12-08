# lm_manager.py

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
#    provider: str = ''
#    service: str = ''

class LmManager():
    def __init__(self):
        self.running = False
        self.status_available = True
        self.frequency: int = 0
        self.symbol_rate: int = 0
        self.constellation: str = ''
        self.fec: str = ''
        self.codecs: str = ''
        self.db_mer: float = 0
        self.db_margin: float = 0
        self.dbm_power: int = 0
        self.provider: str = ''
        self.service: str = ''

    def start_longmynd(self, frequency, rate_list):
        if self.running:
            self.stop_longmynd
        # assemble the command line arguments
        args = '-i '
        args += frequency
        for sr in rate_list:
            args += f' {sr}'

        # TODO: execute longmynd with args

        self.running = True
        print('longmynd running with args: ', args)

    def stop_longmynd(self):
        if not self.running:
            return
        print('stopping longmynd')
        self.running = False
        print('longmynd stopped')

    def read_status(self): # THIS IS A DUMMY READ, PENDING GETTING longmynd WORKING !
        self.frequency = 10491551
        self.symbol_rate = 1500
        self.mode = 'Locked DVB-S2'
        self.constellation = 'QPSK'
        self.fec = '4/5'
        self.codecs = 'H264 MP3'
        self.db_mer = 78.9
        self.db_margin = 4.1
        self.dbm_power = -60
        self.provider = 'A71A'
        self.service = 'QARS'

    def _reset_status(self):
        self.frequency = 0
        self.symbol_rate = 0
        self.constellation = ''
        self.fec = ''
        self.codecs = ''
        self.db_mer = 0
        self.db_margin = 0
        self.dbm_power = 0
        self.provider = ''
        self.service = ''

    def _xxx(self):
        pass


lm_manager = LmManager()