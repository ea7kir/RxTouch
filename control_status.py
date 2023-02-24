from device_manager import activate_mute, deactivate_mute

TUNED_MARKER = [
    # first Int16 represents 10490.500 MHz
    # last Int16 represents 10499.475 MHz
    # spectrum with = 10499.475 - 10490.500 = 8.975 Mhz
    # width between channels = 0.25 MHz
    103, # '10491.50 / 00' beacon
    230, # '10492.75 / 01'
    256, # '10493.00 / 02'
    281, # '10493.25 / 03'
    307, # '10493.50 / 04'
    332, # '10493.75 / 05'
    358, # '10494.00 / 06'
    383, # '10494.25 / 07'
    409, # '10494.50 / 08'
    434, # '10494.75 / 09'
    460, # '10495.00 / 10'
    485, # '10495.25 / 11'
    511, # '10495.50 / 12'
    536, # '10495.75 / 13'
    562, # '10496.00 / 14'
    588, # '10496.25 / 15'
    613, # '10496.50 / 16'
    639, # '10496.75 / 17'
    664, # '10497.00 / 18'
    690, # '10497.25 / 19'
    715, # '10497.50 / 20'
    741, # '10497.75 / 21'
    767, # '10490.00 / 22'
    792, # '10498.25 / 23'
    818, # '10498.50 / 24'
    843, # '10498.75 / 25'
    869, # '10499.00 / 26'
    894, # '10499.25 / 27'
]

BAND_LIST = [
    'Beacon','Wide','Narrow','V.Narrow',
]
BEACON_FREQUENCY_LIST = [
    '10491.50 / 00',
]
WIDE_FREQUENCY_LIST = [
    '10493.25 / 03',
    '10494.75 / 09',
    '10496.25 / 15',
]
NARROW_FREQUENCY_LIST = [
    '10492.75 / 01',
    '10493.25 / 03',
    '10493.75 / 05',
    '10494.25 / 07',
    '10494.75 / 09',
    '10495.25 / 11',
    '10495.75 / 13',
    '10496.25 / 15',
    '10496.75 / 17',
    '10497.25 / 19',
    '10497.75 / 21',
    '10498.25 / 23',
    '10498.75 / 25',
    '10499.25 / 27', # index 13
]
VERY_NARROW_FREQUENCY_LIST = [
    '10492.75 / 01',
    '10493.00 / 02',
    '10493.25 / 03',
    '10493.50 / 04',
    '10493.75 / 05',
    '10494.00 / 06',
    '10494.25 / 07',
    '10494.50 / 08',
    '10494.75 / 09',
    '10495.00 / 10',
    '10495.25 / 11',
    '10495.50 / 12',
    '10495.75 / 13',
    '10496.00 / 14', # index 13
    '10496.25 / 15',
    '10496.50 / 16',
    '10496.75 / 17',
    '10497.00 / 18',
    '10497.25 / 19',
    '10497.50 / 20',
    '10497.75 / 21',
    '10498.00 / 22',
    '10498.25 / 23',
    '10498.50 / 24',
    '10498.75 / 25',
    '10499.00 / 26',
    '10499.25 / 27',
]
BEACON_SYMBOL_RATE_LIST = [ 
    '1500',
]
WIDE_SYMBOL_RATE_LIST = [
    'AUTO','500','1000','1500',
]
NARROW_SYMBOL_RATE_LIST = [
    'AUTO','125','250','333',
]
VERY_NARROW_SYMBOL_RATE_LIST = [
    'AUTO','25','33','66',
]

BEACON_BAND_LIST_INDEX = 0
WIDE_BAND_LIST_INDEX = 1
NARROW_BAND_LIST_INDEX = 2
VERY_NARROW_BAND_LIST_INDEX = 3

INITIAL_BAND                        = 0 # beacon
INITIAL_BEACON_FREQUENCY            = 0
INITIAL_BEACON_SYMBOL_RATE          = 0
INITIAL_WIDE_SYMBOL_RATE            = 0 # AUTO
INITIAL_WIDE_FREQUENCY              = 1 # chan 9
INITIAL_NARROW_SYMBOL_RATE          = 3 # 333
INITIAL_NARROW_FREQUENCY            = 13 # chan 27
INITIAL_VERY_NARROW_SYMBOL_RATE     = 3 # 66
INITIAL_VERY_NARROW_FREQUENCY       = 13 # chan 14

class BeaconIndex:
    band = BEACON_BAND_LIST_INDEX
    frequency = INITIAL_BEACON_FREQUENCY
    symbol_rate = INITIAL_BEACON_SYMBOL_RATE
    frequency_list = BEACON_FREQUENCY_LIST
    max_frequency_index = len(BEACON_FREQUENCY_LIST) - 1
    symbol_rate_list = BEACON_SYMBOL_RATE_LIST
    max_symbol_rate_list = len(BEACON_SYMBOL_RATE_LIST) - 1

class WideIndex:
    band = WIDE_BAND_LIST_INDEX
    frequency = INITIAL_WIDE_FREQUENCY
    symbol_rate = INITIAL_WIDE_SYMBOL_RATE
    frequency_list = WIDE_FREQUENCY_LIST
    max_frequency_index = len(WIDE_FREQUENCY_LIST) - 1
    symbol_rate_list = WIDE_SYMBOL_RATE_LIST
    max_symbol_rate_list = len(WIDE_SYMBOL_RATE_LIST) - 1

class NarrowIndex:
    band = NARROW_BAND_LIST_INDEX
    frequency = INITIAL_NARROW_FREQUENCY
    symbol_rate = INITIAL_NARROW_SYMBOL_RATE
    frequency_list = NARROW_FREQUENCY_LIST
    max_frequency_index = len(NARROW_FREQUENCY_LIST) - 1
    symbol_rate_list = NARROW_SYMBOL_RATE_LIST
    max_symbol_rate_list = len(NARROW_SYMBOL_RATE_LIST) - 1

class VeryNarrowIndex:
    band = VERY_NARROW_BAND_LIST_INDEX
    frequency = INITIAL_VERY_NARROW_FREQUENCY
    symbol_rate = INITIAL_VERY_NARROW_SYMBOL_RATE
    frequency_list = VERY_NARROW_FREQUENCY_LIST
    max_frequency_index = len(VERY_NARROW_FREQUENCY_LIST) - 1
    symbol_rate_list = VERY_NARROW_SYMBOL_RATE_LIST
    max_symbol_rate_list = len(VERY_NARROW_SYMBOL_RATE_LIST) - 1

index = [ BeaconIndex, WideIndex, NarrowIndex, VeryNarrowIndex ]

class BeaconValue:
    band = BAND_LIST[BeaconIndex.band]
    frequency = BEACON_FREQUENCY_LIST[BeaconIndex.frequency]
    symbol_rate = BEACON_SYMBOL_RATE_LIST[BeaconIndex.symbol_rate]

class  WideValue:
    band = BAND_LIST[WideIndex.band]
    frequency = WIDE_FREQUENCY_LIST[WideIndex.frequency]
    symbol_rate = WIDE_SYMBOL_RATE_LIST[WideIndex.symbol_rate]

class NarrowValue:
    band = BAND_LIST[NarrowIndex.band]
    frequency = NARROW_FREQUENCY_LIST[NarrowIndex.frequency]
    symbol_rate = NARROW_SYMBOL_RATE_LIST[NarrowIndex.symbol_rate]

class VeryNarrowValue:
    band = BAND_LIST[VeryNarrowIndex.band]
    frequency = VERY_NARROW_FREQUENCY_LIST[VeryNarrowIndex.frequency]
    symbol_rate = VERY_NARROW_SYMBOL_RATE_LIST[VeryNarrowIndex.symbol_rate]

value = [ BeaconValue, WideValue, NarrowValue, VeryNarrowValue ]

curr_band = INITIAL_BAND
curr_value = value[curr_band]
curr_index = index[curr_band]
max_band_list = len(BAND_LIST) - 1 # TODO: messy!  try integrating band into the Index classes

def inc_band():
    global curr_band, max_band_list, curr_value, curr_index
    if curr_band < max_band_list:
        curr_band += 1
        curr_value = value[curr_band]
        curr_index = index[curr_band]
        return True
    return False

def dec_band():
    global curr_band, curr_value, curr_index
    if curr_band > 0:
        curr_band -= 1
        curr_value = value[curr_band]
        curr_index = index[curr_band]
        return True
    return False
    
def inc_frequency():
    global curr_value, curr_index
    if curr_index.frequency < curr_index.max_frequency_index:
        curr_index.frequency += 1
        curr_value.frequency = curr_index.frequency_list[curr_index.frequency]
        return True
    return False

def dec_frequency():
    global curr_value, curr_index
    if curr_index.frequency > 0:
        curr_index.frequency -= 1
        curr_value.frequency = curr_index.frequency_list[curr_index.frequency]
        return True
    return False
    
def inc_symbol_rate():
    global curr_value, curr_index
    if curr_index.symbol_rate < curr_index.max_symbol_rate_list:
        curr_index.symbol_rate += 1
        curr_value.symbol_rate = curr_index.symbol_rate_list[curr_index.symbol_rate]
        return True
    return False

def dec_symbol_rate():
    global curr_value, curr_index
    if curr_index.symbol_rate > 0:
        curr_index.symbol_rate -= 1
        curr_value.symbol_rate = curr_index.symbol_rate_list[curr_index.symbol_rate]
        return True
    return False
    
def selected_frequency_marker():
    i = int(curr_value.frequency[10:])
    return TUNED_MARKER[i]

class TuneArgs:
    frequency = ''
    symbol_rate = ''

def tune_args():
    global curr_value, curr_index
    tune_args = TuneArgs()
    tune_args.frequency = curr_value.frequency[:8]
    if curr_value.symbol_rate == 'AUTO':
        tune_args.symbol_rate = curr_index.symbol_rate_list[1]
        for i in range(2, curr_index.max_symbol_rate_list + 1):
            tune_args.symbol_rate += f',{curr_index.symbol_rate_list[i]}'
    else:
        tune_args.symbol_rate = curr_value.symbol_rate
    return tune_args

NORMAL_BUTTON_COLOR = ('#FFFFFF','#222222')
DISABALED_BUTTON_COLOR = ('#444444',None)
TUNE_ACTIVE_BUTTON_COLOR = ('#FFFFFF','#007700')
MUTE_ACTIVE_BUTTON_COLOR = ('#FFFFFF','#FF0000')
   
tune_is_active = False
mute_is_active = False
tune_button_color = NORMAL_BUTTON_COLOR
mute_button_color = NORMAL_BUTTON_COLOR

longmynd_pipe = None # intialized in main_gui.py

def tune():
    global tune_is_active, tune_button_color
    tune_is_active = not tune_is_active
    if tune_is_active:
        tune_button_color = TUNE_ACTIVE_BUTTON_COLOR
        args = tune_args()
        longmynd_pipe.send(args)
    else:
        tune_button_color = NORMAL_BUTTON_COLOR
        longmynd_pipe.send('STOP')

def cancel_tune(): # called when any tuning button is pressed
    if tune_is_active:
        tune()

def mute():
    global mute_is_active, mute_button_color
    mute_is_active = not mute_is_active
    if mute_is_active:
        mute_button_color = MUTE_ACTIVE_BUTTON_COLOR
        activate_mute()
    else:
        mute_button_color = NORMAL_BUTTON_COLOR
        deactivate_mute()
