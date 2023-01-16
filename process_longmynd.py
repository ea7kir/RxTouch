import subprocess
import os

import random # ONLY NEEDED TO SIMULATE DATA VALUES DURING DEVELOPMENT
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

    # x_Ryde line7 05
    statusFIFOfd = os.fdopen(os.open(LM_STATUS_PIPE, flags=os.O_NONBLOCK, mode=os.O_RDONLY), encoding="utf-8", errors="replace")

    ES_257 = {
        '2': 'MPEG-2',
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

    videoCodec = '-'
    audioCodec = '-'
    ES_PID = None

#    # TODO:  I don't think these should go here !!!!!!!!!!!!!!
#    hasPIDs = False
#    pidCacheWait = True
#    pidCachePair = (None, None)
#    pidCache = {}
#    pidCacheFault = False
#
#    # my new variables
#    ES_PIDs = {}
#    ES_Types = {}
#
#    import enum
#    class CodecEnum(enum.Enum):
#        MP2  = (enum.auto(), "MPEG-2")
#        MP3  = (enum.auto(), "MP3")
#        AAC  = (enum.auto(), "AAC")
#        H263 = (enum.auto(), "H.263")
#        H264 = (enum.auto(), "H.264")
#        MPA  = (enum.auto(), "MPA")
#        H265 = (enum.auto(), "H.265")
#        AC3  = (enum.auto(), "AC3")
#
#        def __init__(self, enum, longName):
#            self.longName = longName
#        def __str__(self):
#            return self.longName
#
#    def setPIDs(newval):
#        print(newval, flush=True)
#        #pass
#        codecmap = {
#             2:CodecEnum.MP2,
#             3:CodecEnum.MP3,
#             4:CodecEnum.MP3,
#            15:CodecEnum.AAC,
#            16:CodecEnum.H263,
#            27:CodecEnum.H264,
#            32:CodecEnum.MPA,
#            36:CodecEnum.H265,
#            129:CodecEnum.AC3,
#            }
#        newPIDs = {}
#        for pid, codec in newval.items():
#            if codec in codecmap:
#                newPIDs[pid] = codecmap[codec]
#                #videoCodec = codecmap[codec]
#                #print('T', newPIDs[pid], flush=True)
#            else:
#                newPIDs[pid] = str(codec)+"?"
#                #print('F', newPIDs[pid], flush=True)
#        #print(newPIDs[0], newPIDs[1])
#        #if pids != newPIDs:
#        #    pids = newPIDs
#        #    onChangeFire()
#        #    return True
#        #else:
#        #   return False

    """ WAITING FOR

        PIDs
        Constellation
        FEC
        Codecs
        db Margin
        dBm Margin

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
                        #longmynd_data.
                        #longmynd_data.

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
                    ES_PID = rawval
                elif msgtype == 17: # ES TYPE
                    if ES_PID == '257':
                        videoCodec = ES_257.get(rawval)
                        if videoCodec is None:
                            videoCodec = '?'
                    elif ES_PID == '258':
                        audioCodec = ES_258.get(rawval)
                        if audioCodec is None:
                            audioCodec = '?'
                    longmynd_data.codecs = f'{videoCodec} {audioCodec}'
                    
                elif msgtype == 18: # MODCOD
                #    self.tunerStatus.setModcode(int(rawval))
                #    self.lastState['modcode'] = int(rawval)
                    pass
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
                    pass
                elif msgtype == 27: # AGC2 Gain
                #    self.tunerStatus.setAGC2(int(rawval))
                    pass

#                if len(ES_PIDs) == 2 and len(ES_Types) == 2:
#                    print(ES_PIDs, ES_Types, flush=True)


#                # PID list accumulator
#                if msgtype == 16: # ES PID
#                    print(f'16 ES PID = {rawval}')
#                    hasPIDs = True
#                    pidCacheWait = False
#                    if pidCachePair[0] == None:
#                        pidCachePair = (int(rawval), pidCachePair[1])
#                        if pidCachePair[1] != None:
#                            pidCache[pidCachePair[0]] = pidCachePair[1]
#                            pidCachePair = (None, None)
#                    else:
#                        pidCacheFault = True
#                        print('pid cache fault', flush=True)
#                elif msgtype == 17: # ES Type
#                    print(f'16 ES Type = {rawval}')
#                    hasPIDs = True
#                    pidCacheWait = False
#                    if pidCachePair[1] == None:
#                        pidCachePair = (pidCachePair[0], int(rawval))
#                        if pidCachePair[0] != None:
#                            pidCache[pidCachePair[0]] = pidCachePair[1]
#                            pidCachePair = (None, None)
#                    else:
#                        pidCacheFault = True
#                        print('pid cache fault', flush=True)
#                # update pid status once we have them all (uness there was a fault)
#                elif not pidCacheWait:
#                    if not pidCacheFault:
#                        #lastState['pids'] = pidCache
#                        #tunerStatus.setPIDs(pidCache)
#                        # ???
#                        setPIDs(pidCache)
#                    pidCacheFault = False
#                    pidCacheWait = True
#                    pidCache = {}
#                    pidCachePair= (None, None)

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
            sleep(0.5) # temp delay to simulate data reading
