import urllib




relay_avail = [ 
                { name: 'C1', number: 1 },
                { name: 'C2', number: 2 },
                { name: 'C3', number: 3 },
                { name: 'C4', number: 4 },
                { name: 'C5', number: 5 },
                { name: 'C6', number: 6 },
                { name: 'C7', number: 7 },
                { name: 'C8', number: 8 } 
            ]

class RelaysGroup:
    def __init__(self, list_relays):
        self.__relays = []

        if self.__checkRelays(list_relays):
            #create list for self.__relays
            for e in list_relays:
                self.__relays.append({ name: e, state: "OFF" })

        self.__configures = []
        self.__password = ''

    def configure(self, name, state_dict):
        pass

    def setPassword(self, password):
        self.__password = password

    def getRelays(self):
        return self.__relays

    def __checkRelays(self, list_relays):
        for e in list_relays:
            flag = False

            for l in relay_avail:
                if e == l['name']:
                    flag = True
                    break

            if not flag:
                return False

        return True

    def __initialize(self):
        #TODO check connection
        self.__relaysOff()

    def __relaysOff(self):
        pass
