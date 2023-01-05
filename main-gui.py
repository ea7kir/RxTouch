"""RxTouch"""

import PySimpleGUI as sg
import asyncio
from bandplan import bandplan as bp

########################################################################### begin spectrum data

import websockets

# Each scan sends a block of 1844 bytes
# This is 922 16-bit samples in low-high format
# The last two 16-bit samples are zero
# Sample zero is at 10490.500MHz
# Each sample represents 10000 / 1024 = 9.765625kHz
# Sample 919 is at 10499.475MHz
# The noise floor value is around 10000
# The peak of the beacon is around 40000

spectrum_data_changed = False

from dataclasses import dataclass

@dataclass
class SpectrumData:
    points = [(int(0),int(0))] * 920 # to ensure the last point is (0,0)
    beacon_level:int = 0

spectrum_data = SpectrumData()

async def read_spectrum_data():
    global running, spectrum_data_changed
    BATC_SPECTRUM_URI = 'wss://eshail.batc.org.uk/wb/fft/fft_ea7kirsatcontroller'
    websocket = await websockets.connect(BATC_SPECTRUM_URI)
    while running:
        recvd_data = await websocket.recv()
        if len(recvd_data) != 1844:
            print('rcvd_data != 1844')
            continue
        j = 1
        for i in range(0, 1836, 2):
            uint_16: int = int(recvd_data[i]) + (int(recvd_data[i+1] << 8))
            spectrum_data.points[j] = (j, uint_16)
            j += 1
        spectrum_data.points[919] = (919, 0)
        # calculate the average beacon peak level where beacon center is 103
        spectrum_data.beacon_level = 0
        for i in range(93, 113): # should be range(73, 133), but this works better
            spectrum_data.beacon_level += spectrum_data.points[i][1]
        spectrum_data.beacon_level //= 20.0
        spectrum_data_changed = True
        await asyncio.sleep(0)

########################################################################### end spectrum data

########################################################################### begin longmynd data

#from dataclasses import dataclass

@dataclass
class LongmyndData:
    frequency: int = 0
    symbol_rate: int = 0
    constellation: str = ''
    fec: str = ''
    codecs: str = ''
    db_mer: float = 0
    db_margin: float = 0
    dbm_power: int = 0
    null_ratio: int = 0
    provider: str = ''
    service: str = ''
    status_msg: str = 'status message'

longmynd_data = LongmyndData()

# TODO: put these into LongmyndData
longmynd_data_changed = False
longmynd_locked = True

import random # ONLY NEEDED TO SIMULATE DATA DURING DEVELOPMENT

MODE = [
    'Seaching',
    'Locked',
    'DVB-S',
    'DVB-S2',
]

async def read_longmynd_data():
    global running, longmynd_data_changed, longmynd_locked
    longmynd_locked = True
    while running:
        await asyncio.sleep(1) # temp delay to simulate data reading
        if longmynd_locked:
            longmynd_data.frequency = '10491.551'
            longmynd_data.symbol_rate = '1500'
            longmynd_data.mode = MODE[0]
            longmynd_data.constellation = 'QPSK'
            longmynd_data.fec = '4/5'
            longmynd_data.codecs = 'H264 MP3'
            longmynd_data.db_mer = '8.9'
            longmynd_data.db_margin = '4.1'
            longmynd_data.dbm_power = '-60'
            longmynd_data.null_ratio = random.randint(40, 60) # ONLY NEEDED TO SIMULATE DATA DURING DEVELOPMENT
            longmynd_data.provider = 'A71A'
            longmynd_data.service = 'QARS'
            longmynd_data.status_msg = 'online'
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
            longmynd_data.status_msg = 'offline'
        longmynd_data_changed = True
        await asyncio.sleep(1)

def start_longmynd(frequency, rate_list):
    global longmynd_locked
    if longmynd_locked:
        stop_longmynd
    # assemble the command line arguments
    # params = ["-i", TS_IP, TS_Port, "-S", "0.6", requestKHzStr, allSrs]
    OFFSET = 9750000
    TS_IP = '192.168.1.36'
    TS_PORT = '7777'
    requestKHzStr = str(float(frequency) * 1000 - OFFSET)
    allSrs = rate_list[0]
    for i in range(1, len(rate_list)):
        allSrs += f',{rate_list[i]}'
    params = ['-i ', TS_IP, TS_PORT, '-S', '0.6', requestKHzStr, allSrs]
    # TODO: execute longmynd with args see: https://youtu.be/VlfLqG_qjx0
    #time.sleep(2)
    longmynd_locked = True
    #self.status_msg = '{0}'.format(params)

def stop_longmynd(self):
    global longmynd_locked
    if not longmynd_locked:
        return
    #self.status_msg = 'stopping longmynd'
    longmynd_locked = False
    #time.sleep(2)
    #self.status_msg = 'longmynd stopped'

########################################################################### end longmynd data

# LAYOUT ----------------------------------------

sg.theme('Black')

MYSCRCOLOR = '#111111'
MYBUTCOLORS = ('#FFFFFF','#222222')
MYDISABLEDBTCOLORS = ('#444444',None)

def text_data(name, key):
    return sg.Text(name, size=11), sg.Text(' ', size=9, key=key, text_color='orange')

def incdec_but(name, key):
    return sg.Button(name, key=key, size=4, border_width=0, button_color=MYBUTCOLORS, mouseover_colors=MYBUTCOLORS)

def button_selector(key_down, value, key_up, width):
    return  incdec_but('<', key_down), sg.Text(' ', size=width, justification='center', key=value, text_color='orange'), incdec_but('>', key_up) 

top_layout = [
    sg.Button('RxTouch', key='-SYSTEM-', border_width=0, button_color=MYBUTCOLORS, mouseover_colors=MYBUTCOLORS),
    sg.Text(' ', expand_x=True, key='-STATUS_BAR-', text_color='orange'),
    sg.Button('Shutdown', key='-SHUTDOWN-', border_width=0, button_color=MYBUTCOLORS, mouseover_colors=MYBUTCOLORS),    
]

spectrum_layout = [
    # ORIGINAL sg.Graph(canvas_size=(770, 250), graph_bottom_left=(0, 0), graph_top_right=(918, 1.0), background_color='black', float_values=True, key='graph'),
    sg.Graph(canvas_size=(770, 250), graph_bottom_left=(0, 0x2000), graph_top_right=(918, 0xFFFF), background_color='black', float_values=False, key='graph'),
]

tune_layout = [
        sg.Column([
            button_selector('-BD-', '-BV-', '-BU-', 8),
        ]),
        sg.Column([
            button_selector('-SD-', '-SV-', '-SU-', 5),
        ]),
        sg.Column([
            button_selector('-FD-', '-FV-', '-FU-', 12),
        ]),
]

status_layout = [
    sg.Column([
        text_data('Frequency', '-FREQUENCY-'),
        text_data('Symbol Rate', '-SYMBOL_RATE-'),
        text_data('Mode', '-MODE-'),
        text_data('Constellation', '-CONSTELLATION-'),
    ]),
    sg.Column([
        text_data('FEC', '-FEC-'),
        text_data('Codecs', '-CODECS-'),
        text_data('dB MER', '-DB_MER-'),
        text_data('dB Margin', '-DB_MARGIN-'),
    ]),
    sg.Column([
        text_data('dBm Power', '-DBM_POWER-'),
        text_data('Null Ratio', '-NULL_RATIO-'),
        [sg.ProgressBar(100, orientation='h', size=(10, 10), key='-NULL_RATIO-BAR-', bar_color=('#00FF00','#111111'))],
        text_data('Provider', '-PROVIDER-'),
        text_data('Service', '-SERVICE-'),
    ]),
    sg.Column([
        [sg.Button(' TUNE ', key='-TUNE-', border_width=0, button_color=MYBUTCOLORS, mouseover_colors=MYBUTCOLORS, disabled_button_color=MYDISABLEDBTCOLORS, disabled=False)],
        [sg.Text(' ')],
        [sg.Button(' Mute ', key='-MUTE-', border_width=0, button_color=MYBUTCOLORS, mouseover_colors=MYBUTCOLORS, disabled_button_color=MYDISABLEDBTCOLORS, disabled=False)],
    ]),
]

layout = [
    top_layout,
    spectrum_layout,
    tune_layout,
    status_layout,
]

# CALLBACK DISPATCH -----------------------------

def tune():
    # callout to longmynd
    frequency, rate_list = bp.fequency_and_rate_list()
    start_longmynd(frequency, rate_list)

dispatch_dictionary = {
    # Lookup dictionary that maps button to function to call
    '-BD-':bp.dec_band, '-BU-':bp.inc_band, 
    '-FD-':bp.dec_frequency, '-FU-':bp.inc_frequency, 
    '-SD-':bp.dec_symbol_rate, '-SU-':bp.inc_symbol_rate,
    '-TUNE-':tune,
}

# UPDATE FUNCTIONS ------------------------------

def update_control():
    window['-BV-'].update(bp.band)
    window['-FV-'].update(bp.frequency)
    window['-SV-'].update(bp.symbol_rate)

def update_longmynd_status():
    window['-FREQUENCY-'].update(longmynd_data.frequency)
    window['-SYMBOL_RATE-'].update(longmynd_data.symbol_rate)
    window['-MODE-'].update(longmynd_data.mode)
    window['-CONSTELLATION-'].update(longmynd_data.constellation)
    window['-FEC-'].update(longmynd_data.fec)
    window['-CODECS-'].update(longmynd_data.codecs)
    window['-DB_MER-'].update(longmynd_data.db_mer)
    window['-DB_MARGIN-'].update(longmynd_data.db_margin)
    window['-DBM_POWER-'].update(longmynd_data.dbm_power)
    window['-NULL_RATIO-'].Update(longmynd_data.null_ratio)
    window['-NULL_RATIO-BAR-'].UpdateBar(longmynd_data.null_ratio)
    window['-PROVIDER-'].update(longmynd_data.provider)
    window['-SERVICE-'].update(longmynd_data.service)
    window['-STATUS_BAR-'].update(longmynd_data.status_msg)

def update_graph():
    # TODO: try just deleting the polygon and beakcon_level
    spectrum_graph.erase()
    # draw graticule
    c = 0
    for y in range(0x2697, 0xFFFF, 0xD2D): # 0x196A, 0xFFFF, 0xD2D
        if c in {0,5,10,15}:
            color = '#444444'
        else:
            color = '#222222'
        c += 1
        spectrum_graph.draw_line((0, y), (918, y), color=color)
    # TODO: sg.Text('15dB') 
    # TODO: sg.Text('10dB') 
    # TODO: sg.Text('5dB') 
    if TEST_GRAPH:
        spectrum_graph.draw_line((0, 0), (459, 0xFFFF), color='red', width=1)
        spectrum_graph.draw_line((459, 0xFFFF), (918, 0), color='red', width=1)
    else:
        # draw beacon level
        spectrum_graph.draw_line((0, spectrum_data.beacon_level), (918, spectrum_data.beacon_level), color='#880000', width=1)
        # draw spectrum
        spectrum_graph.draw_polygon(spectrum_data.points, fill_color='green')

# MAIN ------------------------------------------

window = sg.Window('', layout, size=(800, 480), font=(None, 11), background_color=MYSCRCOLOR, use_default_focus=False, finalize=True)
window.set_cursor('none')
spectrum_graph = window['graph']

running = True
TEST_GRAPH = False

async def main_window():
    global running, spectrum_data_changed, longmynd_data_changed
    
    while running:
        event, values = window.read(timeout=10)
        if event == '-SHUTDOWN-':
            if sg.popup_yes_no('Shutdown Now?', background_color='red', keep_on_top=True) == 'Yes':
                lm.stop_longmynd()
                running = False
        if event in dispatch_dictionary:
            func_to_call = dispatch_dictionary[event]
            func_to_call()
        if spectrum_data_changed:
            update_graph()
            spectrum_data_changed = False
        if bp.changed:
            update_control()
            bp.changed = False
        if longmynd_data_changed:
            update_longmynd_status()
            longmynd_data_changed = False
        await asyncio.sleep(0)

async def main(): # TODO: could we call 
    await asyncio.gather(
        main_window(),
        read_spectrum_data(),
        read_longmynd_data(),
    )
    print('all tasks have closed')
    window.close()
    if window.was_closed():
        print('main window has closed')

if __name__ == '__main__':
    asyncio.run(main())
    print('about to shut down')
    #import subprocess
    #subprocess.check_call(['sudo', 'poweroff'])
