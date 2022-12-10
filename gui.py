# gui.py

import PySimpleGUI as sg
#import gui_formating as fmt
from bandplan import band_plan as bp
from lm_manager import lm_manager as lm

# The callback functions

def tune():
    frequency, rate_list = bp.fequency_and_rate_list()
    lm.start_longmynd(frequency, rate_list)

# Lookup dictionary that maps button to function to call
dispatch_dictionary = { 
    '-BD-':bp.dec_band, '-BU-':bp.inc_band, 
    '-FD-':bp.dec_frequency, '-FU-':bp.inc_frequency, 
    '-SD-':bp.dec_symbol_rate, '-SU-':bp.inc_symbol_rate,
    '-TUNE-':tune,
}

# ------------------------------------------------

MYBUTCOLORS = ('#FFFFFF','#222222')
MYDISABLEDBTCOLORS = ('#444444',None)

def text_data(name, key):
    return [ sg.Text(' '), sg.Text(name, size=(15,1)), sg.Text('', key=key, text_color='orange', font=(None,11)) ]

def incdec_but(name, key):
    return sg.Button(name, key=key, size=(4,1), font=(None,13), border_width=0, button_color=MYBUTCOLORS, mouseover_colors=MYBUTCOLORS)

def button_selector(key_down, value, key_up):
    return [ incdec_but('<', key_down), sg.Push(), sg.Text('', key=value, text_color='orange', font=(None,13)), sg.Push(), incdec_but('>', key_up) ]

# ------------------------------------------------

sg.theme('Black')

# layouts

# ------------------------------------------------

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

# ------------------------------------------------

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
    text_data('Provider', '-PROVIDER-'),
    text_data('Service', '-SERVICE-'),
]
# ------------------------------------------------

layout = [
    [sg.Frame('Receiver Controls',
        control_layout, title_color='green', size=(340,340), pad=(15,15) ),
        
        sg.Frame('Received Status',
        status_layout, title_color='green', size=(340,340), pad=(15,15) ),
    ],
    [sg.Push(), sg.Button('Shutdown', key='-SHUTDOWN-', font=(None,11))],
    [sg.Text('', key='-STATUS_BAR-', text_color='green')],
]

window = sg.Window('', layout, size=(800, 480), font=(None,11), use_default_focus=False, finalize=True)
    
window.set_cursor('none')

while True:
    event, values = window.read(timeout=10)
    if event == '-SHUTDOWN-':
        if sg.popup_ok_cancel('Shutdown Now?', font=(None,15), background_color='red',
                    #no_titlebar=True, keep_on_top=True) == 'OK':
                    keep_on_top=True) == 'OK':
            lm.stop_longmynd()
            break

    if event in dispatch_dictionary:
        func_to_call = dispatch_dictionary[event]
        func_to_call()

    if bp.changed:
            window['-BV-'].update(bp.band)
            window['-FV-'].update(bp.frequency)
            window['-SV-'].update(bp.symbol_rate)
            bp.changed = False

#    if lm.status_available:
    lm_status = lm.read_status()
    window['-FREQUENCY-'].update(lm.frequency)
    window['-SYMBOL_RATE-'].update(lm.symbol_rate)
    window['-MODE-'].update(lm.mode)
    window['-CONSTELLATION-'].update(lm.constellation)
    window['-FEC-'].update(lm.fec)
    window['-CODECS-'].update(lm.codecs)
    window['-DB_MER-'].update(lm.db_mer)
    window['-DB_MARGIN-'].update(lm.db_margin)
    window['-DBM_POWER-'].update(lm.dbm_power)
    window['-PROVIDER-'].update(lm.provider)
    window['-SERVICE-'].update(lm.service)
    window['-STATUS_BAR-'].update(lm.status_msg)

window.close()
del window

print('about to shutdown')
#import subprocess
#subprocess.check_call(['sudo', 'poweroff'])
