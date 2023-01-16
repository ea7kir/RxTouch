import subprocess
import os

from collections import OrderedDict # for power levels
import bisect  # for power levels

from time import sleep # ONLY NEEDED TO SIMULATE FETCH TIMES DURING DEVELOPMENT

class LongmyndData:  # TODO: most values could be None
    frequency: str = ''
    symbol_rate: str = ''
    constellation: str = ''
    fec: str = ''
    codecs: str = ''
    db_mer: str = ''
    db_margin: str = ''
    dbm_power: str = ''
    null_ratio: str = ''
    provider: str = ''
    service: str = ''
    status_msg: str = ''
    longmynd_running: bool = False

"""
Example to receive the beacon:
cd /home/pi/RxTouch/longmynd
/home/pi/RxTouch/longmynd/longmynd -i 192.168.1.41 7777 -S 0.6 741500 1500 &
"""

def process_read_longmynd_data(longmynd2):
    LM_STOP_START_SCRIPT = '/home/pi/RxTouch/lm_stopstart'
    LM_STOP_SCRIPT = '/home/pi/RxTouch/lm_stop'
    LM_STATUS_PIPE  = '/home/pi/RxTouch/longmynd/longmynd_main_status'

    OFFSET = 9750000
    TS_IP = '192.168.1.41' # Apple TV at office.local
    TS_PORT = '7777'

    longmynd_data = LongmyndData()

    statusFIFOfd = os.fdopen(os.open(LM_STATUS_PIPE, flags=os.O_NONBLOCK, mode=os.O_RDONLY), encoding="utf-8", errors="replace")

# TODO: the following PID decdoding is no workin properly
# ES PID = 257, ES TYPE = 15 and ES PID = 256, ES TYPE = 36
# So 2 tables are NOT better than 1

    ES_257 = {
        '2': 'MPEG-2', # TODO: too wide for display column
        '16': 'H.263',
        '27': 'H.264',
        '36': 'H.265',
    }

    ES_258 = {
        '3': 'MP3',
        '4': 'MP3',
        '15': 'ACC',
        '32': 'MPA',
        '129': 'AC3',
    }

    video_codec = '-'
    audio_codec = '-'
    es_pid = None
    agc1 = None
    agc2 = None
    agc_changed = False

    def calculated_dbm_power(agc1, agc2):
        return '-'

    """ WAITING FOR

        Codecs          fails if PID is not 257 and 258
        Constellation
        FEC
        dB Margin       SignalReport uses Modulation/mode & MER 

        formating
    """

    def calculated_dbm_power(agc1, agc2):
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

        if agc1 is None or agc2 is None:
            return '-'

        if agc1 > 0:
            lookup_dict = agc1_dict
            lookup_value = agc1
        else:
            lookup_dict = agc2_dict
            lookup_value = agc2

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


    while True:
        if longmynd2.poll():
            tune_args = longmynd2.recv()
            if tune_args == 'STOP':
                args = LM_STOP_SCRIPT
                p2 = subprocess.run(args)
                longmynd_data.longmynd_running = False
            else:
                requestKHzStr = str( int(float(tune_args.frequency) * 1000 - OFFSET) )
                args = [LM_STOP_START_SCRIPT, '-i ', TS_IP, TS_PORT, '-S', '0.6', requestKHzStr, tune_args.symbol_rate]
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
                            case 4: # locked on a DVB-S2 signal
                                longmynd_data.mode = 'DVBS-S2'

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
                            video_codec = '-'
                            audio_codec = '-'
                            es_pid = None
                            longmynd_data.codecs = '-'
                            longmynd_data.constellation = '-'
                            longmynd_data.null_ratio = 0
                    case  2: # LNA Gain
                        pass
                    case 3: # Puncture Rate
                        pass
                    case 4: # I Symbol Power
                        pass
                    case 5: # Q Symbol Power
                        pass
                    case 6: # Carrier Frequency
                        cf = float(rawval)
                        frequency = (cf + OFFSET) / 1000
                        longmynd_data.frequency = frequency # TODO: format as #####.##
                    case 7: # I Constellation
                        pass
                    case 8: # Q Constellation
                        pass
                    case 9: # Symbol Rate
                        longmynd_data.symbol_rate = str(float(rawval)/1000) # TODO: format as .#
                    case 10: # Viterbi Error Rate
                        pass
                    case 11: # BER
                        pass
                    case 12: # MER
                        longmynd_data.db_mer = f'{float(rawval)/10}' # TODO: format as .#
                    case 13: # Service Provider
                        longmynd_data.provider = str(rawval)
                    case 14: # 
                        longmynd_data.service = str(rawval)
                    case 15: # Null Ratio
                        longmynd_data.null_ratio = int(rawval)
                    case 16: # ES PID
                        es_pid = rawval
                        #print(f'PID = {rawval}')
                    case 17: # ES TYPE
                        match es_pid:
                            case '257':
                                video_codec = ES_257.get(rawval)
                                if video_codec is None:
                                    video_codec = f'{rawval}?'
                            case '258':
                                audio_codec = ES_258.get(rawval)
                                if audio_codec is None:
                                    audio_codec = f'{rawval}?'
                            #case _:
                            #    print(f'PID = {es_pid}, TYPE = {rawval}')
                        longmynd_data.codecs = f'{video_codec} {audio_codec}'
                    case 18: # MODCOD
                    #    self.tunerStatus.setModcode(int(rawval))
                        mode_code = int(rawval)
                    case 19: # Short Frames
                        pass
                    case 20: # Pilot Symbols
                        pass
                    case 21: # LDPC Error Count
                        pass
                    case 22: # BCH Error Count
                        pass
                    case 23: # BCH Uncorrected
                        pass
                    case 24: # LNB Voltage Enabled
                        pass
                    case 25: # LNB H Polarisation
                        pass
                    case 26: # AGC1 Gain
                        agc1 = int(rawval)
                        longmynd_data.dbm_power = calculated_dbm_power(agc1, agc2)
                    case 27: # AGC2 Gain
                        agc2 = int(rawval)
                        longmynd_data.dbm_power = calculated_dbm_power(agc1, agc2)

                # TODO: if changed:
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
