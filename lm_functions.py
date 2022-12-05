# lm_functions.py

def lm_data_dict() -> dict:
    lm_frequency = 10491551
    lm_symbol_rate = 1500
    lm_mode = 'Locked DVB-S2'
    lm_constellation = 'QPSK'
    lm_fec = '4/5'
    lm_codecs = 'H264 MP3'
    lm_db_mer = 78.9
    lm_db_margin = 4.1
    lm_dbm_power = -60
    lm_provider = 'A71A'
    lm_service = 'QARS'
    new_dict = {
        '-FREQUENCY-': lm_frequency,
        '-SYMBOL_RATE-': lm_symbol_rate,
        '-MODE-': lm_mode,
        '-CONSTELLATION-': lm_constellation,
        '-FEC-': lm_fec,
        '-CODECS-': lm_codecs,
        '-DB_MER-': lm_db_mer,
        '-DB_MARGIN-': lm_db_margin,
        '-DBM_POWER-': lm_dbm_power,
        '-PROVIDER-': lm_provider,
        '-SERVICE-': lm_service,
    }
    return new_dict

