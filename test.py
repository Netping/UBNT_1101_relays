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

    conf_dict_2 = {
        'ON' : [
                    {
                        'name' : 'C1',
                        'state' : 'ON'
                    },
                    {
                        'name' : 'C2',
                        'state' : 'ON'
                    }
                ],

        'OFF' : [
                    {
                        'name' : 'C1',
                        'state' : 'OFF'
                    },
                    {
                        'name' : 'C2',
                        'state' : 'OFF'
                    }
                ]
    }

    group = RelaysGroup(['C1','C2'])

    DischargeLoad_1 = group.configure("Discharge1", conf_dict_1)
    DischargeLoad_2 = group.configure("Discharge2", conf_dict_2)

    DischargeLoad_1('OFF')
    DischargeLoad_2('ON')

    DischargeLoad_1('Discharge1')

if __name__ == "__main__":
    main()
