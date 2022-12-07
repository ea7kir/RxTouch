# lm_functions.py

from dataclasses import dataclass

@dataclass
class LmStatus:
    frequency: int = 0
    symbol_rate: int = 0
    constellation: str = ''
    fec: str = ''
    codecs: str = ''
    db_mer: float = 0
    db_margin: float = 0
    dbm_power: int = 0
    provider: str = ''
    service: str = ''

def reset_lmstatus():
    frequency = 0
    symbol_rate = 0
    constellation = ''
    fec = ''
    codecs = ''
    db_mer = 0
    db_margin = 0
    dbm_power = 0
    provider = ''
    service = ''

lm_status = LmStatus()

lm_status_available = True

def read_lm_status() -> LmStatus:
    lm_status.frequency = 10491551
    lm_status.symbol_rate = 1500
    lm_status.mode = 'Locked DVB-S2'
    lm_status.constellation = 'QPSK'
    lm_status.fec = '4/5'
    lm_status.codecs = 'H264 MP3'
    lm_status.db_mer = 78.9
    lm_status.db_margin = 4.1
    lm_status.dbm_power = -60
    lm_status.provider = 'A71A'
    lm_status.service = 'QARS'
    return lm_status

longmynd_running = False

def read_longmynd_ts() -> str:
    msg = ''
    
    return msg

def stop_longmynd():
    global longmynd_running
    if not longmynd_running:
        return
    print('stopping longmynd')
    longmynd_running = False
    print('longmynd stopped')

def start_longmynd(frequency, symbol_rates):
    global longmynd_running
    if longmynd_running:
        stop_longmynd
    # TODO: execute longmynd with args
    print('starting longmynd')
    longmynd_running = True
    print('longmynd running')


