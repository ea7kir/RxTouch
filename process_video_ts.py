from time import sleep # ONLY NEEDED TO SIMULATE FETCH TIMES DURING DEVELOPMENT

# not known if thess pipes will be needed
def process_video_ts(recv_video_ts, send_video_ts):
    LM_TS_PIPE = '/home/pi/RxTouch/longmynd/longmynd_main_ts'
    while True:
        # ...
        sleep(0.020)# ONLY NEEDED TO SIMULATE FETCH TIMES DURING DEVELOPMENT
