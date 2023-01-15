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
    status_msg: str = 'xxx'
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

    # TODO:  I don't think these should go here !!!!!!!!!!!!!!
    hasPIDs = False
    pidCacheWait = True
    pidCachePair = (None, None)
    pidCache = {}
    pidCacheFault = False

    def setPIDs(cache):
        # TODO: figure this one out
        pass

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

                    if not hasPIDs:
                    #    self.tunerStatus.setPIDs(self.pidCache)
                        setPIDs(pidCache)
                    hasPIDs = False

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

                ### elif msgtype == 16: # ES PID
                ###     pass
                ### elif msgtype == 17: # ES TYPE
                ###     pass

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

                # PID list accumulator
                if msgtype == 16: # ES PID
                    hasPIDs = True
                    pidCacheWait = False
                    if pidCachePair[0] == None:
                        pidCachePair = (int(rawval), pidCachePair[1])
                        if pidCachePair[1] != None:
                            pidCache[pidCachePair[0]] = pidCachePair[1]
                            pidCachePair = (None, None)
                    else:
                        pidCacheFault = True
                        print('pid cache fault', flush=True)
                elif msgtype == 17: # ES Type
                    hasPIDs = True
                    pidCacheWait = False
                    if pidCachePair[1] == None:
                        pidCachePair = (pidCachePair[0], int(rawval))
                        if pidCachePair[0] != None:
                            pidCache[pidCachePair[0]] = pidCachePair[1]
                            pidCachePair = (None, None)
                    else:
                        pidCacheFault = True
                        print('pid cache fault', flush=True)
                # update pid status once we have them all (uness there was a fault)
                elif not pidCacheWait:
                    if not pidCacheFault:
                        #lastState['pids'] = pidCache
                        #tunerStatus.setPIDs(pidCache)
                        # ???
                        setPIDs(pidCache)
                    pidCacheFault = False
                    pidCacheWait = True
                    pidCache = {}
                    pidCachePair= (None, None)

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
