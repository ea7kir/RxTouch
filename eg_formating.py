# gui_formatting.py

def frequency(kHz: int) -> str:
    if kHz > 0:
        return '{:09.3f}'.format(kHz / 1000)
    return '-----.---'

def symbol_rate(kHz: int) -> str:
    if kHz > 0:
        return kHz
    return '-'

def mode(m: str) -> str:
    if m:
        return m
    return '-'

def constellation(m: str) -> str:
    if m:
        return m
    return '-'

def fec(m: str) -> str:
    if m:
        return m
    return '-/-'

def codecs(m: str) -> str:
    if m:
        return m
    return '-'

def codecs_va(video: str, audio: str) -> str:
    a = '-'
    v = '-'
    if video: v = video
    if audio: a = audio
    return '{} {}'.format(v, a)

def db_mer(m: str) -> str:
    if m:
        return m
    return '-.-'

def db_margin(m: str) -> str:
    if m:
        return m
    return 'D -.-'

def dbm_power(m: str) -> str:
    if m:
        return m
    return '-'

def provider(m: str) -> str:
    if m:
        return m
    return '-'

def service(m: str) -> str:
    if m:
        return m
    return '-'
