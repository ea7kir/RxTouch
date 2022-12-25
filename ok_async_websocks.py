import websockets
import asyncio

SPECTRUM_URI = 'wss://eshail.batc.org.uk/wb/fft/fft_ea7kirsatcontroller'

async def wsrun(uri):
    async with websockets.connect(uri) as websocket:
        await websocket.send('hey')
        while True:
            print(await websocket.recv())


asyncio.get_event_loop().run_until_complete(wsrun(SPECTRUM_URI))

 