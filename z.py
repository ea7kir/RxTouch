
def start_longmynd(frequency, rate_list):
    stop_longmynd()
    # assemble the command line arguments
    # params = ["-i", TS_IP, TS_Port, "-S", "0.6", requestKHzStr, allSrs]
    OFFSET = 9750000
    TS_IP = '192.168.1.41'
    TS_PORT = '7777'
    requestKHzStr = str(float(frequency) * 1000 - OFFSET)
    allSrs = rate_list[0]
    for i in range(1, len(rate_list)):
        allSrs += f',{rate_list[i]}'
    params = ['-i ', TS_IP, TS_PORT, '-S', '0.6', requestKHzStr, allSrs]
    # TODO: execute longmynd with args see: https://youtu.be/VlfLqG_qjx0
    #time.sleep(2)
    longmynd_data.status_msg = f'longmynd is running : {params}'
    longmynd_data.longmynd_running = True
    print(longmynd_data.status_msg, flush=True)

start_lonmynd('12345.55', [111,222,333])