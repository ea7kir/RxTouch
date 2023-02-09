"""RxTouch"""

from multiprocessing import Process
from multiprocessing import Pipe
from time import sleep

import PySimpleGUI as sg
import control_status as cs

from process_spectrum import process_read_spectrum_data, SpectrumData
from process_longmynd import process_read_longmynd_data, LongmyndData
from process_video_ts import process_video_ts

# LAYOUT ----------------------------------------

sg.theme('Black')

SCREEN_COLOR = '#111111'
NORMAL_BUTTON_COLOR = ('#FFFFFF','#222222')
DISABALED_BUTTON_COLOR = ('#444444',None)
TUNE_ACTIVE_BUTTON_COLOR = ('#FFFFFF','#007700')
MUTE_ACTIVE_BUTTON_COLOR = ('#FFFFFF','#FF0000')

def text_data(name, key):
    return sg.Text(name, size=11), sg.Text(' ', size=9, key=key, text_color='orange')

def incdec_but(name, key):
    return sg.Button(name, key=key, size=4, border_width=0, button_color=NORMAL_BUTTON_COLOR, mouseover_colors=NORMAL_BUTTON_COLOR)

def button_selector(key_down, value, key_up, width):
    return  incdec_but('<', key_down), sg.Text(' ', size=width, justification='center', key=value, text_color='orange'), incdec_but('>', key_up) 

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
        [sg.Button(' TUNE ', key='-TUNE-', border_width=0, button_color=NORMAL_BUTTON_COLOR, mouseover_colors=NORMAL_BUTTON_COLOR, disabled_button_color=DISABALED_BUTTON_COLOR, disabled=False)],
        [sg.Text(' ')],
        [sg.Button(' MUTE ', key='-MUTE-', border_width=0, button_color=NORMAL_BUTTON_COLOR, mouseover_colors=NORMAL_BUTTON_COLOR, disabled_button_color=DISABALED_BUTTON_COLOR, disabled=False)],
    ]),
]

layout = [
    top_layout,
    spectrum_layout,
    tune_layout,
    status_layout,
]

# CALLBACK DISPATCH -----------------------------

def display_initial_values():
    # fix to display initial controll values
    pass

dispatch_dictionary = {
    # Lookup dictionary that maps button to function to call
    # NOTE: the order could affect responsiveness, but maybe a disctionary lookup is just too slow
    #'-TUNE-':cs.tune,
    #'-MUTE-':cs.mute,
    '-BD-':cs.dec_band, '-BU-':cs.inc_band, 
    '-FD-':cs.dec_frequency, '-FU-':cs.inc_frequency, 
    '-SD-':cs.dec_symbol_rate, '-SU-':cs.inc_symbol_rate,
    '-DISPLAY_INITIAL_VALUES-':display_initial_values,
}

# MAIN ------------------------------------------

def main_gui(spectrum_pipe, longmynd_pipe):
    window = sg.Window('', layout, size=(800, 480), font=(None, 11), background_color=SCREEN_COLOR, use_default_focus=False, finalize=True)
    window.set_cursor('none')
    graph = window['graph']
    tune_active = False
    mute_active = False
    # fix to display initial controll values
    window.write_event_value('-DISPLAY_INITIAL_VALUES-', None)
    while True:
        event, values = window.read(timeout=100)
        if event == '__TIMEOUT__':
            if spectrum_pipe.poll():
                spectrum_data = spectrum_pipe.recv()
                while spectrum_pipe.poll():
                    _ = spectrum_pipe.recv()
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
            if longmynd_pipe.poll():
                longmynd_data = longmynd_pipe.recv()
                while longmynd_pipe.poll():
                    _ = longmynd_pipe.recv()
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
                window['-STATUS_BAR-'].update(longmynd_data.status_msg)
        else: # don't bother searching for __TIMEOUT__ events
            if event == '-SHUTDOWN-':
                #if sg.popup_yes_no('Shutdown Now?', background_color='red', keep_on_top=True) == 'Yes':
                longmynd_pipe.send('STOP') # NOTE: maybe this needs time to complete
                window['-STATUS_BAR-'].update(longmynd_data.status_msg)
                # TODO: a delay is neccessary, but I need to find a better way
                #       or dind a way to know when kill has completed
                sleep(1.5)
                break
# TODO: move tune and mute to control_status
            if event == '-TUNE-':
                tune_active = not tune_active # move this to get auto beacon at startup
                if tune_active:
                    window['-TUNE-'].update(button_color=TUNE_ACTIVE_BUTTON_COLOR)
                    tune_args = cs.tune_args()
                    longmynd_pipe.send(tune_args)
                else:
                    window['-TUNE-'].update(button_color=NORMAL_BUTTON_COLOR)
                    longmynd_pipe.send('STOP')
            if event == '-MUTE-':
                mute_active = not mute_active
                if mute_active:
                    window['-MUTE-'].update(button_color=MUTE_ACTIVE_BUTTON_COLOR)
                else:
                    window['-MUTE-'].update(button_color=NORMAL_BUTTON_COLOR)
            if event in dispatch_dictionary:
                func_to_call = dispatch_dictionary[event]
                func_to_call()
                window['-BV-'].update(cs.curr_value.band)
                window['-FV-'].update(cs.curr_value.frequency)
                window['-SV-'].update(cs.curr_value.symbol_rate)
                #window['-TUNE-'].update(button_color=cs.tune_button_color)
                #window['-MUTE-'].update(button_color=cs.mute_button_color)

    window.close()
    del window

if __name__ == '__main__':
    parent_spectrum_pipe, child_spectrum_pipe = Pipe()
    parent_longmynd_pipe, child_longmynd_pipe = Pipe()
    parent_video_ts_pipe, child_video_ts_pipe = Pipe()
    # create the process
    p_read_spectrum_data = Process(target=process_read_spectrum_data, args=(child_spectrum_pipe,))
    p_read_longmynd_data = Process(target=process_read_longmynd_data, args=(child_longmynd_pipe,))
    p_process_video_ts = Process(target=process_video_ts, args=(child_video_ts_pipe,))
    # start the process
    p_read_spectrum_data.start()
    p_read_longmynd_data.start()
    p_process_video_ts.start()
    # main ui
    main_gui(parent_spectrum_pipe, parent_longmynd_pipe)
    # kill 
    p_read_spectrum_data.kill()
    p_read_longmynd_data.kill()
    p_process_video_ts.kill()
    # shutdown
    print('about to shut down')
    #import subprocess
    #subprocess.check_call(['sudo', 'poweroff'])
