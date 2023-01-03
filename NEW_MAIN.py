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

SPECTRUM = '-SPECTRUM-'
LONGMYND = '-LONGMYND-'

#async def task_batc_stream_client():
#    url = 'wss://eshail.batc.org.uk/wb/fft/fft_ea7kirsatcontroller'
#    async with websockets.connect(url) as websocket:
#        #await websocket.send('hey')
#        while True:
#            raw_data = await websocket.recv()
#            length = len(raw_data)
#            print(f'recvd {length} bytes')
#            await asyncio.sleep(0)

async def task_1_read_spectrum_stream_as_points(window):  
    points = [(0,0)] * 918
    await asyncio.sleep(1.0)
    i = 0
    while True:
        i += 1
        points[0] = (i,i)
        window.write_event_value(SPECTRUM, points)
        await asyncio.sleep(0.3)

async def task_2_read_longmynd_status_as_dataclass(window):
    status = LmStatus()
    await asyncio.sleep(1.0)
    while True:
        status.null_ratio += 1
        window.write_event_value(LONGMYND, status)
        await asyncio.sleep(0.5)

async def main():
    layout = [
        [sg.Text('Spectrum'), sg.Text('DATA GOES HERE', key=SPECTRUM)],
        [sg.Text('Longmynd'), sg.Text('DATA GOES HERE', key=LONGMYND)],
    ]
    window = sg.Window('Window Title', layout, size=(200,100), finalize=True)
    task_1 = asyncio.create_task(task_1_read_spectrum_stream_as_points(window))
    task_2 = asyncio.create_task(task_2_read_longmynd_status_as_dataclass(window))
    while True:
        event, values = window.read(timeout=1)
        if event == sg.WIN_CLOSED:
            break
        if event == SPECTRUM:
            window[SPECTRUM](values[SPECTRUM][0])
        if event == LONGMYND:
            window[LONGMYND](values[LONGMYND].null_ratio)
        await asyncio.sleep(0)
    task_1.cancel()
    task_2.cancel()
    await asyncio.sleep(1.0)
    window.close()
    del window

if __name__ == '__main__':
    asyncio.run(main())
