import PySimpleGUI as sg
import asyncio
import random
import sys

sg.change_look_and_feel('DarkAmber')

layout = [
    [sg.Text('')],
    [sg.Text('Password:'), sg.InputText(password_char='*', key='password')],
    [sg.Text('', key='status', size=(20, 1))],
    [sg.Button('Submit'), sg.Button('Çancel')],
]

window = sg.Window('Dripbox', layout, finalize=True)

async def background():
    while True:
        rando = random.randint(2, 2000)
        print(rando)
        window['status'].update(rando)
        await asyncio.sleep(1)

async def ui():
    while True:
        event, value = window.read(timeout=1)
        if event in (None, 'Çancel'):
            sys.exit()
        if event != '__TIMEOUT__':
            print(f"{event} - {value}")
        await asyncio.sleep(0)

#async def wait_list():
#    await asyncio.wait([ui(), background()]) # I changed the order, but make no dif

async def main():
    await asyncio.gather(
        ui(),
        background(),
    )

if __name__ == '__main__':
#    loop = asyncio.get_event_loop()
#    loop.run_until_complete(wait_list())
#    loop.close()
    asyncio.run(main())
    
