import PySimpleGUI as sg
import asyncio
import websockets

layout = [
    [sg.Quit(button_color=('white', 'red'))],
    [sg.Graph(canvas_size=(700, 200), graph_bottom_left=(0, 0), graph_top_right=(918, 1.0), background_color='black', float_values=True, key='graph')],      
]

window = sg.Window('Qatar-OSCAR 100 Wideband Spectrum Monitor', layout, finalize=True)
spectrum_graph = window['graph']
running = True

from dataclasses import dataclass
@dataclass
class SpectrumData:
    beacon_value = 0.0
    spectrum_value = [0.0] * 918

async def process_spectrum_data(recvd_data: bytearray) -> SpectrumData:
    spectrum_data = SpectrumData()
    if len(recvd_data) != 1844:
        print('rcvd_data != 1844')
        return spectrum_data
    for i in range(0, 1836, 2):
        uint_16: int = int(recvd_data[i]) + (int(recvd_data[i+1] << 8))
        # chop off 1/8 noise
        if uint_16 < 8192: uint_16 = 8192
        spectrum_data.spectrum_value[i // 2] = float(uint_16 - 8192) / 52000.0
    # find the average beacon value where beacon center is 103
    spectrum_data.beacon_value = 0.0
    #for i in range(73, 133):
    for i in range(93, 113):
        spectrum_data.beacon_value += spectrum_data.spectrum_value[i]
    spectrum_data.beacon_value /= 20.0
    # invert y axis
    #spectrum_data.beacon_value = 1.0 - spectrum_data.beacon_value / 61.0
    #print(spectrum_data.spectrum_value)
    return spectrum_data

async def get_spectrum_data(websocket) -> SpectrumData:
    recvd_data = await websocket.recv()
    processed_data = await process_spectrum_data(recvd_data)
    return processed_data

async def main_window():
    BATC_SPECTRUM_URI = 'wss://eshail.batc.org.uk/wb/fft/fft_ea7kirsatcontroller'
    websocket = await websockets.connect(BATC_SPECTRUM_URI)
    #points = [(0,0)] * 919
    global running
    while running:
        event, values = window.read(timeout=1)
        if event in ('Quit', None):
            running = False
        spectrum_graph.erase()
        # graticule
        for i in range(1, 19):
            y = (1.0 / 18.0) * i
            if i in {1,6,11,16}:
                color = '#444444'
            else:
                color = '#222222'
            spectrum_graph.draw_line((0, y), (918, y), color=color)
        # data
        spectrum_data = await get_spectrum_data(websocket)
        points = [(0,0)]
        for i in range(0, 918):
            points.append((i, spectrum_data.spectrum_value[i]))
        points.append((918,0))
        # beacon level
        #spectrum_graph.draw_line((0, spectrum_data.beacon_value), (918, spectrum_data.beacon_value), color='red', width=1)
        spectrum_graph.draw_polygon(points, fill_color='green')
        await asyncio.sleep(0)
    await websocket.close()

async def main():
    await asyncio.gather(
        main_window(),
    )
    print('all tasks have closed')
    window.close()
    if window.was_closed():
        print('main window has closed')

if __name__ == '__main__':
    asyncio.run(main())
    print('about to shut down')
    #import subprocess
    #subprocess.check_call(['sudo', 'poweroff'])
