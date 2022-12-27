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

# Each scan sends a block of 1844 bytes
# This is 922 16-bit samples in low-high format
# The last two 16-bit samples are zero
# Sample zero is at 10490.500MHz
# Each sample represents 10000 / 1024 = 9.765625kHz
# Sample 919 is at 10499.475MHz
# The noise floor value is around 10000
# The peak of the beacon is around 40000

async def get_spectrum_data(websocket) -> (bool, float, list):
    recvd_data = await websocket.recv()
    beacon_level = 0.0
    points = [(0,0)] * 919 # ensure the last point is (0,0)
    if len(recvd_data) != 1844:
        print('rcvd_data != 1844')
        return False, 0, []
    for i in range(0, 1836, 2):
        uint_16: int = int(recvd_data[i]) + (int(recvd_data[i+1] << 8))
        # chop off 1/8 noise
        if uint_16 < 8192: uint_16 = 8192 # TODO: where di I get this info from?
        j = (i // 2) + 1
        points[j] = (j, float(uint_16 - 8192) / 52000.0)
    # calculate average beacon peak level where beacon center is 103
    beacon_level = 0.0
    for i in range(93, 113): # should be range(73, 133), but this works better
        beacon_level += points[i][1]
    beacon_level /= 20.0
    return True, beacon_level, points

async def main_window():
    BATC_SPECTRUM_URI = 'wss://eshail.batc.org.uk/wb/fft/fft_ea7kirsatcontroller'
    websocket = await websockets.connect(BATC_SPECTRUM_URI)
    global running
    while running:
        event, values = window.read(timeout=1)
        if event in ('Quit', None):
            running = False
        spectrum_graph.erase()
        # draw graticule
        for i in range(1, 19):
            y = (1.0 / 18.0) * i
            if i in {1,6,11,16}:
                color = '#444444'
            else:
                color = '#222222'
            spectrum_graph.draw_line((0, y), (918, y), color=color)
        # get new data
        valid, beacon_level, points = await get_spectrum_data(websocket)
        if valid:
            # draw beacon level
            spectrum_graph.draw_line((0, beacon_level), (918, beacon_level), color='red', width=1)
            # draw spectrum
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
