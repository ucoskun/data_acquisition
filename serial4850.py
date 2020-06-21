# Module for STP-DRV-4850 serial communication

import time
import serial

class Serial4850:
    def __init__(self, port_path):

        self.port_path = port_path

        self.ser = serial.Serial(port = port_path, baudrate = 9600, parity = serial.PARITY_NONE, stopbits = serial.STOPBITS_ONE, bytesize = serial.EIGHTBITS)

        self.ser.isOpen()

    def rotate(self, numbers):

        print("Rotating by", str(numbers))
        self.ser.write(("FL" + str(numbers) + "\r").encode('ascii'))