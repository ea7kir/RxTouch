import PySimpleGUI as sg
import time
import threading
from ok_net_utils import start_listening, get_stream_msg
from ok_process_spectrum_data import SpectrumData, process_spectrum_data
from ok_dummy_data import get_dummy_data

def get_spectrum_data():
    recvd_data = get_stream_msg()
    #recvd_data = get_dummy_data()
    #print('ok_display_spectrum_data.py recvd_data got: ', len(recvd_data))
    return process_spectrum_data(recvd_data)

def main():

    layout = [
        [sg.Quit(button_color=('white', 'red'))],
        [sg.Graph(canvas_size=(700, 200), graph_bottom_left=(0, 0), graph_top_right=(918, 2), background_color='black', float_values=False, key='graph')],      
    ]
    
    window = sg.Window('Qatar-OSCAR 100 Wideband Spectrum Monitor', layout, finalize=True)
    spectrum_graph = window['graph']

    #points = [0,0] * 919

    
    window.perform_long_operation(start_listening, '-OPERATION DONE-')
    #start_listening()
    print('########## HERE ###########')
    while True: # the Event Loop
  
        event, values = window.read(timeout=100)
        if event in ('Quit', None):
            break

        spectrum_data = get_spectrum_data()
        #print(spectrum_data.spectrum_value)

        points = [(0,0)]

        for i in range(0, 918):
            points.append((i, spectrum_data.spectrum_value[i]))
        points.append((918,0))

        #print(points[0], points[1], points[2], points[3], points[4])

        spectrum_graph.erase()
        #triangle = [(0.0,0.0),(459.7,6300.5),(918-9,0.0)]
        spectrum_graph.draw_polygon(points, fill_color='green')
        
    
    window.close()

if __name__ == '__main__':
    main()