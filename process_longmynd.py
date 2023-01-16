import subprocess
import os

#import random # ONLY NEEDED TO SIMULATE DATA VALUES DURING DEVELOPMENT
from time import sleep # ONLY NEEDED TO SIMULATE FETCH TIMES DURING DEVELOPMENT

class LongmyndData:
    frequency: str = ''
    symbol_rate: str = ''
    constellation: str = ''
    fec: str = ''
    codecs: str = ''
    db_mer: str = ''
    db_margin: str = ''
    dbm_power: str = ''
    null_ratio: int = 0
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

    longmynd_data = LongmyndData()

    statusFIFOfd = os.fdopen(os.open(LM_STATUS_PIPE, flags=os.O_NONBLOCK, mode=os.O_RDONLY), encoding="utf-8", errors="replace")

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

        Constellation
        FEC
        dB Margin       SignalReport uses Modulation/mode & MER 
        dBm Power

        formating
    """

    while True:
        if longmynd2.poll():
            tune_args = longmynd2.recv()
            if tune_args == 'STOP':
                args = LM_STOP_SCRIPT
                p2 = subprocess.run(args)
                longmynd_data.longmynd_running = False
            else:
                OFFSET = 9750000
                TS_IP = '192.168.1.41' # Apple TV at office.local
                TS_PORT = '7777'
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
                
                # x_Ryde line 497
                if msgtype == 1: # State
                    if int(rawval) == 0: # initialising
                        longmynd_data.mode = 'Initialising'
                    if int(rawval) == 1: # searching
                        longmynd_data.mode = 'Seaching'
                    elif int(rawval) == 2: # found headers
                        longmynd_data.mode = 'Locked'
                    elif int(rawval) == 3: # locked on a DVB-S signal
                        longmynd_data.mode = 'DVBS-S'
                    elif int(rawval) == 4: # locked on a DVB-S2 signal
                        longmynd_data.mode = 'DVBS-S2'

#                    if not hasPIDs:
#                    #    self.tunerStatus.setPIDs(self.pidCache)
#                        setPIDs(pidCache)
#                    hasPIDs = False

                    #if self.lastState != self.changeRefState : # if the signal parameters have changed
                    #    self.stateMonotonic += 1
                    #    self.changeRefState = copy.deepcopy(self.lastState)
                    #self.lastState['state'] = int(rawval)

                    if int(rawval) < 3: # if it is not locked, reset some state
                    #    self.lastState['provider'] = ""
                    #    self.lastState['service'] = ""
                    #    self.lastState['modcode'] = None
                    #    self.lastState['pids'] = {}
                        longmynd_data.provider = '-'
                        longmynd_data.service = '-'
                        video_codec = '-'
                        audio_codec = '-'
                        es_pid = None
                        longmynd_data.codecs = '-'
                        longmynd_data.constellation = '-'
                        longmynd_data.null_ratio = 0

                    #if self.lastState != self.changeRefState : # if the signal parameters have changed
                    #    self.stateMonotonic += 1
                    #    self.changeRefState = copy.deepcopy(self.lastState)

                elif msgtype == 2: # LNA Gain
                    pass
                elif msgtype == 3: # Puncture Rate
                    pass
                elif msgtype == 4: # I Symbol Power
                    pass
                elif msgtype == 5: # Q Symbol Power
                    pass
                elif msgtype == 6: # Carrier Frequency
                #    currentBand = self.activeConfig.getBand()
                #    self.tunerStatus.setFreq(currentBand.mapTuneToReq(int(rawval)))
                    cf = float(rawval)
                    frequency = (cf + OFFSET) / 1000
                    longmynd_data.frequency = frequency # TODO: format as #####.##
                elif msgtype == 7: # I Constellation
                    pass
                elif msgtype == 8: # Q Constellation
                    pass
                elif msgtype == 9: # Symbol Rate
                    #self.tunerStatus.setSR(float(rawval)/1000)
                    #print(f'->{msgtype}, {rawval}', flush=True)
                    longmynd_data.symbol_rate = str(float(rawval)/1000) # TODO: format as .#
                elif msgtype == 10: # Viterbi Error Rate
                    pass
                elif msgtype == 11: # BER
                    pass
                elif msgtype == 12: # MER
                    #print(f'-> {msgtype}, {rawval}', flush=True)
                    #self.tunerStatus.setMer(float(rawval)/10)
                    longmynd_data.db_mer = f'{float(rawval)/10}' # TODO: format as .#
                elif msgtype == 13: # Service Provider
                    #print(f'-> {msgtype}, {rawval}', flush=True)
                    longmynd_data.provider = str(rawval)
                elif msgtype == 14: # 
                    #print(f'-> {msgtype}, {rawval}', flush=True)
                    longmynd_data.service = str(rawval)
                elif msgtype == 15: # Null Ratio
                    longmynd_data.null_ratio = int(rawval)
                elif msgtype == 16: # ES PID
                    es_pid = rawval
                elif msgtype == 17: # ES TYPE
                    if es_pid == '257':
                        video_codec = ES_257.get(rawval)
                        if video_codec is None:
                            video_codec = f'{rawval}?'
                    elif es_pid == '258':
                        audio_codec = ES_258.get(rawval)
                        if audio_codec is None:
                            audio_codec = f'{rawval}?'
                    longmynd_data.codecs = f'{video_codec} {audio_codec}'
                elif msgtype == 18: # MODCOD
                #    self.tunerStatus.setModcode(int(rawval))
                #    self.lastState['modcode'] = int(rawval)
                    mode_code = int(rawval)
                elif msgtype == 19: # Short Frames
                    pass
                elif msgtype == 20: # Pilot Symbols
                    pass
                elif msgtype == 21: # LDPC Error Count
                    pass
                elif msgtype == 22: # BCH Error Count
                    pass
                elif msgtype == 23: # BCH Uncorrected
                    pass
                elif msgtype == 24: # LNB Voltage Enabled
                    pass
                elif msgtype == 25: # LNB H Polarisation
                    pass
                elif msgtype == 26: # AGC1 Gain
                #    self.tunerStatus.setAGC1(int(rawval))
                    agc1 = int(rawval)
                    longmynd_data.dbm_power = calculated_dbm_power(agc1, agc2)
                elif msgtype == 27: # AGC2 Gain
                #    self.tunerStatus.setAGC2(int(rawval))
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
            longmynd_data.null_ratio = 0
            longmynd_data.provider = '-'
            longmynd_data.service = '-'
            longmynd_data.status_msg = '-'
            longmynd2.send(longmynd_data)
            sleep(0.5) # delay to simulate data reading
