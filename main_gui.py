"""RxTouch"""

import PySimpleGUI as sg
from rx_bandplan import bandplan as bp

from process_spectrum import process_read_spectrum_data, SpectrumData
from process_longmynd import process_read_longmynd_data, LongmyndData
from process_video_ts import process_video_ts

from multiprocessing import Process
from multiprocessing import Pipe

# LAYOUT ----------------------------------------

sg.theme('Black')

MYSCRCOLOR = '#111111'
MYBUTCOLORS = ('#FFFFFF','#222222')
MYDISABLEDBUTCOLORS = ('#444444',None)

def text_data(name, key):
    return sg.Text(name, size=11), sg.Text(' ', size=9, key=key, text_color='orange')

def incdec_but(name, key):
    return sg.Button(name, key=key, size=4, border_width=0, button_color=MYBUTCOLORS, mouseover_colors=MYBUTCOLORS)

def button_selector(key_down, value, key_up, width):
    return  incdec_but('<', key_down), sg.Text(' ', size=width, justification='center', key=value, text_color='orange'), incdec_but('>', key_up) 

top_layout = [
    sg.Button('RxTouch', key='-SYSTEM-', border_width=0, button_color=MYBUTCOLORS, mouseover_colors=MYBUTCOLORS),
    sg.Text(' ', expand_x=True, key='-STATUS_BAR-', text_color='orange'),
    sg.Button('Shutdown', key='-SHUTDOWN-', border_width=0, button_color=MYBUTCOLORS, mouseover_colors=MYBUTCOLORS),    
]

spectrum_layout = [
    sg.Graph(canvas_size=(770, 250), graph_bottom_left=(0, 0x2000), graph_top_right=(918, 0xFFFF), background_color='black', float_values=False, key='graph'),
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
        [sg.Button(' TUNE ', key='-TUNE-', border_width=0, button_color=MYBUTCOLORS, mouseover_colors=MYBUTCOLORS, disabled_button_color=MYDISABLEDBUTCOLORS, disabled=False)],
        [sg.Text(' ')],
        [sg.Button(' Mute ', key='-MUTE-', border_width=0, button_color=MYBUTCOLORS, mouseover_colors=MYBUTCOLORS, disabled_button_color=MYDISABLEDBUTCOLORS, disabled=False)],
    ]),
]

layout = [
    top_layout,
    spectrum_layout,
    tune_layout,
    status_layout,
]

# CALLBACK DISPATCH -----------------------------

def tune():
    # callout to longmynd
    frequency, rate_list = bp.fequency_and_rate_list()
    # TODO: send a start message to process_read_longmynd_data
    # to call process_read_longmynd_data.start(frequency, rate_list)

dispatch_dictionary = {
    # Lookup dictionary that maps button to function to call
    '-BD-':bp.dec_band, '-BU-':bp.inc_band, 
    '-FD-':bp.dec_frequency, '-FU-':bp.inc_frequency, 
    '-SD-':bp.dec_symbol_rate, '-SU-':bp.inc_symbol_rate,
    '-TUNE-':tune,
}

# UPDATE FUNCTIONS ------------------------------

def update_control(window, bp):
    window['-BV-'].update(bp.band)
    window['-FV-'].update(bp.frequency)
    window['-SV-'].update(bp.symbol_rate)

def update_longmynd_status(window, longmynd_data):
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
    window['-STATUS_BAR-'].update(longmynd_data.status_msg)

def update_graph(graph, spectrum_data):
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
    x = bp.selected_frequency_marker()
    graph.draw_line((x, 0x2000), (x, 0xFFFF), color='#880000')
    # draw beacon level
    graph.draw_line((0, spectrum_data.beacon_level), (918, spectrum_data.beacon_level), color='#880000', width=1)
    # draw spectrum
    graph.draw_polygon(spectrum_data.points, fill_color='green')

# MAIN ------------------------------------------

def main_gui(recv_spectrum_data, recv_longmynd_data):
    window = sg.Window('', layout, size=(800, 480), font=(None, 11), background_color=MYSCRCOLOR, use_default_focus=False, finalize=True)
    window.set_cursor('none')
    graph = window['graph']
    while True:
        event, values = window.read(timeout=1)
        if event == '-SHUTDOWN-':
            #if sg.popup_yes_no('Shutdown Now?', background_color='red', keep_on_top=True) == 'Yes':
            break
        if event in dispatch_dictionary:
            func_to_call = dispatch_dictionary[event]
            func_to_call()
        if bp.changed:
            update_control(window, bp)
            bp.changed = False
        while recv_spectrum_data.poll():
            spectrum_data = recv_spectrum_data.recv()
            update_graph(graph, spectrum_data)
        while recv_longmynd_data.poll():
            longmynd_data = recv_longmynd_data.recv()
            update_longmynd_status(window, longmynd_data)
    window.close()
    del window

if __name__ == '__main__':
    recv_spectrum_data, send_spectrum_data = Pipe()
    recv_longmynd_data, send_longmynd_data = Pipe()
    recv_video_ts, send_video_ts = Pipe()
    # create the process
    p_read_spectrum_data = Process(target=process_read_spectrum_data, args=(send_spectrum_data,))
    p_read_longmynd_data = Process(target=process_read_longmynd_data, args=(send_longmynd_data,))
    p_process_video_ts = Process(target=process_video_ts, args=(recv_video_ts, send_video_ts))
    # start the process
    p_read_spectrum_data.start()
    p_read_longmynd_data.start()
    p_process_video_ts.start()
    # main ui
    main_gui(recv_spectrum_data, recv_longmynd_data)
    # kill 
    p_read_spectrum_data.kill()
    p_read_longmynd_data.kill()
    p_process_video_ts.kill()
    # shutdown
    print('about to shut down')
    #import subprocess
    #subprocess.check_call(['sudo', 'poweroff'])
