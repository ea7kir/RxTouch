"""RxTouch"""

import PySimpleGUI as sg
import asyncio
from bandplan import bandplan as bp
from longmynd_manager import longmynd_manager as lm

# LAYOUT ----------------------------------------

sg.theme('Black')

MYBUTCOLORS = ('#FFFFFF','#222222')
MYDISABLEDBTCOLORS = ('#444444',None)

def text_data(name, key):
    return [ sg.Text(' '), sg.Text(name, size=(15,1)), sg.Text('', key=key, text_color='orange', font=(None,11)) ]

def incdec_but(name, key):
    return sg.Button(name, key=key, size=(4,1), font=(None,13), border_width=0, button_color=MYBUTCOLORS, mouseover_colors=MYBUTCOLORS)

def button_selector(key_down, value, key_up):
    return [ incdec_but('<', key_down), sg.Push(), sg.Text('', key=value, text_color='orange', font=(None,13)), sg.Push(), incdec_but('>', key_up) ]

control_layout = [
    [sg.Push(), sg.Text('Band', text_color='green'), sg.Push()],
    button_selector('-BD-', '-BV-', '-BU-'),
    [sg.Push(), sg.Text('Frequency / Channel', text_color='green'), sg.Push()],
    button_selector('-FD-', '-FV-', '-FU-'),
    [sg.Push(), sg.Text('Symbol Rate', text_color='green'), sg.Push()],
    button_selector('-SD-', '-SV-', '-SU-'),
    [sg.Text('')],
    [sg.Push(), sg.Button('TUNE', key='-TUNE-', border_width=0, button_color=MYBUTCOLORS, mouseover_colors=MYBUTCOLORS, disabled_button_color=MYDISABLEDBTCOLORS, disabled=False), sg.Push()],
]

top_layout = [
    sg.Button('RxTouch', key='-SYSTEM-', border_width=0, button_color=MYBUTCOLORS, mouseover_colors=MYBUTCOLORS),
    sg.Text('', key='-STATUS_BAR-', text_color='green'),
    sg.Push(),
    sg.Button('Shutdown', key='-SHUTDOWN-', border_width=0, button_color=MYBUTCOLORS, mouseover_colors=MYBUTCOLORS),    
]

status_layout = [
    text_data('Frequency', '-FREQUENCY-'),
    text_data('Symbol Rate', '-SYMBOL_RATE-'),
    text_data('Mode', '-MODE-'),
    text_data('Constellation', '-CONSTELLATION-'),
    text_data('FEC', '-FEC-'),
    text_data('Codecs', '-CODECS-'),
    text_data('dB MER', '-DB_MER-'),
    text_data('dB Margin', '-DB_MARGIN-'),
    text_data('dBm Power', '-DBM_POWER-'),
    text_data('Null Ratio', '-NULL_RATIO-'),
    [sg.ProgressBar(100, orientation='h', size=(10, 10), key='-NULL_RATIO-BAR-', bar_color=('#00FF00','#111111'))],
    text_data('Provider', '-PROVIDER-'),
    text_data('Service', '-SERVICE-'),
]

layout = [
    top_layout,
    [
        sg.Frame(' Receiver Control ',
        control_layout, title_color='green', size=(340,340), pad=(15,15) ),
        sg.Frame(' Received Status ',
        status_layout, title_color='green', size=(340,400), pad=(15,15) ),
    ],
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

window = sg.Window('', layout, size=(800, 480), font=(None,11), use_default_focus=False, finalize=True)
window.set_cursor('none')

running = True

async def main_window():
    global running
    while running:
        event, values = window.read(timeout=10)
        if event == '-SHUTDOWN-':
            if sg.popup_yes_no('Shutdown Now?', font=(None,11), background_color='red', keep_on_top=True) == 'Yes':
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
