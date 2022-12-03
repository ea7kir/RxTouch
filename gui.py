# gui.py

import PySimpleGUI as sg
import gui_formating as fmt

frequency = 12345678
symbol_rate = 333
mode = "mode"
constellation = 'constellatio'
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

FRAME_TEXT_FONT = (None, 14)
FRAME_TITLE_FONT = (None, 14)


sg.theme('DarkGreen3')   # Add a touch of color

# All the stuff inside your window

received_status_labels_layout =  [
            [sg.Text("Frequency", font = FRAME_TEXT_FONT)],
            [sg.Text("Symbol Rate", font = FRAME_TEXT_FONT)],
            [sg.Text("Mode", font = FRAME_TEXT_FONT)],
            [sg.Text('Constellation', font = FRAME_TEXT_FONT)],
            [sg.Text('FEC', font = FRAME_TEXT_FONT)],
            [sg.Text('Codecs', font = FRAME_TEXT_FONT)],
            [sg.Text('dB MER', font = FRAME_TEXT_FONT)],
            [sg.Text('dB Margin', font = FRAME_TEXT_FONT)],
            [sg.Text('dBm Power', font = FRAME_TEXT_FONT)],
            [sg.Text('Povider', font = FRAME_TEXT_FONT)],
            [sg.Text('Service', font = FRAME_TEXT_FONT)],
        ]

received_status_data_layout =  [
            [sg.Text(font = FRAME_TEXT_FONT, key='-FREQUENCY-')],
            [sg.Text(font = FRAME_TEXT_FONT, key='-SYMBOL_RATE-')],
            [sg.Text(font = FRAME_TEXT_FONT, key='-MODE-')],
            [sg.Text(font = FRAME_TEXT_FONT, key='-CONSTELLATION-')],
            [sg.Text(font = FRAME_TEXT_FONT, key='-FEC-')],
            [sg.Text(font = FRAME_TEXT_FONT, key='-CODECS-')],
            [sg.Text(font = FRAME_TEXT_FONT, key='-DB_MER-')],
            [sg.Text(font = FRAME_TEXT_FONT, key='-DB_MARGIN-')],
            [sg.Text(font = FRAME_TEXT_FONT, key='-DBM_POWER-')],
            [sg.Text(font = FRAME_TEXT_FONT, key='-PROVIDER-')],
            [sg.Text(font = FRAME_TEXT_FONT, key='-SERVICE-')],
        ]

received_status_layout = [sg.Frame('Received Status',
    [
        [sg.Column(received_status_labels_layout), sg.Column(received_status_data_layout)]
    ],
    font = FRAME_TITLE_FONT, # for the title
    size = (220,335)
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
    event, values = window.read(timeout=10)
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
