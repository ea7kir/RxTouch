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
    win = window  
    points = [(0,0)] * 918
    i = 0
    while True:
        i += 1
        points[0] = (i,i)
        print('task_1')
        win.write_event_value(SPECTRUM, points)
        await asyncio.sleep(0.5)

async def task_2_read_longmynd_status_as_dataclass(window):
    win = window
    status = LmStatus()
    while True:
        status.null_ratio += 1
        print('task_2')
        win.write_event_value(LONGMYND, status)
        await asyncio.sleep(0.5)

async def main():
    layout = [
        [sg.Text('Spectrum'), sg.Text('DATA GOES HERE', key='-spectrum_data-')],
        [sg.Text('Longmynd'), sg.Text('DATA GOES HERE', key='-longmynd_data-')],
    ]
    window = sg.Window('Window Title', layout, size=(200,100), finalize=True)
    await asyncio.sleep(0.5)
    task_1 = asyncio.create_task(task_1_read_spectrum_stream_as_points(window))
    await asyncio.sleep(0.5)
    task_2 = asyncio.create_task(task_2_read_longmynd_status_as_dataclass(window))
    await asyncio.sleep(0.5)
    while True:
        event, values = window.read(timeout=1) # is this incompatable with asyncio?
        if event == sg.WIN_CLOSED:
            task_1.cancel()
            task_2.cancel()
            break
        if event == SPECTRUM:
            window['-spectrum_data-'](values[SPECTRUM][0])
        if event == LONGMYND:
            window['-longmynd_data-'](values[LONGMYND].null_ratio)
    window.close()
    del window


if __name__ == '__main__':
    asyncio.run(main())
