# gui.py

import PySimpleGUI as sg
import gui_formating as fmt
from bandplan import band_plan as bp
from lm_functions import lm_status_available, read_lm_status, start_longmynd, stop_longmynd, longmynd_running

# ------------------------------------------------

# The callback functions

def tune():
    start_longmynd(bp.frequency, bp.symbol_rate)


# Lookup dictionary that maps button to function to call
dispatch_dictionary = { 
    '-BD-':bp.dec_band, '-BU-':bp.inc_band, 
    '-FD-':bp.dec_frequency, '-FU-':bp.inc_frequency, 
    '-SD-':bp.dec_symbol_rate, '-SU-':bp.inc_symbol_rate,
    '-TUNE-':tune,
}

# ------------------------------------------------

def text_data(name, key):
    FONT = (None,11); SIZE=(15,1)
    return [ sg.Text(' '), sg.Text(name, size=SIZE), sg.Text('', key=key, text_color='orange', font=FONT) ]

def incdec_but(name, key):
    return sg.Button(name, key=key, size=(4,1), font=(None,13))

def button_selector(key_down, value, key_up):
    return [ incdec_but('<', key_down), sg.Push(), sg.Text('', key=value, text_color='orange', font=(None,13)), sg.Push(), incdec_but('>', key_up) ]


# ------------------------------------------------


sg.theme('Black')

# layouts

# ------------------------------------------------

control_layout = [
    [sg.Push(), sg.Text('Band', text_color='green'), sg.Push()],
    button_selector('-BD-', '-BV-', '-BU-'),
    [sg.Push(), sg.Text('Channel / Frequency', text_color='green'), sg.Push()],
    button_selector('-FD-', '-FV-', '-FU-'),
    [sg.Push(), sg.Text('Symbol Rate', text_color='green'), sg.Push()],
    button_selector('-SD-', '-SV-', '-SU-'),
    [sg.Text('')],
    [sg.Push(), sg.Button('TUNE', key='-TUNE-'), sg.Push() ],
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
        control_layout, title_color='green', size=(355,340), pad=(15,15)),
        
        sg.Frame('Received Status',
        status_layout, title_color='green', size=(355,340), pad=(15,15) ),
    ],
    [sg.Text('')],
    [sg.Push(), sg.Button('Shutdown', key='-SHUTDOWN-', font=(None,11))],
]

window = sg.Window('', layout, size=(800, 480), font=(None, 11), button_color='grey', use_default_focus=False, finalize=True)
    #default_button_element_size=(15,2), auto_size_buttons=False, use_default_focus=False)
#window.set_cursor('none')


while True:
    event, values = window.read(timeout=100)
    if event == '-SHUTDOWN-':
        if sg.popup_ok_cancel('Shutdown Now?', font=(None,11), background_color='red',
                    #no_titlebar=True, keep_on_top=True) == 'OK':
                    keep_on_top=True) == 'OK':
            break

    if event in dispatch_dictionary:
        func_to_call = dispatch_dictionary[event]
        func_to_call()

    if bp.changed:
            window['-BV-'].update(bp.band)
            window['-FV-'].update(bp.frequency)
            window['-SV-'].update(bp.symbol_rate)
            bp.changed = False

    if lm_status_available:
        lm_status = read_lm_status()
        window['-FREQUENCY-'].update(fmt.frequency(lm_status.frequency))
        window['-SYMBOL_RATE-'].update(fmt.symbol_rate(lm_status.symbol_rate))
        window['-MODE-'].update(fmt.mode(lm_status.mode))
        window['-CONSTELLATION-'].update(fmt.constellation(lm_status.constellation))
        window['-FEC-'].update(fmt.fec(lm_status.fec))
        window['-CODECS-'].update(fmt.codecs(lm_status.codecs))
        window['-DB_MER-'].update(fmt.db_mer(lm_status.db_mer))
        window['-DB_MARGIN-'].update(fmt.db_margin(lm_status.db_margin))
        window['-DBM_POWER-'].update(fmt.dbm_power(lm_status.dbm_power))
        window['-PROVIDER-'].update(fmt.provider(lm_status.provider))
        window['-SERVICE-'].update(fmt.service(lm_status.service))

window.close(); del window

stop_longmynd()
print('about to shutdown')
#import subprocess
#subprocess.check_call(['sudo', 'poweroff'])

