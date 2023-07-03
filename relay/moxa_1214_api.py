# py modules

import sys
from relay import moxa_api


# constants
POWER_ON = 1
POWER_OFF = 0
#name of the data to be read/write from/to moxa device
PARAMETER_NAME = "relay"

# method for checking value of pin_number
# parameters:
# pin_number - int value of pin_number
# return:
# True or False
def check_pin_number(pin_number):
    if pin_number < 0 or pin_number > 5:
        print(
            "ERROR! wrong pin_number value: " +
            str(pin_number))
        return False
    else:
        return True


class MoxaRelay:
    """
    Class to manage relay: open and close it
    """
    def __init__(self, ip):
        self.__ip = ip
        self.pull_status()
        return
    
  
    def pull_status(self):
        #TODO: add raise exeption if cant write 
        self.__status = moxa_api.get_moxa_value(self.__ip, PARAMETER_NAME)
        return

    
    def push_status(self):
        #TODO: add raise exeption if cant write 
        res = moxa_api.set_moxa_value(self.__ip, PARAMETER_NAME, self.__status)
        return
    
    def get_pin(self, pin):
        if check_pin_number(pin):
            return self.__status['io']['relay'][pin]['relayStatus']
        
    def set_pin(self, pin, v):
        if check_pin_number(pin):
            self.__status['io']['relay'][pin]['relayStatus'] = 1 if v else 0
    
    