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
provider = "ËA7KIR"
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
    

sg.theme('DarkGreen3')   # Add a touch of color
# All the stuff inside your window.

labels = [  [sg.Text('Frequency')],
            [sg.Text('Symbol Rate')],
            [sg.Text('Mode')],
            [sg.Text('Constellation')],
            [sg.Text('FEC')],
            [sg.Text('Codecs')],
            [sg.Text('dB MER')],
            [sg.Text('dB Margin')],
            [sg.Text('dBm Power')],
            [sg.Text('Povider')],
            [sg.Text('Service')],
]

values = [  [sg.Text(size=(12,1), key='-FREQUENCY-')],
            [sg.Text(size=(12,1), key='-SYMBOL_RATE-')],
            [sg.Text(size=(12,1), key='-MODE-')],
            [sg.Text(size=(12,1), key='-CONSTELLATION-')],
            [sg.Text(size=(12,1), key='-FEC-')],
            [sg.Text(size=(12,1), key='-CODECS-')],
            [sg.Text(size=(12,1), key='-DB_MER-')],
            [sg.Text(size=(12,1), key='-DB_MARGIN-')],
            [sg.Text(size=(12,1), key='-DBM_POWER-')],
            [sg.Text(size=(12,1), key='-PROVIDER-')],
            [sg.Text(size=(12,1), key='-SERVICE-')],
]

buttons = [ [sg.Exit()],
]

layout = [
    [ sg.Column(labels), sg.Column(values), sg.Column(buttons),]
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
