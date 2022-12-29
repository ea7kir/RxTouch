import websockets
import asyncio

BATC_SPECTRUM_URI = 'wss://eshail.batc.org.uk/wb/fft/fft_ea7kirsatcontroller'

async def task_batc_stream_client(uri):
    async with websockets.connect(uri) as websocket:
        #await websocket.send('hey')
        while True:
            raw_data = await websocket.recv()
            length = len(raw_data)
            print(f'recvd {length} bytes')
            await asyncio.sleep(0)

async def task_another():
    # report a message
    print('executing another task')
    # suspend for a moment
    await asyncio.sleep(1)

async def main():
    # report a message
    print('main coroutine')
    # create and schedule the task
    task = asyncio.create_task(task_batc_stream_client(BATC_SPECTRUM_URI))
    # wait a moment
    await asyncio.sleep(10)
    # cancel the task
    was_cancelled = task.cancel()
    print(f'>was canceled: {was_cancelled}')
    # wait a moment
    await asyncio.sleep(0.1)
    # report the status
    print(f'>canceled: {task.cancelled()}')


if __name__ == '__main__':
    asyncio.run(main())

 