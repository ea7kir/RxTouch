# gui.py

import PySimpleGUI as sg
import gui_formating as fmt

frequency = 12345678
symbol_rate = 333
mode = "mode"
constellation = 'constellation'
fec = '3/4'
codec_audio = "ACC"
codec_video = "H265"
db_mer = 7.2
db_margin = 3.4
dbm_power = 70
provider = "EA7KIR"
service = "service"

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

received_status_labels_layout =  [
            [text_label("Frequency")],
            [text_label("Symbol Rate")],
            [text_label("Mode")],
            [text_label('Constellation')],
            [text_label('FEC')],
            [text_label('Codecs')],
            [text_label('dB MER')],
            [text_label('dB Margin')],
            [text_label('dBm Power')],
            [text_label('Povider')],
            [text_label('Service')],
        ]

received_status_data_layout =  [
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

received_status_layout = [sg.Frame(' Received Status ',
    [
        [sg.Column(received_status_labels_layout), sg.Column(received_status_data_layout)]
    ],
    title_color = 'green',
    #border_color = 'green',
    #font = FRAME_TITLE_FONT, # for the title
    size = (225,340)
    )
]

buttons = [ [sg.Exit()],
]

layout = [
    [ received_status_layout ],
    [ sg.Column(buttons),]
]

window = sg.Window('', layout, size=(800, 480), finalize=True)

while True:
    event, values = window.read(timeout=100)
    if event in ('Shutdown','Exit'): # if user closes window or clicks cancel
        break
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

window.close()
print('Doing the shutdown sequence.')
