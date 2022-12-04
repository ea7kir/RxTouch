# gui.py

import PySimpleGUI as sg
import gui_formating as fmt

frequency = 10491551
symbol_rate = 1500
mode = 'Locked DVB-S2'
constellation = 'QPSK'
fec = '4/5'
codec_video = 'H264'
codec_audio = 'MP3'
db_mer = 78.9
db_margin = 4.1
dbm_power = -60
provider = 'A71A'
service = 'QARS'

def readLongmydBuffer():
    frequency = 12345678 #'00000.000'
    symbol_rate = '-'
    mode = '-'
    constellation = '-'
    fec = '-/-'
    codecs = '- -'
    db_mer = '-.-'
    db_margin = 'D -.-'
    dbm_power = '---'
    provider = '-'
    service = '-'

def text_label(name):
    return sg.Text(name, font=(None, 11))

def data_field(key):
    return sg.Text('', key=key, text_color='orange', font=(None, 11))

sg.theme('Black')

# All the stuff inside your window

# ------------------------------------------------

control_labels_layout = [
    [text_label('Frequency')],
    [text_label('Symbol Rate')],
]

control_data_layout = [
    # frequency
    [sg.Combo(['2400.00','2400.00','2400.00','2400.00'])],
    # symbol rate
    [sg.Combo(['250','333','500'])],
    [sg.Button('Activate')]
]
'''
control_layout = [sg.Frame('Control Panel',
    [
        [sg.Column(control_labels_layout), sg.Column(control_data_layout)]
    ],
    title_color = 'green',
    size = (225,340),
    )
]
'''
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
            [text_label('Povider')],
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

'''
status_layout = [sg.Frame(' Received Status ',
    [
        [sg.Column(status_labels_layout), sg.Column(status_data_layout)]   
    ],
    title_color = 'green',
    #border_color = 'green',
    #font = FRAME_TITLE_FONT, # for the title
    size = (225,340),
    )
]
'''
# ------------------------------------------------

buttons = [ [sg.Button('Shutdown')],
]

layout = [
    [sg.Frame('Receiver Controls',
        [
            [sg.Column(control_labels_layout), sg.Column(control_data_layout)]
        ],
        title_color = 'green',
        size = (300,340),
        ),
        
        sg.Frame('Received Status',
        [
            [sg.Column(status_labels_layout), sg.Column(status_data_layout)]
        ],
        title_color = 'green',
        size = (225,340),
        ),
    ],
    [ sg.Column(buttons) ],

]

window = sg.Window('', layout, size=(800, 480), finalize=True)

def update_all():
    window['-FREQUENCY-'].update(fmt.frequency(frequency))
    window['-SYMBOL_RATE-'].update(fmt.symbol_rate(symbol_rate))
    window['-MODE-'].update(fmt.mode(mode))
    window['-CONSTELLATION-'].update(fmt.constellation(constellation))
    window['-FEC-'].update(fmt.fec(fec))
    window['-CODECS-'].update(fmt.codecs(codec_audio,codec_video))
    window['-DB_MER-'].update(fmt.db_mer(db_mer))
    window['-DB_MARGIN-'].update(fmt.db_margin(db_margin))
    window['-DBM_POWER-'].update(fmt.dbm_power(dbm_power))
    window['-PROVIDER-'].update(fmt.provider(provider))
    window['-SERVICE-'].update(fmt.service(service))

while True:
    event, values = window.read(timeout=100)
    if event in ('Shutdown','Exit'): # if user closes window or clicks cancel
        break
    update_all()

window.close()
print('Doing the shutdown sequence.')
