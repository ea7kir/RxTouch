""" WAITING FOR
    TODO: rewrite of calculated_dbm_power(agc_pair)
"""
import subprocess
import os

import socket # only used to find ip of apple tv

from collections import OrderedDict # for power levels
import bisect  # for power levels

from time import sleep # ONLY NEEDED TO SIMULATE FETCH TIMES DURING DEVELOPMENT

class LongmyndData:
    frequency = ''
    symbol_rate = ''
    constellation = ''
    fec = ''
    codecs = ''
    db_mer = ''
    db_margin = ''
    dbm_power = ''
    null_ratio = ''
    provider = ''
    service = ''
    status_msg = ''
    longmynd_running: bool = False

"""
Example to receive the beacon:
cd /home/pi/RxTouch/longmynd
/home/pi/RxTouch/longmynd/longmynd -i 192.168.1.41 7777 -S 0.6 741500 1500 &
"""

def process_read_longmynd_data(longmynd2):
    LM_START_SCRIPT = '/home/pi/RxTouch/lm_start'
    LM_STOP_SCRIPT = '/home/pi/RxTouch/lm_stop'
    LM_STATUS_PIPE  = '/home/pi/RxTouch/longmynd/longmynd_main_status'

    OFFSET = 9750000
    TS_IP = socket.gethostbyname('office.local') # Apple TV at office.local
    #TS_IP = '192.168.1.41' # Apple TV at office.local
    TS_PORT = '7777'

    longmynd_data = LongmyndData()

    statusFIFOfd = os.fdopen(os.open(LM_STATUS_PIPE, flags=os.O_NONBLOCK, mode=os.O_RDONLY), encoding="utf-8", errors="replace")

################################################################

    class EsPair:
        has_1st_pid = False
        has_2nd_pid = False
        the_1st_type = None
        the_2nd_type = None
        def __init__(self):
            pass
        def codec(self, type_str):
            match type_str:
                case '2': return 'MPEG-2' # TODO: too wide for display column
                case '3': return 'MP3'
                case '4': return 'MP3'
                case '15': return 'ACC'
                case '16': return 'H.263'
                case '27': return 'H.264'
                case '32': return 'MPA'
                case '36': return 'H.265'
                case '129': return 'AC3'
            return '-'
        def reset(self):
            self.has_1st_pid = False
            self.has_2nd_pid = False
            self.the_1st_type = None
            self.the_2nd_type = None

    es_pair = EsPair()
    
################################################################

    class AgcPair:
        agc1 = None
        agc2 = None
        def __init__(self):
            pass
        def reset(self):        # NOTE: not currently used
            self.agc1 = None
            self.agc2 = None

################################################################

    agc_pair = AgcPair()

################################################################

    class ModcodPair: # returns constellation, fec
        MODCOD_DVB_S = [
            ('QPSK', '1/2'), ('QPSK', '2/3'), ('QPSK', '3/4'), ('QPSK', '5/6'), ('QPSK', '7/8'),
        ]
        MODCOD_DVB_S2 = [
            ('DummyPL', 'x'), ('QPSK', '1/4'), ('QPSK', '1/3'), ('QPSK', '2/5'),
            ('QPSK', '1/2'), ('QPSK', '3/5'), ('QPSK', '2/3'), ('QPSK', '3/4'),
            ('QPSK', '4/5'), ('QPSK', '5/6'), ('QPSK', '8/9'), ('QPSK', '9/10'),
            ('8PSK', '3/5'), ('8PSK', '2/3'), ('8PSK', '3/4'), ('8PSK', '5/6'),
            ('8PSK', '8/9'), ('8PSK', '9/10'),
            ('16APSK', '2/3'), ('16APSK', '3/4'), ('16APSK', '4/5'), ('16APSK', '5/6'),
            ('16APSK', '8/9'), ('16APSK', '9/10'), ('32APSK', '3/4'), ('32APSK', '4/5'),
            ('32APSK', '5/6'), ('32APSK', '8/9'), ('32APSK', '9/10')
        ]
        state = None
        modcode = None
        def __init__(self):
            pass
        def constellation_fec(self): # TODO: why can the result be '-', '?'
            match self.state:
                case 'S':
                    return self.MODCOD_DVB_S[self.modecod]
                case 'S2':
                    return self.MODCOD_DVB_S2[self.modcod]
            return 'A', 'B'
        def reset(self):
            self.state = None
            self.modcode = None

################################################################

    modcod_pair = ModcodPair()
    
################################################################

    class DbMarginPair: # returns db_margin
        # SignalReport uses Modulation/mode & MER
        MOD_THRESHOLD = {
            'DVB-S 1/2':          1.7,
            'DVB-S 2/3':          3.3,
            'DVB-S 3/4':          4.2,
            'DVB-S 5/6':          5.1,
            'DVB-S 6/7':          5.5,
            'DVB-S 7/8':          5.8,
            'DVB-S2 QPSK 1/4':   -2.3,
            'DVB-S2 QPSK 1/3':   -1.2,
            'DVB-S2 QPSK 2/5':   -0.3,
            'DVB-S2 QPSK 1/2':    1.0,
            'DVB-S2 QPSK 3/5':    2.3,
            'DVB-S2 QPSK 2/3':    3.1,
            'DVB-S2 QPSK 3/4':    4.1,
            'DVB-S2 QPSK 4/5':    4.7,
            'DVB-S2 QPSK 5/6':    5.2,
            'DVB-S2 QPSK 8/9':    6.2,
            'DVB-S2 QPSK 9/10':   6.5,
            'DVB-S2 8PSK 3/5':    5.5,
            'DVB-S2 8PSK 2/3':    6.6,
            'DVB-S2 8PSK 3/4':    7.9,
            'DVB-S2 8PSK 5/6':    9.4,
            'DVB-S2 8PSK 8/9':    10.7,
            'DVB-S2 8PSK 9/10':   11.0,
            'DVB-S2 16APSK 2/3':  9.0,
            'DVB-S2 16APSK 3/4':  10.2,
            'DVB-S2 16APSK 4/5':  11.0,
            'DVB-S2 16APSK 5/6':  11.6,
            'DVB-S2 16APSK 8/9':  12.9,
            'DVB-S2 16APSK 9/10': 13.2,
            'DVB-S2 32APSK 3/4':  12.8,
            'DVB-S2 32APSK 4/5':  13.7,
            'DVB-S2 32APSK 5/6':  14.3,
            'DVB-S2 32APSK 8/9':  15.7,
            'DVB-S2 32APSK 9/10': 16.1,
        }
        state = None
        mer = None
        fec = None
        constellation = None
        def __init__(self):
            pass
        def compute_db_margin(self, state, mer, fec, constellation):
            if mer == '-' or fec == '-' or constellation == '-':
                return '-'
            if mer == None or fec == None or constellation == None:
                return '-'
            self.state = state
            self.mer = mer
            self.fec = fec
            self.constellation = constellation
            match self.state:
                case 'S':
                    key = f'DVB-S {self.fec}'
            match self.state:
                case 'S2':
                    key = f'DVB-S2 {self.constellation} {self.fec}'
                case '_':
                    return '-'
            float_mer = float(self.mer)
            float_threshold = self.MOD_THRESHOLD[key]
            db_margin = float_mer - float_threshold
            return 'D {:.1f}'.format(db_margin)
        def reset(self):
            self.state = None
            self.mer = None
            self.fec = None
            self.constellation = None


################################################################

    db_margin_pair = DbMarginPair()
    
################################################################

    def calculated_dbm_power(agc_pair): # returns dbm_power
        # TODO: Ryde Version, so rewrite using match/case instead of bisect()
        agc1_dict = OrderedDict() # collections.OrderedDict()
        agc1_dict[1] = -70
        agc1_dict[10] = -69
        agc1_dict[21800] = -68
        agc1_dict[25100] = -67
        agc1_dict[27100] = -66
        agc1_dict[28100] = -65
        agc1_dict[28900] = -64
        agc1_dict[29600] = -63
        agc1_dict[30100] = -62
        agc1_dict[30550] = -61
        agc1_dict[31000] = -60
        agc1_dict[31350] = -59
        agc1_dict[31700] = -58
        agc1_dict[32050] = -57
        agc1_dict[32400] = -56
        agc1_dict[32700] = -55
        agc1_dict[33000] = -54
        agc1_dict[33300] = -53
        agc1_dict[33600] = -52
        agc1_dict[33900] = -51
        agc1_dict[34200] = -50
        agc1_dict[34500] = -49
        agc1_dict[34750] = -48
        agc1_dict[35000] = -47
        agc1_dict[35250] = -46
        agc1_dict[35500] = -45
        agc1_dict[35750] = -44
        agc1_dict[36000] = -43
        agc1_dict[36200] = -42
        agc1_dict[36400] = -41
        agc1_dict[36600] = -40
        agc1_dict[36800] = -39
        agc1_dict[37000] = -38
        agc1_dict[37200] = -37
        agc1_dict[37400] = -36
        agc1_dict[37600] = -35
        agc1_dict[37700] = -35

        agc2_dict = OrderedDict() # collections.OrderedDict()
        agc2_dict[182] = -71
        agc2_dict[200] = -72
        agc2_dict[225] = -73
        agc2_dict[255] = -74
        agc2_dict[290] = -75
        agc2_dict[325] = -76
        agc2_dict[360] = -77
        agc2_dict[400] = -78
        agc2_dict[450] = -79
        agc2_dict[500] = -80
        agc2_dict[560] = -81
        agc2_dict[625] = -82
        agc2_dict[700] = -83
        agc2_dict[780] = -84
        agc2_dict[880] = -85
        agc2_dict[1000] = -86
        agc2_dict[1140] = -87
        agc2_dict[1300] = -88
        agc2_dict[1480] = -89
        agc2_dict[1660] = -90
        agc2_dict[1840] = -91
        agc2_dict[2020] = -92
        agc2_dict[2200] = -93
        agc2_dict[2380] = -94
        agc2_dict[2560] = -95
        agc2_dict[2740] = -96
        agc2_dict[3200] = -97

        if agc_pair.agc1 is None or agc_pair.agc2 is None:
            return '-'

        if agc_pair.agc1 > 0:
            lookup_dict = agc1_dict
            lookup_value = agc_pair.agc1
        else:
            lookup_dict = agc2_dict
            lookup_value = agc_pair.agc2

        agc_keys = list(lookup_dict.keys())

        # find where it would be inserted if it was a list
        agc_index = bisect.bisect_left(agc_keys,lookup_value)

        if agc_index >= len(agc_keys): # bigger than list use max value
            closest_key = agc_keys[-1]
        elif agc_index <= 0: # smaller than list use min value
            closest_key = agc_keys[0]
        elif abs(agc_keys[agc_index]-lookup_value) >= abs(agc_keys[agc_index-1]-lookup_value): # check if n or n-1 is closer
            closest_key = agc_keys[agc_index - 1]
        else:
            closest_key = agc_keys[agc_index]

        return lookup_dict[closest_key]

# LOOP BEGIN ########################################################################################

    while True:
        
        if longmynd2.poll():
            tune_args = longmynd2.recv()
            if tune_args == 'STOP':
                args = LM_STOP_SCRIPT
                p2 = subprocess.run(args)
                longmynd_data.longmynd_running = False
            else:
                requestKHzStr = str( int(float(tune_args.frequency) * 1000 - OFFSET) )
                args = [LM_START_SCRIPT, '-i ', TS_IP, TS_PORT, '-S', '0.6', requestKHzStr, tune_args.symbol_rate]
                p1 = subprocess.run(args) #, cwd='/home/pi/RxTouch/longmynd')
                longmynd_data.status_msg = f'tuned: {requestKHzStr}, {tune_args.symbol_rate}'
                longmynd_data.longmynd_running = True

        if longmynd_data.longmynd_running:

            # x_Ryde line 491
            lines = statusFIFOfd.readlines()
            if lines == []: 
                continue
            for line in lines:
                if line[0] != '$':
                    continue
                rawtype, rawval = line[1:].rstrip().split(',',1)
                msgtype = int(rawtype)

                match msgtype:
                    case 1: # State
                        match int(rawval):
                            case 0: # initialising
                                longmynd_data.mode = 'Initialising'
                            case 1: # searching
                                longmynd_data.mode = 'Seaching'
                            case 2: # found headers
                                longmynd_data.mode = 'Locked'
                            case 3: # locked on a DVB-S signal
                                longmynd_data.mode = 'DVBS-S'
                                modcod_pair.state = 'S'
                            case 4: # locked on a DVB-S2 signal
                                longmynd_data.mode = 'DVBS-S2'
                                modcod_pair.state = 'S2'

                        #if not hasPIDs:
                        #    self.tunerStatus.setPIDs(self.pidCache)
                        #    setPIDs(pidCache)
                        #hasPIDs = False

                        #if self.lastState != self.changeRefState : # if the signal parameters have changed
                        #    self.stateMonotonic += 1
                        #    self.changeRefState = copy.deepcopy(self.lastState)
                        #self.lastState['state'] = int(rawval)

                        if int(rawval) < 3: # if it is not locked, reset some state
                            longmynd_data.provider = '-'
                            longmynd_data.service = '-'
                            es_pair.reset()
                            longmynd_data.codecs = '-'
                            modcod_pair.reset()
                            longmynd_data.constellation = '-'
                            longmynd_data.fec = '-'
                            longmynd_data.null_ratio = '-'
                    case 2: # LNA Gain - On devices that have LNA Amplifiers this represents the two gain sent as N, where n = (lna_gain<<5) | lna_vgo. Though not actually linear, n can be usefully treated as a single byte representing the gain of the amplifier
                        pass
                    case 3: # Puncture Rate - During a search this is the pucture rate that is being trialled. When locked this is the pucture rate detected in the stream. Sent as a single value, n, where the pucture rate is n/(n+1)
                        pass
                    case 4: # I Symbol Power - Measure of the current power being seen in the I symbols
                        pass
                    case 5: # Q Symbol Power - Measure of the current power being seen in the Q symbols
                        pass
                    case 6: # Carrier Frequency - During a search this is the carrier frequency being trialled. When locked this is the Carrier Frequency detected in the stream. Sent in KHz
                        cf = float(rawval)
                        frequency = (cf + OFFSET) / 1000
                        longmynd_data.frequency = '{:.2f}'.format(frequency)
                    case 7: # I Constellation - Single signed byte representing the voltage of a sampled I point
                        pass
                    case 8: # Q Constellation - Single signed byte representing the voltage of a sampled Q point
                        pass
                    case 9: # Symbol Rate - During a search this is the symbol rate being trialled.  When locked this is the symbol rate detected in the stream
                        longmynd_data.symbol_rate = '{:.1f}'.format(float(rawval)/1000)
                    case 10: # Viterbi Error Rate - Viterbi correction rate as a percentage * 100
                        pass
                    case 11: # BER - Bit Error Rate as a Percentage * 100
                        pass
                    case 12: # MER - Modulation Error Ratio in dB * 10
                        if rawval != '0':
                            longmynd_data.db_mer = '{:.1f}'.format(float(rawval)/10)
                        else:
                            longmynd_data.db_mer = '-'
                    case 13: # Service Provider - TS Service Provider Name
                        longmynd_data.provider = str(rawval)
                    case 14: # Service Provider Service - TS Service Name
                        longmynd_data.service = str(rawval)
                    case 15: # Null Ratio - Ratio of Nulls in TS as percentage
                        longmynd_data.null_ratio = int(rawval)
                    case 16: # The PID numbers themselves are fairly arbitrary, will vary based on the transmitted signal and don't really mean anything in a single program multiplex.
                        # In the status stream 16 and 17 always come in pairs, 16 is the PID and 17 is the type for that PID, e.g.
                        # This means that PID 257 is of type 27 which you look up in the table to be H.264 and PID 258 is type 3 which the table says is MP3.
                        # $16,257 == PID 257 is of type 27 which you look up in the table to be H.264
                        # $17,27  meaning H.264
                        # $16,258 == PID 258 is type 3 which the table says is MP3
                        # $17,3   maeaning MP3
                        # The PID numbers themselves are fairly arbitrary, will vary based on the transmitted signal and don't really mean anything in a single program multiplex.
                        if not es_pair.has_1st_pid:
                            es_pair.has_1st_pid = True
                        elif not es_pair.has_2nd_pid:
                            es_pair.has_2nd_pid = True
                    case 17: # ES TYPE - Elementary Stream Type (repeated as pair with 16 for each ES)
                        if es_pair.has_1st_pid and not es_pair.has_2nd_pid:
                            es_pair.the_1st_type = rawval
                        elif es_pair.has_2nd_pid:
                            es_pair.the_2nd_type = rawval
                        if es_pair.has_1st_pid and es_pair.has_2nd_pid:
                            longmynd_data.codecs = f'{es_pair.codec(es_pair.the_1st_type)} {es_pair.codec(es_pair.the_2nd_type)}'
                            es_pair.reset()
                    case 18: # MODCOD - Received Modulation & Coding Rate. See MODCOD Lookup Table below
                    #    self.tunerStatus.setModcode(int(rawval))
                        modcod_pair.modcod = int(rawval)
                        longmynd_data.constellation, longmynd_data.fec = modcod_pair.constellation_fec()

                        # TODO: move db_margin_pair.compute_db_margin into ModcodPair
                        longmynd_data.db_margin = db_margin_pair.compute_db_margin(
                            modcod_pair.state,
                            longmynd_data.db_mer,
                            longmynd_data.fec,
                            longmynd_data.constellation
                        )

                    case 19: # Short Frames - 1 if received signal is using Short Frames, 0 otherwise (DVB-S2 only)
                        pass
                    case 20: # Pilot Symbols - 1 if received signal is using Pilot Symbols, 0 otherwise (DVB-S2 only)
                        pass
                    case 21: # LDPC Error Count - LDPC Corrected Errors in last frame (DVB-S2 only)
                        pass
                    case 22: # BCH Error Count - BCH Corrected Errors in last frame (DVB-S2 only)
                        pass
                    case 23: # BCH Uncorrected - 1 if some BCH-detected errors were not able to be corrected, 0 otherwise (DVB-S2 only)
                        pass
                    case 24: # LNB Voltage Enabled - 1 if LNB Voltage Supply is enabled, 0 otherwise (LNB Voltage Supply requires add-on board)
                        pass
                    case 25: # LNB H Polarisation - 1 if LNB Voltage Supply is configured for Horizontal Polarisation (18V), 0 otherwise (LNB Voltage Supply requires add-on board)
                        pass
                    case 26: # AGC1 Gain - Gain value of AGC1 (0: Signal too weak, 65535: Signal too strong)
                        # NOTE: may we should wait for the pair, as with 16 and 17
                        agc_pair.agc1 = int(rawval)
                        longmynd_data.dbm_power = calculated_dbm_power(agc_pair)
                    case 27: # AGC2 Gain - Gain value of AGC2 (0: Minimum Gain, 65535: Maximum Gain)
                        agc_pair.agc2 = int(rawval)
                        longmynd_data.dbm_power = calculated_dbm_power(agc_pair)

                longmynd2.send(longmynd_data)

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
            longmynd_data.null_ratio = '-'
            longmynd_data.provider = '-'
            longmynd_data.service = '-'
            longmynd_data.status_msg = '-'
            longmynd2.send(longmynd_data)
            sleep(0.5) # delay to simulate data reading

# LOOP END ########################################################################################
