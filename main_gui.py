"""RxTouch"""

from multiprocessing import Process
from multiprocessing import Pipe

import PySimpleGUI as sg
import button_logic

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
    ]),
    sg.Column([
        text_data('FEC', '-FEC-'),
        text_data('Codecs', '-CODECS-'),
        text_data('dB MER', '-DB_MER-'),
        text_data('dB Margin', '-DB_MARGIN-'),
    ]),
    sg.Column([
        text_data('dBm Power', '-DBM_POWER-'),
        text_data('Null Ratio', '-NULL_RATIO-'),
        [sg.ProgressBar(100, orientation='h', size=(10, 10), key='-NULL_RATIO-BAR-', bar_color=('#00FF00','#111111'))],
        text_data('Provider', '-PROVIDER-'),
        text_data('Service', '-SERVICE-'),
    ]),
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
    '-BD-':button_logic.dec_band, '-BU-':button_logic.inc_band, 
    '-FD-':button_logic.dec_frequency, '-FU-':button_logic.inc_frequency, 
    '-SD-':button_logic.dec_symbol_rate, '-SU-':button_logic.inc_symbol_rate,
    '-DISPLAY_INITIAL_VALUES-':display_initial_values,
}

# MAIN ------------------------------------------

def main_gui(recv_spectrum_data, longmynd1):
    window = sg.Window('', layout, size=(800, 480), font=(None, 11), background_color=SCREEN_COLOR, use_default_focus=False, finalize=True)
    window.set_cursor('none')
    graph = window['graph']
    tune_active = False
    mute_active = False
    # fix to display initial controll values
    window.write_event_value('-DISPLAY_INITIAL_VALUES-', None)
    while True:
        event, values = window.read(timeout=100)
        if event == '-SHUTDOWN-':
            #if sg.popup_yes_no('Shutdown Now?', background_color='red', keep_on_top=True) == 'Yes':
            longmynd1.send('STOP')
            break
        if event == '-TUNE-':
            tune_active = not tune_active
            if tune_active:
                window['-TUNE-'].update(button_color=TUNE_ACTIVE_BUTTON_COLOR)
                tune_args = button_logic.tune_args()
                print(f'tune_args has : {tune_args.frequency}, {tune_args.symbol_rate}')
                # TODO: send tune_args to process_read_longmynd_data.start(tune_args)
                longmynd1.send(tune_args)
                #window['-STATUS_BAR-'].update(f'start: {tune_args.frequency},{tune_args.symbol_rate}')
                window['-STATUS_BAR-'].update(longmynd.status_msg)
            else:
                longmynd1.send('STOP')
                window['-TUNE-'].update(button_color=NORMAL_BUTTON_COLOR)
                #window['-STATUS_BAR-'].update('stop (or invalid display)')
                window['-STATUS_BAR-'].update(longmynd.status_msg)
        if event == '-MUTE-':
            mute_active = not mute_active
            if mute_active:
                window['-MUTE-'].update(button_color=MUTE_ACTIVE_BUTTON_COLOR)
            else:
                window['-MUTE-'].update(button_color=NORMAL_BUTTON_COLOR)
        if event in dispatch_dictionary:
            func_to_call = dispatch_dictionary[event]
            func_to_call()
            window['-BV-'].update(button_logic.curr_value.band)
            window['-FV-'].update(button_logic.curr_value.frequency)
            window['-SV-'].update(button_logic.curr_value.symbol_rate)
        if recv_spectrum_data.poll():
            spectrum_data = recv_spectrum_data.recv()
            while recv_spectrum_data.poll():
                _ = recv_spectrum_data.recv()
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
            x = button_logic.selected_frequency_marker()
            graph.draw_line((x, 0x2000), (x, 0xFFFF), color='#880000')
            # draw beacon level
            graph.draw_line((0, spectrum_data.beacon_level), (918, spectrum_data.beacon_level), color='#880000', width=1)
            # draw spectrum
            graph.draw_polygon(spectrum_data.points, fill_color='green')
        if longmynd1.poll():
            longmynd_data = longmynd1.recv()
            while longmynd1.poll():
                _ = longmynd1.recv()
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
            window['-NULL_RATIO-BAR-'].UpdateBar(longmynd_data.null_ratio)
            window['-PROVIDER-'].update(longmynd_data.provider)
            window['-SERVICE-'].update(longmynd_data.service)
    window.close()
    del window

if __name__ == '__main__':
    recv_spectrum_data, send_spectrum_data = Pipe()
    longmynd1, longmynd2 = Pipe(duplex=True)
    recv_video_ts, send_video_ts = Pipe()
    # create the process
    p_read_spectrum_data = Process(target=process_read_spectrum_data, args=(send_spectrum_data,))
    p_read_longmynd_data = Process(target=process_read_longmynd_data, args=(longmynd2,))
    p_process_video_ts = Process(target=process_video_ts, args=(recv_video_ts, send_video_ts))
    # start the process
    p_read_spectrum_data.start()
    p_read_longmynd_data.start()
    p_process_video_ts.start()
    # main ui
    main_gui(recv_spectrum_data, longmynd1)
    # kill 
    p_read_spectrum_data.kill()
    p_read_longmynd_data.kill()
    p_process_video_ts.kill()
    # shutdown
    print('about to shut down')
    #import subprocess
    #subprocess.check_call(['sudo', 'poweroff'])
