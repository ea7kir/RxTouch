# gui.py

import PySimpleGUI as sg
import gui_formating as fmt
from defs import shutdown, activate_longmynd
from bandplan import RX_FREQUENCY_LIST, SYMBOL_RATE_LIST
from lm_functions import lm_status_available, read_lm_status

# ------------------------------------------------

# The callback functions
def band_down():
    print('band_down callback')

def band_up():
    print('band_up callback')

def freq_down():
    print('freq_down callback')

def freq_up():
    print('freq_up callback')

def sr_down():
    print('sr_down callback')

def sr_up():
    print('sr_up callback')

def tune():
    print('tune callback')

def pre_shutdown():
    print('pre_shutdown callback')

def timeout():
    pass

# Lookup dictionary that maps button to function to call
dispatch_dictionary = { 
    '-BD-':band_down, '-BU-':band_up, 
    '-FD-':freq_down, '-FU-':freq_up, 
    '-SD-':sr_down, '-SU-':sr_up, 
    '-TUNE-':tune #, '-SHUTDOWN-':pre_shutdown, '-TIMEOUT-':timeout
}

# ------------------------------------------------

def text_data(name, key):
    FONT = (None,11); SIZE=(15,1)
    return [ sg.Text(' '), sg.Text(name, size=SIZE, font=FONT), sg.Text('', key=key, text_color='orange', font=FONT) ]

def text_combo(name, values):
    FONT = (None,11); SIZE=(15,None)
    return [ sg.Text(' '), sg.Text(name, size=SIZE, font=FONT), sg.Combo(values, size=SIZE, font=FONT) ]

def text_button(name, b_name):
    FONT = (None,11); SIZE=(15,2)
    return [ sg.Text(' '), sg.Text(name, size=SIZE, font=FONT), sg.Button(b_name, size=SIZE, font=FONT) ]

def my_button(name, key):
    #FONT = (None,11); SIZE=(5,2)
    return sg.Button(name, key=key, size=(5,2), font=(None,11))

def button_selector(key_down, key_text, key_up):
    #FONT = (None,11); SIZE=(15,1)
    return [ my_button('<', key_down), sg.Push(), sg.Text('V.Narrow', key=key_text, font=(None,18)), sg.Push(), my_button('>', key_up) ]


# ------------------------------------------------


sg.theme('Black')

# layouts

# ------------------------------------------------

control_layout = [
    #text_combo('Frequency', RX_FREQUENCY_LIST),
    #text_combo('Symbol Rate', SYMBOL_RATE_LIST),
    #text_button('Minitiouner', 'Tune'),
    [sg.Text('Band')],
    button_selector('-BD-', '-BT-', '-BU-'),
    [sg.Text('Channel Frequency')],
    button_selector('-FD-', 'FT', '-FU-'),
    [sg.Text('Symbol Rate')],
    button_selector('-SD-', 'ST', '-SU-'),
    [sg.Text('')],
    [sg.Button('TUNE', key='-TUNE-', font=(None,11), size=(15,2))],
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

buttons = [
    [sg.Button('Shutdown', key='-SHUTDOWN-', font=(None,11), size=(15,2))],
]

# ------------------------------------------------

layout = [
    [sg.Frame('Receiver Controls',
        control_layout, title_color='green', size=(355,340), pad=(15,15)),
        
        sg.Frame('Received Status',
        status_layout, title_color='green', size=(355,340), pad=(15,15) ),
    ],
    [ sg.Column(buttons) ],
]

window = sg.Window('', layout, size=(800, 480), use_default_focus=False, finalize=True)
    #default_button_element_size=(15,2), auto_size_buttons=False, use_default_focus=False)
#window.set_cursor('none')


while True:
    event, values = window.read(timeout=100)
    if event == '-SHUTDOWN-':
        break

    if event in dispatch_dictionary:
        func_to_call = dispatch_dictionary[event]   # get function from dispatch dictionary
        func_to_call()
#    else:
#        print('Event {} not in dispatch dictionary'.format(event))

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
shutdown()
