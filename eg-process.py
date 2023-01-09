
import PySimpleGUI as sg

from time import sleep
from multiprocessing import Process
from multiprocessing import Pipe

from dataclasses import dataclass

@dataclass
class SpectrumData:
    points = [(int(0),int(0))] * 920 # to ensure the last point is (0,0)
    beacon_level:int = 0
    changed:bool = False

@dataclass
class LmStatus:
    frequency = '10491.551'
    symbol_rate = '1500'
    mode = '' #MODE[0]
    constellation = 'QPSK'
    fec = '4/5'
    codecs = 'H264 MP3'
    db_mer = '8.9'
    db_margin = '4.1'
    dbm_power = '-60'
    null_ratio = 0
    provider = 'A71A'
    service = 'QARS'

SPECTRUM = '-SPECTRUM-'
LONGMYND = '-LONGMYND-'

def ui(connection1, connection2):
    layout = [
        [sg.Text('Spectrum'), sg.Text('DATA GOES HERE', key=SPECTRUM)],
        [sg.Text('Longmynd'), sg.Text('DATA GOES HERE', key=LONGMYND)],
    ]
    window = sg.Window('Window Title', layout, size=(200,100), finalize=True)
    while True:
        event, values = window.read(timeout=1)
        if event == sg.WIN_CLOSED:
            break
        spectrum_item = connection1.recv()
        window[SPECTRUM].update(spectrum_item.beacon_level)
        lm_item = connection2.recv()
        window[LONGMYND].update(lm_item.null_ratio)
#        if event == SPECTRUM:
#            window[SPECTRUM](values[SPECTRUM].beacon_level)
#        if event == LONGMYND:
#            window[LONGMYND](values[LONGMYND].null_ratio)
        #await asyncio.sleep(0.01)
    window.close()
    del window

def  my_process_1(connection):
    spectrum_item = SpectrumData()
    while True:
        sleep(0.001)
        #print(f'This is my_process_1: {spectrum_item.beacon_level}', flush=True)
        connection.send(spectrum_item)
        spectrum_item.beacon_level += 1

def  my_process_2(connection):
    lm_item = LmStatus()
    while True:
        sleep(0.001)
        #print('This is my_process_2', flush=True)
        connection.send(lm_item)
        lm_item.null_ratio += 1

def  my_process_3():
    x = 0
    while True:
        x += 1
        sleep(0.001)
        #print('This is my_process_3', flush=True)

def  my_process_4():
    x = 0
    while True:
        x += 1
        sleep(0.001)
        #print('This is my_process_4', flush=True)

def  my_process_5():
    x = 0
    while True:
        x += 1
        sleep(0.001)
        #print('This is my_process_3', flush=True)

def  my_process_6():
    x = 0
    while True:
        x += 1
        sleep(0.001)
        #print('This is my_process_4', flush=True)

# protect the entry point
if __name__ == '__main__':
    conn1a, conn1b = Pipe()
    conn2a, conn2b = Pipe()
    # create the process
    process1 = Process(target=my_process_1, args=(conn1b,))
    process2 = Process(target=my_process_2, args=(conn2b,))
    process3 = Process(target=my_process_3)
    #process4 = Process(target=my_process_4)
    #process5 = Process(target=my_process_5)
    #process6 = Process(target=my_process_6)
    # start the process
    process1.start()
    process2.start()
    process3.start()
    #process4.start()
    #process5.start()
    #process6.start()
    # wait for the process to finish
    print('Waiting for the process to finish')
    ui(conn1a, conn2a)
    process1.kill()
    process2.kill()
    process3.kill()
    #process4.kill()
    #process5.kill()
    #process6.kill()
