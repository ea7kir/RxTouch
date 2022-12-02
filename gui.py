# gui.py

import PySimpleGUI as sg

frequency = '00000.000'
symbol_rate = '-'
mode = '-'
constelation = '-'
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
            [sg.Text(size=(12,1), key='-CONSTELATION-')],
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
        [ sg.Column(labels),
          sg.Column(values), 
          sg.Column(buttons),]
]


# Create the Window
#window = sg.Window('', layout, no_titlebar=True, location=(0,0), size=(800, 480), keep_on_top=True)
window = sg.Window('', layout, size=(800, 480), finalize=True)
#window.Maximize()
#window = sg.Window('Window Title', layout, resizable=True)
#window = sg.Window('Window', [[]], no_titlebar=True, location=(0,0), size=(800,480), keep_on_top=True).Finalize()

# Event Loop to process "events" and get the "values" of the inputs
while True:
    event, values = window.read(timeout=10)
    if event in ('Shutdown','Exit'): # if user closes window or clicks cancel
        break
    window['-FREQUENCY-'].update(frequency)
    window['-SYMBOL_RATE-'].update(symbol_rate)
    window['-MODE-'].update(mode)
    window['-CONSTELATION-'].update(constelation)
    window['-FEC-'].update(fec)
    window['-CODECS-'].update(codecs)
    window['-DB_MER-'].update(db_mer)
    window['-DB_MARGIN-'].update(db_margin)
    window['-DBM_POWER-'].update(dbm_power)
    window['-PROVIDER-'].update(provider)
    window['-SERVICE-'].update(service)

window.close()
print('Doing the shutdown sequence.')

"""
FROM: https://www.pysimplegui.org/en/latest/#persistent-window-example-running-timer-that-updates

FORMATING EG:

window['text'].update('{:02d}:{:02d}.{:02d}'.format((current_time // 100) // 60,
                                                                  (current_time // 100) % 60,
                                                                  current_time % 100))

"""
