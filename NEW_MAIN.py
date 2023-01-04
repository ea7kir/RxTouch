import websockets
import asyncio

#import threading
#import time
import PySimpleGUI as sg

from dataclasses import dataclass

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

@dataclass
class SpectrumData:
    points = [(0,0)] * 919
    beacon_level = 0.0

SPECTRUM = '-SPECTRUM-'
LONGMYND = '-LONGMYND-'

window:sg.Window = None

#async def task_batc_stream_client():
#    url = 'wss://eshail.batc.org.uk/wb/fft/fft_ea7kirsatcontroller'
#    async with websockets.connect(url) as websocket:
#        #await websocket.send('hey')
#        while True:
#            raw_data = await websocket.recv()
#            length = len(raw_data)
#            print(f'recvd {length} bytes')
#            await asyncio.sleep(0)

async def task_1_read_spectrum_stream_as_points():  
    while window is None:
        await asyncio.sleep(0.2)
    spectrum_data = SpectrumData()
    #await asyncio.sleep(1.0)
    BATC_SPECTRUM_URI = 'wss://eshail.batc.org.uk/wb/fft/fft_ea7kirsatcontroller'
    websocket = await websockets.connect(BATC_SPECTRUM_URI)
    while True:
        recvd_data = await websocket.recv()
        if len(recvd_data) != 1844:
            print('rcvd_data != 1844')
            continue
        for i in range(0, 1836, 2):
            uint_16: int = int(recvd_data[i]) + (int(recvd_data[i+1] << 8))
            # chop off 1/8 noise
            if uint_16 < 8192: uint_16 = 8192 # TODO: where di I get this info from?
            j = (i // 2) + 1
            spectrum_data.points[j] = (j, float(uint_16 - 8192) / 52000.0)
        # calculate average beacon peak level where beacon center is 103
        spectrum_data.beacon_level = 0.0
        for i in range(93, 113): # should be range(73, 133), but this works better
            spectrum_data.beacon_level += spectrum_data.points[i][1]
        spectrum_data.beacon_level /= 20.0
        window.write_event_value(SPECTRUM, spectrum_data)
        #await asyncio.sleep(0.01)

import random # ONLY NEEDED TO SIMULATE DATA DURING DEVELOPMENT
async def task_2_read_longmynd_status_as_dataclass():
    while window is None:
        await asyncio.sleep(0.2)
    status = LmStatus()
    await asyncio.sleep(1.0)
    while True:
        status.null_ratio = random.randint(40, 60) # ONLY NEEDED TO SIMULATE DATA DURING DEVELOPMENT
        window.write_event_value(LONGMYND, status)
        await asyncio.sleep(0.5)

def main():
    global window
    layout = [
        [sg.Text('Spectrum'), sg.Text('DATA GOES HERE', key=SPECTRUM)],
        [sg.Text('Longmynd'), sg.Text('DATA GOES HERE', key=LONGMYND)],
    ]
    window = sg.Window('Window Title', layout, size=(200,100), finalize=True)
    while True:
        event, values = window.read(timeout=1)
        if event == sg.WIN_CLOSED:
            break
        if event == SPECTRUM:
            window[SPECTRUM](values[SPECTRUM].beacon_level)
        if event == LONGMYND:
            window[LONGMYND](values[LONGMYND].null_ratio)
        #await asyncio.sleep(0.01)

if __name__ == '__main__':
    #task_1 = asyncio.create_task(task_1_read_spectrum_stream_as_points())
    #task_2 = asyncio.create_task(task_2_read_longmynd_status_as_dataclass())
    #asyncio.run(main())
    main()
    window.close()
    del window
