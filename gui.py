# gui.py

import PySimpleGUI as sg
import gui_formating as fmt
from defs import shutdown, activate_longmynd
from bandplan import RX_FREQUENCY_LIST, SYMBOL_RATE_LIST
from lm_functions import lm_data_dict

def text_label(name):
    return sg.Text(name, font=(None, 11))

def data_field(key):
    return sg.Text('', key=key, text_color='orange', font=(None, 11))

sg.theme('Black')

# layouts

# ------------------------------------------------

control_labels_layout = [
    [text_label('Frequency')],
    [text_label('Symbol Rate')],
]

control_data_layout = [
    # frequency
    [sg.Combo(RX_FREQUENCY_LIST)],
    # symbol rate
    [sg.Combo(SYMBOL_RATE_LIST)],
    [sg.Button('Activate')]
]

# ------------------------------------------------

status_labels_layout =  [
            [text_label('Frequency')],
            [text_label('Symbol Rate')],
            [text_label('Mode')],
            [text_label('Constellation')],
            [text_label('FEC')],
            [text_label('Codecs')],
            [text_label('dB MER')],
            [text_label('dB Margin')],
            [text_label('dBm Power')],
            [text_label('Provider')],
            [text_label('Service')],
        ]

status_data_layout =  [
            [data_field('-FREQUENCY-')],
            [data_field('-SYMBOL_RATE-')],
            [data_field('-MODE-')],
            [data_field('-CONSTELLATION-')],
            [data_field('-FEC-')],
            [data_field('-CODECS-')],
            [data_field('-DB_MER-')],
            [data_field('-DB_MARGIN-')],
            [data_field('-DBM_POWER-')],
            [data_field('-PROVIDER-')],
            [data_field('-SERVICE-')],
        ]

# ------------------------------------------------

buttons = [ [sg.Button('Shutdown')],
]

# ------------------------------------------------

layout = [
    [sg.Frame('Receiver Controls',
        [
            [sg.Column(control_labels_layout), sg.Column(control_data_layout)]
        ],
        title_color = 'green',
        size = (350,340),
        pad = (15, 15)
        ),
        
        sg.Frame('Received Status',
        [
            [sg.Column(status_labels_layout), sg.Column(status_data_layout)]
        ],
        title_color = 'green',
        size = (350,340),
        pad = (15, 15)
        ),
    ],
    [ sg.Column(buttons) ],
]

# ------------------------------------------------

window = sg.Window('', layout, size=(800, 480), finalize=True)

while True:
    event, values = window.read(timeout=100)
    if event in ('Shutdown','Exit'): # if user closes window or clicks cancel
        break
    if event == 'Activate':
        activate_longmynd()
    data_dict = lm_data_dict()
    window['-FREQUENCY-'].update(fmt.frequency(data_dict['-FREQUENCY-']))
    window['-SYMBOL_RATE-'].update(fmt.symbol_rate(data_dict['-SYMBOL_RATE-']))
    window['-MODE-'].update(fmt.mode(data_dict['-MODE-']))
    window['-CONSTELLATION-'].update(fmt.constellation(data_dict['-CONSTELLATION-']))
    window['-FEC-'].update(fmt.fec(data_dict['-FEC-']))
    window['-CODECS-'].update(fmt.codecs(data_dict['-CODECS-']))
    window['-DB_MER-'].update(fmt.db_mer(data_dict['-DB_MER-']))
    window['-DB_MARGIN-'].update(fmt.db_margin(data_dict['-DB_MARGIN-']))
    window['-DBM_POWER-'].update(fmt.dbm_power(data_dict['-DBM_POWER-']))
    window['-PROVIDER-'].update(fmt.provider(data_dict['-PROVIDER-']))
    window['-SERVICE-'].update(fmt.service(data_dict['-SERVICE-']))

window.close(); del window
shutdown()
