
# Module for Arduino Relay power control

import time
import serial

class RelayControl:
    def __init__(self, port_path, baud = 9600, write_timeout = 1, timeout = 3):

        self.port_path = port_path
        self.ser = serial.Serial('COM3', 9600, timeout = 3)
        self.ser.isOpen()
        print('ATMega bootloader is loading')
        time.sleep(4)
        print('Done.')

    def power_state(self, state):
        # state = 1 (ON) or 0 (OFF)
        print('Power changed to', str(state))
        self.ser.write(("0" + str(state)).encode('ascii'))
