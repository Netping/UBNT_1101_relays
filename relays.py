import socket
import logging




relays_avail = [ 
                { 'name' : 'C1', 'number' : 1 },
                { 'name' : 'C2', 'number' : 2 },
                { 'name' : 'C3', 'number' : 3 },
                { 'name' : 'C4', 'number' : 4 },
                { 'name' : 'C5', 'number' : 5 },
                { 'name' : 'C6', 'number' : 6 },
                { 'name' : 'C7', 'number' : 7 },
                { 'name' : 'C8', 'number' : 8 },
                { 'name' : 'C9', 'number' : 9 },
                { 'name' : 'C10', 'number' : 10 },
                { 'name' : 'C11', 'number' : 11 },
                { 'name' : 'C12', 'number' : 12 },
                { 'name' : 'C13', 'number' : 13 },
                { 'name' : 'C14', 'number' : 14 },
                { 'name' : 'C15', 'number' : 15 },
                { 'name' : 'C16', 'number' : 16 },
                { 'name' : 'C17', 'number' : 17 },
                { 'name' : 'C18', 'number' : 18 },
                { 'name' : 'C19', 'number' : 19 },
                { 'name' : 'C20', 'number' : 20 },
                { 'name' : 'C21', 'number' : 21 },
                { 'name' : 'C22', 'number' : 22 },
                { 'name' : 'C23', 'number' : 23 },
                { 'name' : 'C24', 'number' : 24 },
                { 'name' : 'C25', 'number' : 25 },
                { 'name' : 'C26', 'number' : 26 },
                { 'name' : 'C27', 'number' : 27 },
                { 'name' : 'C28', 'number' : 28 }, 
            ]

class RelaysGroup:
    def __init__(self, list_relays):
        self.__relays = []
        self.__configures = []
        self.__addr = '192.168.0.101'
        self.__TCPport = 2424
        self.__password = 'Laurent'
        self.__sock = None
        self.__TCPblockSize = 1024

        self.__logger = logging.getLogger('UBNT_1101_Relays Group')
        self.__logger.setLevel(logging.ERROR)

        if self.__checkRelays(list_relays) and self.__initialize():
            #create list for self.__relays
            for e in list_relays:
                self.__relays.append({ 'name' : e, 'state' : "OFF" })
        else:
            #log message
            self.__logger.error("Can't init relays group")
            #print("Can't init group")

        #build default name and state_dict
        name = ''
        state_dict = {
            'ON' : [],
            'OFF' : []
        }

        for relay in list_relays:
            e_on = {}
            e_on['name'] = relay
            e_on['state'] = 'ON'
            state_dict['ON'].append(e_on)

            e_off = {}
            e_off['name'] = relay
            e_off['state'] = 'OFF'
            state_dict['OFF'].append(e_off)

            name = name + relay + '_'

        return self.configure(name, state_dict)

    def configure(self, name, state_dict):
        for c in self.__configures:
            if c['name'] == name:
                #message to log
                self.__logger.error("That configure name already exists (" + name + ")")
                #print('That configure name already exists')
                return 1

        element = { 
                    'name' : name,
                    'value' : state_dict,
                    'state' : 'OFF'
                }

        def changeState(arg):
            if arg == name:
                #inversion for self
                if element['state'] == 'OFF':
                    changeState('ON')
                elif element['state'] == 'ON':
                    changeState('OFF')

            elif arg.upper() == 'ON':
                #turn on configure
                for l in element['value']['ON']:
                    for relay in relays_avail:
                        if relay['name'] == l['name']:
                            state = 2

                            if l['state'].upper() == 'OFF':
                                state = 0
                            elif l['state'].upper() == 'ON':
                                state = 1

                            if state == 2:
                                #log message
                                self.__logger.error("Wrong state value (" + l['state'] + ")")
                                return

                            self.__sendCommand(relay['number'] , state)
                            break

                element['state'] = 'ON'

            elif arg.upper() == 'OFF':
                #turn off configure
                for l in element['value']['OFF']:
                    for relay in relays_avail:
                        if relay['name'] == l['name']:
                            state = 2

                            if l['state'].upper() == 'OFF':
                                state = 0
                            elif l['state'].upper() == 'ON':
                                state = 1

                            if state == 2:
                                #log message
                                self.__logger.error("Wrong state value (" + l['state'] + ")")
                                return

                            self.__sendCommand(relay['number'] , state)
                            break

                element['state'] = 'OFF'

        self.__configures.append(element)

        return changeState

    def __checkRelays(self, list_relays):
        for e in list_relays:
            flag = False

            for l in relays_avail:
                if e == l['name']:
                    flag = True
                    break

            if not flag:
                return False

        return True

    def __initialize(self):
        #check connection
        if self.__initConnection():
            return False

        self.__relaysOff()

        return True

    def __relaysOff(self):
        for e in relays_avail:
            if self.__sendCommand(e['number'], 0):
                #TODO log message
                self.__logger.error("Error in setting relay " + e['number'] + " to OFF state")
                pass

    def __initConnection(self):
        if not self.__sock:
            self.__sock = socket.socket()
            self.__sock.connect( (self.__addr, self.__TCPport) )

        #check connection
        self.__sock.send(b"$KE\r\n")
        rcv_data = self.__sock.recv(self.__TCPblockSize)

        if not ("#OK" in rcv_data.decode("utf-8")):
            #log message
            self.__logger.error("Can't connect to device (ip: " + self.__addr + " port: " + self.__TCPport)
            #print("Can't connect to device")
            return 1

        #set password
        self.__sock.send(b"$KE,PSW,SET," + self.__password.encode() + b"\r\n")
        rcv_data = self.__sock.recv(self.__TCPblockSize)

        if not ("#PSW,SET,OK" in rcv_data.decode("utf-8")):
            #log message
            self.__logger.error("Can't set password for device (ip: " + self.__addr + " port: " + self.__TCPport)
            #print("Can't set password")
            return 2

        return 0

    def __sendCommand(self, num, state):
        self.__sock.send(b"$KE,REL," + str(num).encode() + b"," + str(state).encode() + b"\r\n")
        rcv_data = self.__sock.recv(self.__TCPblockSize)

        if not ("#REL,OK" in rcv_data.decode("utf-8")):
            #log message
            #print('Error in setting relay ' + str(num) + ' to ' + str(state))
            self.__logger.error('Error in setting relay ' + str(num) + ' to ' + str(state))
            return 1

        return 0
