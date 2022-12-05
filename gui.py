# gui.py

import PySimpleGUI as sg
import gui_formating as fmt
from defs import shutdown, activate_longmynd
from bandplan import RX_FREQUENCY_LIST, SYMBOL_RATE_LIST
from lm_functions import lm_status_available, read_lm_status

def xxx_text_label(name):
    return sg.Text(name, font=(None, 11))

def xxx_data_field(key):
    return sg.Text('', key=key, text_color='orange', font=(None, 11))

def data_field2(name, key):
    FONT = (None,11); SIZE=(15,1)
    return [ sg.Text(' '), sg.Text(name, size=SIZE, font=FONT), sg.Text('', key=key, text_color='orange', font=FONT) ]

def data_combo(name, values, width):
    FONT = (None,11); SIZE=(15,1)
    return [ sg.Text(' '), sg.Text(name, size=SIZE, font=FONT), sg.Combo(values, size=SIZE, font=FONT) ]

sg.theme('Black')

# layouts

# ------------------------------------------------

control_layout = [
    data_combo('Frequency', RX_FREQUENCY_LIST, 10),
    data_combo('Symbol Rate', SYMBOL_RATE_LIST, 10),
]

# ------------------------------------------------

status_layout = [
    data_field2('Frequency', '-FREQUENCY-'),
    data_field2('Symbol Rate', '-SYMBOL_RATE-'),
    data_field2('Mode', '-MODE-'),
    data_field2('Constellation', '-CONSTELLATION-'),
    data_field2('FEC', '-FEC-'),
    data_field2('Codecs', '-CODECS-'),
    data_field2('dB MER', '-DB_MER-'),
    data_field2('dB Margin', '-DB_MARGIN-'),
    data_field2('dBm Power', '-DBM_POWER-'),
    data_field2('Provider', '-PROVIDER-'),
    data_field2('Service', '-SERVICE-'),
]

# ------------------------------------------------

buttons = [
    [sg.Button('Shutdown')],
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

window = sg.Window('', layout, size=(800, 480), finalize=True)

while True:
    event, values = window.read(timeout=100)
    if event in ('Shutdown','Exit'): # if user closes window or clicks cancel
        break
    if event == 'Activate':
        activate_longmynd()
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
