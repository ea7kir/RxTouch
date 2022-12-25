import PySimpleGUI as sg
import asyncio
from random import randint
import sys

sg.change_look_and_feel('DarkAmber')

layout = [
    [sg.Text('')],
    [sg.Text('Enter text:'), sg.InputText(key='-Text-')],
    [sg.Text('', key='-Status-', size=(20, 1))],
    [sg.Button('Submit', key='-Submit-'), sg.Button('Çancel', key='-Cancel-')],
]

window = sg.Window('Dripbox', layout, finalize=True)

running = True

async def background():
    global running
    while running:
        rando = randint(2, 2000)
        print(rando)
        window['-Status-'].update(rando)
        await asyncio.sleep(1)

async def ui():
    global running
    while running:
        event, value = window.read(timeout=1)
        if event == sg.WIN_CLOSED or event == '-Cancel-':
            running = False
        if event != '__TIMEOUT__':
            print(f"{event} - {value}")
        await asyncio.sleep(0)

async def main():
    await asyncio.gather(
        ui(),
        background(),
    )
    print('All tasks stoped')
    window.close()
    print('window closed')

if __name__ == '__main__':
    asyncio.run(main())
    print('end')
    
