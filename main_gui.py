"""RxTouch"""

from multiprocessing import Process
from multiprocessing import Pipe

import threading
from time import sleep

import PySimpleGUI as sg
import control_status as cs

from process_spectrum import process_read_spectrum_data, SpectrumData
from process_longmynd import process_read_longmynd_data, LongmyndData
from process_video_ts import process_video_ts

from device_manager import configure_devices, shutdown_devices

""" LAYOUT FUNCTIONS ------------------------------ """

sg.theme('Black')
SCREEN_COLOR = '#111111'
NORMAL_BUTTON_COLOR = ('#FFFFFF','#222222')

def text_data(name, key):
    return sg.Text(name, size=11), sg.Text(' ', size=9, key=key, text_color='orange')

def incdec_but(name, key):
    return sg.Button(name, key=key, size=4, border_width=0, button_color=NORMAL_BUTTON_COLOR, mouseover_colors=NORMAL_BUTTON_COLOR)

def button_selector(key_down, value, key_up, width):
    return  incdec_but('<', key_down), sg.Text(' ', size=width, justification='center', key=value, text_color='orange'), incdec_but('>', key_up) 

""" LAYOUTS --------------------------------------- """

top_layout = [
    sg.Button('RxTouch', key='-SYSTEM-', border_width=0, button_color=NORMAL_BUTTON_COLOR, mouseover_colors=NORMAL_BUTTON_COLOR),
    sg.Text(' ', expand_x=True, key='-STATUS_BAR-', text_color='orange'),
    sg.Button('Shutdown', key='-SHUTDOWN-', border_width=0, button_color=NORMAL_BUTTON_COLOR, mouseover_colors=NORMAL_BUTTON_COLOR),    
]

spectrum_layout = [
    sg.Graph(canvas_size=(770, 240), graph_bottom_left=(0, 0x2000), graph_top_right=(918, 0xFFFF), background_color='black', float_values=False, key='graph'),
]

tune_layout = [
    sg.Column([
        button_selector('-BD-', '-BV-', '-BU-', 8),
    ]),
    sg.Column([
        button_selector('-SD-', '-SV-', '-SU-', 5),
    ]),
    sg.Column([
        button_selector('-FD-', '-FV-', '-FU-', 12),
    ]),
]

status_layout = [
    sg.Column([
        text_data('Frequency', '-FREQUENCY-'),
        text_data('Symbol Rate', '-SYMBOL_RATE-'),
        text_data('Mode', '-MODE-'),
        text_data('Constellation', '-CONSTELLATION-'),
    ], size=(210,120)),
    sg.Column([
        text_data('FEC', '-FEC-'),
        text_data('Codecs', '-CODECS-'),
        text_data('dB MER', '-DB_MER-'),
        text_data('dB Margin', '-DB_MARGIN-'),
    ], size=(210,120)),
    sg.Column([
        text_data('dBm Power', '-DBM_POWER-'),
    #    text_data('Null Ratio', '-NULL_RATIO-'),
    #    [sg.ProgressBar(100, orientation='h', size=(15, 5), key='-NULL_RATIO-BAR-', bar_color=('#00FF00','#111111'), expand_x=True)],
        [   sg.Text('Null Ratio', size=11), 
            sg.ProgressBar(100, orientation='h', size=(0,15), key='-NULL_RATIO-BAR-', bar_color=('#00FF00','#111111'), expand_x=True),
            sg.Text('',size=3, key='-NULL_RATIO-', text_color='orange', justification='right'),
        ],
        text_data('Provider', '-PROVIDER-'),
        text_data('Service', '-SERVICE-'),
    ], size=(210,120)),
    sg.Column([
        [sg.Button(' TUNE ', key='-TUNE-', border_width=0, button_color=NORMAL_BUTTON_COLOR, mouseover_colors=NORMAL_BUTTON_COLOR)],
        [sg.Text(' ')],
        [sg.Button(' MUTE ', key='-MUTE-', border_width=0, button_color=NORMAL_BUTTON_COLOR, mouseover_colors=NORMAL_BUTTON_COLOR)],
    ]),
]

layout = [
    top_layout,
    spectrum_layout,
    tune_layout,
    status_layout,
]

""" THREADS -------------------------------------- """

def spectrum_thread(window, pipe):
    while True:
        while pipe.poll():
            _ = pipe.recv()
            sleep(0)
            #print('dump spectrum data', flush= True)
        spectrum_data = pipe.recv()
        window.write_event_value('-SPECTRUM_THREAD-', (threading.current_thread().name, spectrum_data))

def longmynd_thread(window, pipe):
    while True:
        while pipe.poll():
            _ = pipe.recv()
            sleep(0)
            #print('dump longmynd data', flush= True)
        longmynd_data = pipe.recv()
        window.write_event_value('-LONGMYND_THREAD-', (threading.current_thread().name, longmynd_data))

""" MAIN ------------------------------------------ """

def main_gui(spectrum_pipe, longmynd_pipe):
    window = sg.Window('', layout, size=(800, 480), location=(0,0), no_titlebar=True, force_toplevel=True,
                       font=(None, 11), background_color=SCREEN_COLOR, use_default_focus=False, finalize=True)
    window.set_cursor('none')
    graph = window['graph']
    cs.longmynd_pipe = longmynd_pipe
    window['-TUNE-'].update(button_color=cs.tune_button_color)
    window['-MUTE-'].update(button_color=cs.mute_button_color)
    window['-BV-'].update(cs.curr_value.band)
    window['-FV-'].update(cs.curr_value.frequency)
    window['-SV-'].update(cs.curr_value.symbol_rate)
    window.refresh()

    threading.Thread(target=spectrum_thread, args=(window, spectrum_pipe), daemon=True).start()
    threading.Thread(target=longmynd_thread, args=(window, longmynd_pipe), daemon=True).start()

    while True:
        event, values = window.read()
        match event:
            case '-TUNE-':
                cs.tune()
                window['-TUNE-'].update(button_color=cs.tune_button_color)
            case '-MUTE-':
                cs.mute()
                window['-MUTE-'].update(button_color=cs.mute_button_color)
            case '-BD-':
                if cs.dec_band():
                    cs.cancel_tune()
                    window['-TUNE-'].update(button_color=cs.tune_button_color)
                    window['-BV-'].update(cs.curr_value.band)
                    window['-SV-'].update(cs.curr_value.symbol_rate)
                    window['-FV-'].update(cs.curr_value.frequency)
            case '-BU-':
                if cs.inc_band():
                    cs.cancel_tune()
                    window['-TUNE-'].update(button_color=cs.tune_button_color)
                    window['-BV-'].update(cs.curr_value.band)
                    window['-SV-'].update(cs.curr_value.symbol_rate)
                    window['-FV-'].update(cs.curr_value.frequency)
            case '-FD-':
                if cs.dec_frequency():
                    cs.cancel_tune()
                    window['-TUNE-'].update(button_color=cs.tune_button_color)
                    window['-FV-'].update(cs.curr_value.frequency)
            case '-FU-':
                if cs.inc_frequency():
                    cs.cancel_tune()
                    window['-TUNE-'].update(button_color=cs.tune_button_color)
                    window['-FV-'].update(cs.curr_value.frequency)
            case '-SD-':
                if cs.dec_symbol_rate():
                    cs.cancel_tune()
                    window['-TUNE-'].update(button_color=cs.tune_button_color)
                    window['-SV-'].update(cs.curr_value.symbol_rate)
            case '-SU-':
                if cs.inc_symbol_rate():
                    cs.cancel_tune()
                    window['-TUNE-'].update(button_color=cs.tune_button_color)
                    window['-SV-'].update(cs.curr_value.symbol_rate)
            case '-SHUTDOWN-':
                #if sg.popup_yes_no('Shutdown Now?', background_color='red', keep_on_top=True) == 'Yes':
                cs.cancel_tune()
                window['-TUNE-'].update(button_color=cs.tune_button_color)
                window['-STATUS_BAR-'].update('Shutting down...')
                window.refresh()
                sleep(5)
                break
            case '-SPECTRUM_THREAD-':
                spectrum_data = values['-SPECTRUM_THREAD-'][1]
                # TODO: try just deleting the polygon and beakcon_level with delete_figure(id)
                graph.erase()
                # draw graticule
                c = 0
                for y in range(0x2697, 0xFFFF, 0xD2D): # 0x196A, 0xFFFF, 0xD2D
                    if c == 5:
                        graph.draw_text('5dB', (13,y), color='#444444')
                        graph.draw_line((40, y), (918, y), color='#444444')
                    elif c == 10:
                        graph.draw_text('10dB', (17,y), color='#444444')
                        graph.draw_line((40, y), (918, y), color='#444444')
                    elif c == 15:
                        graph.draw_text('15dB', (17,y), color='#444444')
                        graph.draw_line((40, y), (918, y), color='#444444')
                    else:
                        graph.draw_line((0, y), (918, y), color='#222222')
                    c += 1
                # draw tuned marker
                x = cs.selected_frequency_marker()
                graph.draw_line((x, 0x2000), (x, 0xFFFF), color='#880000')
                # draw beacon level
                graph.draw_line((0, spectrum_data.beacon_level), (918, spectrum_data.beacon_level), color='#880000', width=1)
                # draw spectrum
                graph.draw_polygon(spectrum_data.points, fill_color='green')

                # MER in 720 x 240
                #graph.draw_text(window['-DB_MER-'].get(), (470, 0x8900), font=('bold',220), color='white')

            case '-LONGMYND_THREAD-':
                longmynd_data = values['-LONGMYND_THREAD-'][1]
                window['-FREQUENCY-'].update(longmynd_data.frequency)
                window['-SYMBOL_RATE-'].update(longmynd_data.symbol_rate)
                window['-MODE-'].update(longmynd_data.mode)
                window['-CONSTELLATION-'].update(longmynd_data.constellation)
                window['-FEC-'].update(longmynd_data.fec)
                window['-CODECS-'].update(longmynd_data.codecs)
                window['-DB_MER-'].update(longmynd_data.db_mer)
                window['-DB_MARGIN-'].update(longmynd_data.db_margin)
                window['-DBM_POWER-'].update(longmynd_data.dbm_power)
                window['-NULL_RATIO-'].Update(longmynd_data.null_ratio)
                window['-NULL_RATIO-BAR-'].UpdateBar(longmynd_data.null_ratio_bar)
                window['-PROVIDER-'].update(longmynd_data.provider)
                window['-SERVICE-'].update(longmynd_data.service)

    window.close()
    del window

if __name__ == '__main__':

    configure_devices()

    # TODO: consider using duplex=False

    parent_spectrum_pipe, child_spectrum_pipe = Pipe()
    parent_longmynd_pipe, child_longmynd_pipe = Pipe()
    # create the process
    p_read_spectrum_data = Process(target=process_read_spectrum_data, args=(child_spectrum_pipe,))
    p_read_longmynd_data = Process(target=process_read_longmynd_data, args=(child_longmynd_pipe,))
    # start the process
    p_read_spectrum_data.start()
    p_read_longmynd_data.start()
    # main ui
    main_gui(parent_spectrum_pipe, parent_longmynd_pipe)
    # kill 
    p_read_spectrum_data.kill()
    p_read_longmynd_data.kill()

    shutdown_devices()

    # shutdown
    print('about to shut down')
    #import subprocess
    #args = ['/usr/bin/sudo', 'poweroff']
    #subprocess.check_call(args)
