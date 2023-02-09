# constants

LM_START_SCRIPT                 = '/home/pi/RxTouch/lm_start'
LM_STOP_SCRIPT                  = '/home/pi/RxTouch/lm_stop'

LM_STATUS_FIFO_NAME             = '/home/pi/RxTouch/longmynd/longmynd_main_status'
LM_TS_PIPE                      = '/home/pi/RxTouch/longmynd/longmynd_main_ts'

LM_OFFSET                       = 9750000

import socket # only used to find ip of apple tv
TS_IP                           = socket.gethostbyname('office.local') # Apple TV
TS_PORT                         = '7777'

SPECTRUM_URL                    = 'wss://eshail.batc.org.uk/wb/fft/fft_ea7kirsatcontroller'
