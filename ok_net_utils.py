import websockets
import asyncio

SPECTRUM_STREAM = 'wss://eshail.batc.org.uk/wb/fft/fft_ea7kirsatcontroller'

_stream_msg = [0] * 1844

def get_stream_msg():
    global _stream_msg
    #print('_stash_msg has: ', len(_stream_msg))
    return _stream_msg

def _stash_msg(msg):
    global _stream_msg
    for i in range(0,1844):
        _stream_msg[i] = msg[i]
    print('_stash_msg has: ', _stream_msg)




def start_listening():
    pass

##################################

class OscarSpectrumFeed:
    def __init__(self):
        self._data = [0] * 1844
        self._locked = False

    async def _capture_data(self):
        uri = 'wss://eshail.batc.org.uk/wb/fft/fft_ea7kirsatcontroller'
        async with websockets.connect(uri) as websocket:
            while True:
                raw_data = await websocket.recv()
                length = len(raw_data)
                print('recvd {} bytes', length)
                if length == 1844:
                    self._locked = True
                    for i in range(0, 1844):
                        self._data[i] = raw_data[i]
                    self._locked = False

    def open(self):
        asyncio.get_event_loop().run_until_complete(self._capture_data())

    def data(self):
        while self._locked:
            pass
        return self.data

    def close(self):
        pass

