import PySimpleGUI as sg
import asyncio
#from ok_dummy_data import get_dummy_data
from ok_process_spectrum_data import get_recvd_data, SpectrumData, process_spectrum_data

running = True
   
async def get_spectrum_data() -> SpectrumData:
    recvd_data = get_recvd_data()
    processed_data = process_spectrum_data(recvd_data)
    return processed_data

async def main_window():
    global running
    layout = [
        [sg.Quit(button_color=('white', 'red'))],
        [sg.Graph(canvas_size=(700, 200), graph_bottom_left=(0, 0), graph_top_right=(918, 2), background_color='black', float_values=False, key='graph')],      
    ]
    
    window = sg.Window('Qatar-OSCAR 100 Wideband Spectrum Monitor', layout, finalize=True)
    spectrum_graph = window['graph']

    #points = [0,0] * 919

    while running: # the Event Loop
  
        event, values = window.read(timeout=1)
        if event in ('Quit', None):
            running = False

        spectrum_data = await get_spectrum_data()

        points = [(0,0)]

        for i in range(0, 918):
            points.append((i, spectrum_data.spectrum_value[i]))
        points.append((918,0))
        spectrum_graph.erase()
        spectrum_graph.draw_polygon(points, fill_color='green')
        asyncio.sleep(0)

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
