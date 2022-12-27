"""RxTouch"""

import PySimpleGUI as sg
import asyncio
from bandplan import bandplan as bp
from longmynd_manager import longmynd_manager as lm

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
    sg.Text(' ', expand_x=True, key='-STATUS_BAR-', text_color='green'),
    sg.Button('Shutdown', key='-SHUTDOWN-', border_width=0, button_color=MYBUTCOLORS, mouseover_colors=MYBUTCOLORS),    
]

spectrum_layout = [
    sg.Graph(canvas_size=(800, 200), graph_bottom_left=(0, 0), graph_top_right=(918, 1.0), background_color='black', float_values=True, key='graph'),
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
    lm.start_longmynd(frequency, rate_list)

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

def update_status():
    window['-FREQUENCY-'].update(lm.frequency)
    window['-SYMBOL_RATE-'].update(lm.symbol_rate)
    window['-MODE-'].update(lm.mode)
    window['-CONSTELLATION-'].update(lm.constellation)
    window['-FEC-'].update(lm.fec)
    window['-CODECS-'].update(lm.codecs)
    window['-DB_MER-'].update(lm.db_mer)
    window['-DB_MARGIN-'].update(lm.db_margin)
    window['-DBM_POWER-'].update(lm.dbm_power)
    window['-NULL_RATIO-'].Update(lm.null_ratio)
    window['-NULL_RATIO-BAR-'].UpdateBar(lm.null_ratio)
    window['-PROVIDER-'].update(lm.provider)
    window['-SERVICE-'].update(lm.service)
    window['-STATUS_BAR-'].update(lm.status_msg)

# MAIN ------------------------------------------

window = sg.Window('', layout, size=(800, 480), font=(None, 11), background_color=MYSCRCOLOR, use_default_focus=False, finalize=True)
window.set_cursor('none')

running = True

async def main_window():
    global running
    while running:
        event, values = window.read(timeout=10)
        if event == '-SHUTDOWN-':
            if sg.popup_yes_no('Shutdown Now?', background_color='red', keep_on_top=True) == 'Yes':
                lm.stop_longmynd()
                running = False
        if event in dispatch_dictionary:
            func_to_call = dispatch_dictionary[event]
            func_to_call()
        if bp.changed:
            update_control()
            bp.changed = False
        await asyncio.sleep(0)

async def read_lm_status():
    global running
    while running:
        lm.read_status()
        update_status()
        await asyncio.sleep(0)

async def main():
    await asyncio.gather(
        main_window(),
        read_lm_status(),
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
