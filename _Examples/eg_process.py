
import PySimpleGUI as sg

from time import sleep
from multiprocessing import Process
from multiprocessing import Pipe

class SpectrumData:
    def __init__(self):
        self.points = [(int(0),int(0))] * 920 # to ensure the last point is (0,0)
        self.beacon_level:int = 0
        #self.changed:bool = False

class LongmyndData:
    def __init__(self):
        self.frequency = '10491.551'
        self.symbol_rate = '1500'
        self.mode = '' #MODE[0]
        self.constellation = 'QPSK'
        self.fec = '4/5'
        self.codecs = 'H264 MP3'
        self.db_mer = '8.9'
        self.db_margin = '4.1'
        self.dbm_power = '-60'
        self.null_ratio = 0
        self.provider = 'A71A'
        self.service = 'QARS'

BEACON = '-BEACON-'
POINTS = '-POINTS-'
LONGMYND = '-LONGMYND-'

def main_gui(recv_spectrum_data, recv_longmynd_data):
    layout = [
        [sg.Text('Spectrum beacon'), sg.Text('DATA GOES HERE', key=BEACON)],
        [sg.Text('Spectrum points'), sg.Text('DATA GOES HERE', key=POINTS)],
        [sg.Text('Longmynd'), sg.Text('DATA GOES HERE', key=LONGMYND)],
    ]
    window = sg.Window('Window Title', layout, size=(200,100), finalize=True)
    while True:
        event, values = window.read(timeout=1)
        if event == sg.WIN_CLOSED:
            # TODO: HOW TO SEND COMMANDS OR STOP A PROCESS ?
            break
        while recv_spectrum_data.poll():
            spectrum_data = recv_spectrum_data.recv()
            window[BEACON].update(spectrum_data.beacon_level)
            window[POINTS].update(spectrum_data.points[100])
        while recv_longmynd_data.poll():
            longmynd_data = recv_longmynd_data.recv()
            window[LONGMYND].update(longmynd_data.null_ratio)
    window.close()
    del window

def process_read_spectrum_data(send_spectrum_data):
    spectrum_data = SpectrumData()
    j = 0
    k = 0
    while True:
        sleep(0.333)
        #print(f'This is process_read_spectrum_data: {spectrum_data.beacon_level}', flush=True)
        send_spectrum_data.send(spectrum_data)
        spectrum_data.beacon_level += 1
        j += 1; k += 2
        spectrum_data.points[100] = (j,k)

def process_read_longmynd_data(send_longmymd_data):
    longmynd_data = LongmyndData()
    while True:
        sleep(0.1)
        #print(f'This is process_read_longmynd_data: {longmynd_data.null_ratio}', flush=True)
        send_longmymd_data.send(longmynd_data)
        longmynd_data.null_ratio += 1

def my_process_3():
    x = 0
    while True:
        x += 1
        sleep(0.001)
        #print('This is my_process_3', flush=True)

def my_process_4():
    x = 0
    while True:
        x += 1
        sleep(0.001)
        #print('This is my_process_4', flush=True)

def my_process_5():
    x = 0
    while True:
        x += 1
        sleep(0.001)
        #print('This is my_process_3', flush=True)

def my_process_6():
    x = 0
    while True:
        x += 1
        sleep(0.001)
        #print('This is my_process_4', flush=True)

# protect the entry point
if __name__ == '__main__':
    recv_spectrum_data, send_spectrum_data = Pipe()
    recv_longmynd_data, send_longmynd_data = Pipe()
    # create the process
    p_read_spectrum_data = Process(target=process_read_spectrum_data, args=(send_spectrum_data,))
    p_read_longmynd_data = Process(target=process_read_longmynd_data, args=(send_longmynd_data,))
    #process3 = Process(target=my_process_3)
    #process4 = Process(target=my_process_4)
    #process5 = Process(target=my_process_5)
    #process6 = Process(target=my_process_6)
    # start the process
    p_read_spectrum_data.start()
    p_read_longmynd_data.start()
    #process3.start()
    #process4.start()
    #process5.start()
    #process6.start()

    main_gui(recv_spectrum_data, recv_longmynd_data)
    
    p_read_spectrum_data.kill()
    p_read_longmynd_data.kill()
    #process3.kill()
    #process4.kill()
    #process5.kill()
    #process6.kill()
