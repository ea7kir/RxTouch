FREQUENCY = '-----.---'
SYMBOL_RATE = '-'
MODE = '-'
CONSTELLATION = '-'
FEC = '-/-'
CODEC = '-'
CODECS = '- -'
DB_MER = '-.-'
DB_MARGIN = 'D -.-'
DBM_POWER = '---'
PROVIDER = '-'
SERVICE = '-'
DRIVE = '-'

def frequency(kHz: int) -> str:
    if kHz > 0:
        return '{:09.3f}'.format(kHz / 1000)
    return FREQUENCY

def symbol_rate(kHz: int) -> str:
    if kHz > 0:
        return kHz
    return SYMBOL_RATE

def mode(m: str) -> str:
    if m:
        return m
    return MODE

def constellation(m: str) -> str:
    if m:
        return m
    return CONSTELLATION

def fec(m: str) -> str:
    if m:
        return m
    return FEC

def codecs(m: str) -> str:
    if m:
        return m
    return CODECS

def codecs_va(video: str, audio: str) -> str:
    a = None
    v = None
    if video:
        v = video
    else:
        v = CODEC
    if audio:
        a = audio
    else:
        a = CODEC
    return '{} {}'.format(v, a)

def db_mer(m: str) -> str:
    if m:
        return m
    return MODE

def db_margin(m: str) -> str:
    if m:
        return m
    return MODE

def dbm_power(m: str) -> str:
    if m:
        return m
    return MODE

def provider(m: str) -> str:
    if m:
        return m
    return MODE

def service(m: str) -> str:
    if m:
        return m
    return MODE
