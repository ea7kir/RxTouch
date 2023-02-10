#import pigpio
#from device_constants import RELAY_ON, RELAY_OFF
#from device_constants import RELAY_MUTE_GPIO

_pi = None

def _switch_mute(gpio, state):
    pass
    #_pi.write(gpio, state)

def _config_mute(gpio):
    pass
    #_pi.set_mode(gpio, pigpio.OUTPUT)
    #_pi.write(gpio, RELAY_OFF)

def configure_mute(pi):
    pass
    global _pi
    _pi = pi
    #_config_relay(RELAY_MUTE_GPIO)

def shutdown_mute():
    pass
    #_switch_relay(RELAY_MUTE_GPIO, RELAY_OFF)

def switch_mute_On():
    print("SWITCHING ON MUTE")
    pass
    #_switch_relay(RELAY_MUTE_GPIO, RELAY_ON)

def switch_mute_Off():
    print("SWITCHING OFF MUTE")
    pass
    #_switch_relay(RELAY_MUTE_GPIO, RELAY_OFF)
