#
#  TxRouch
#  Copyright (c) 2023 Michael Naylor EA7KIR (https://michaelnaylor.es)
#

#import pigpio
#from time import sleep

from device_mute import configure_mute, shutdown_mute
from device_mute import switch_mute_On, switch_mute_Off

_pi = None

def configure_devices():
    global _pi
    #_pi = pigpio.pi()
    configure_mute(_pi)

def shutdown_devices():
    shutdown_mute()
    #_pi.stop()

def activate_mute():
    switch_mute_On()

def deactivate_mute():
    switch_mute_Off()