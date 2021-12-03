#!/usr/bin/python3
from relays import *




def main():
    conf_dict_1 = {
        'ON' : [
                    {
                        'name' : 'C1',
                        'state' : 'ON'
                    },
                    {
                        'name' : 'C2',
                        'state' : 'OFF'
                    }
                ],

        'OFF' : [
                    {
                        'name' : 'C1',
                        'state' : 'OFF'
                    },
                    {
                        'name' : 'C2',
                        'state' : 'ON'
                    }
                ]
    }

    group = RelaysGroup(['C1','C2'])

    DischargeLoad_2 = group.configure("Discharge2", conf_dict_2)

    DischargeLoad_2('ON')

if __name__ == "__main__":
    main()
