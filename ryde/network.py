#    Ryde Player provides a on screen interface and video player for Longmynd compatible tuners.
#    Copyright © 2020 Tim Clark
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <https://www.gnu.org/licenses/>.

import socket, json
import ryde.sources.common
import ryde.common

class networkConfig(object):
    def __init__(self):
        self.enabled = False
        self.bindaddr = 'localhost'
        self.port = 8765

    # parse a dict containing the network config
    def loadConfig(self, config):
        perfectConfig = True
        if isinstance(config, dict):
            if 'bindaddr' in config:
                if isinstance(config['bindaddr'], str):
                    self.bindaddr = config['bindaddr']
                else:
                    print("Invalid bind ip address, skipping")
                    perfectConfig = False
            else:
                print("No bind ip address, skipping")
                perfectConfig = False
            if 'port' in config:
                if isinstance(config['port'], int):
                    if config['port'] <= 65535 and config['port']>0: # max TCP port, (2^16)-1
                        self.port = config['port']
                    else:
                        print("Invalid port number, out of range, skipping")
                        perfectConfig = False
                else:
                    print("Invalid port number, not an int, skipping")
                    perfectConfig = False
        else:
            print("Network config invalid, ignoring")
        if perfectConfig:
            self.enabled = True
        return perfectConfig


class networkManager(object):
    def __init__(self, config, eventCallback, muteCallback, debugFunctions):
        self.config = config
        self.eventCallback = eventCallback
        self.muteCallback = muteCallback
        self.debugFunctions = debugFunctions
        self.activeConnections = dict()
        if self.config.network.enabled:
            self.mainSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.mainSock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.mainSock.setblocking(0)
            self.mainSock.bind((self.config.network.bindaddr, self.config.network.port))
            self.mainSock.listen(5)
            self.commands = { # dict of commands and handler functions
                    "getBands":  self.getBands,
                    "setTune":   self.setTune,
                    "setMute":   self.setMute,
                    "sendEvent": self.sendEvent,
                    "debugFire": self.debugFire,
                    }
            self.eventMap = dict()
            for thisEvent in rydeplayer.common.navEvent:
                self.eventMap[thisEvent.rawName] = thisEvent

    def __del__(self):
        for sock in list(self.activeConnections.keys()):
            sock.shutdown(socket.SHUT_RDWR)
            sock.close()
        self.mainSock.shutdown(socket.SHUT_RDWR)
        self.mainSock.close()

    def getFDs(self):
        if self.config.network.enabled:
            return [self.mainSock] + list(self.activeConnections.keys())
        else:
            return []

    def handleFD(self, fd):
        stop = False
        if fd is self.mainSock:
            connection, addr = fd.accept()
            connection.setblocking(0)
            self.activeConnections[connection] = bytes()
        elif fd in self.activeConnections:
            dataStr = fd.recv(1024)
            if dataStr:
                self.activeConnections[fd]+=dataStr
                if len(self.activeConnections[fd]) > (100*1024): # 100kB command limit
                    del self.activeConnections[fd]
                    fd.shutdown(socket.SHUT_RDWR)
                    fd.close()
                    print("Network command too long, chopping")
                try:
                    data = json.loads(self.activeConnections[fd])
                except json.JSONDecodeError:
                    return stop
                result, stop = self.processCommand(data)
                fd.send(bytes(json.dumps(result),encoding="utf-8"))
            else:
                del self.activeConnections[fd]
                fd.shutdown(socket.SHUT_RDWR)
                fd.close()
        return stop

    # decode basic command and call appropriate handler
    def processCommand(self, command):
        result = {'success': True}
        stop = False
        print(command)
        print(type(command))
        if not isinstance(command,dict):
            result['success'] = False
            result['error'] = "JSON is not an object"
            return (result, stop)
        if 'request' not in command:
            result['success'] = False
            result['error'] = "Request type missing"
            return (result, stop)
        if command['request'] not in self.commands.keys():
            result['success'] = False
            result['error'] = "Invalid request type"
            return (result, stop)
        if self.commands[command['request']] is not None:
            commandResult, stop = self.commands[command['request']](command)
            return ({**result, **commandResult}, stop)
        return (result, stop)

    def getBands(self, command):
        result = {'success':True, 'bands': {}}
        for band, bandName in self.config.bands.items():
            result['bands'][bandName]=band.dumpBand()
        return (result, False)

    def setTune(self, command):
        result = {'success':True}
        if 'tune' not in command:
            result['success'] = False
            result['error'] = "No tune details"
            return (result, False)
        newconfig = rydeplayer.sources.common.tunerConfig()
        if not newconfig.loadConfig(command['tune'],list(self.config.bands.keys())):
            result['success'] = False
            result['error'] = "Parse Failure, see Ryde log for details"
            return (result, False)
        self.config.tuner.setConfigToMatch(newconfig)
        return (result, False)

    def setMute(self, command):
        result = {'success':True}
        if 'mute' not in command:
            result['success'] = False
            result['error'] = "No mute state specified"
            return (result, False)
        if not isinstance(command['mute'], bool):
            result['success'] = False
            result['error'] = "Mute is not a bool"
            return (result, False)
        self.muteCallback(command['mute'])
        return (result, False)

    def sendEvent(self, command):
        result = {'success':True}
        if 'event' not in command:
            result['success'] = False
            result['error'] = "No event provided"
            return (result, False)
        if command['event'] not in self.eventMap:
            result['success'] = False
            result['error'] = "Invalid event provided"
            return (result, False)
        thisEvent = self.eventMap[command['event']]
        stop = self.eventCallback(thisEvent)
        return (result, stop)

    def debugFire(self, command):
        result = {'success':True}
        if 'function' not in command:
            result['success'] = False
            result['error'] = "No function provided"
            return (result, False)
        if command['function'] not in self.debugFunctions:
            result['success'] = False
            result['error'] = "Invalid function name provided"
            return (result, False)
        self.debugFunctions[command['function']]()
        return (result, False)
