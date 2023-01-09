

# EXAMPLE CODE

import subprocess

# See: https://www.youtube.com/watch?v=2Fp1N6dof0Y


def start_longmynd(frequency, rate_list):
    stop_longmynd()
    # assemble the command line arguments
    # params = ["-i", TS_IP, TS_Port, "-S", "0.6", requestKHzStr, allSrs]
    OFFSET = 9750000
    TS_IP = '192.168.1.36'
    TS_PORT = '7777'
    requestKHzStr = str(float(frequency) * 1000 - OFFSET)
    allSrs = rate_list[0]
    for i in range(1, len(rate_list)):
        allSrs += f',{rate_list[i]}'
    params = ['-i ', TS_IP, TS_PORT, '-S', '0.6', requestKHzStr, allSrs]
    # TODO: execute longmynd with args see: https://youtu.be/VlfLqG_qjx0
    #time.sleep(2)
    longmynd_data.longmynd_running = True

def stop_longmynd():
    if not longmynd_data.longmynd_running:
        return
    #self.status_msg = 'stopping longmynd'
    longmynd_data.longmynd_running = False
    #time.sleep(2)



p = subprocess.run(cmd, shell=True, capture_outpput=True)

print(p.stdout)

print(p.returncode)