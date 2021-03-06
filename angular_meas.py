import pyvisa
import time
import serial
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import serial4850
import relaycontrol

volt_uT = 10

# Initialize serial communication with Step Motor Driver
motor = serial4850.Serial4850('COM5')

# Initialize serial communication with Arduino
power = relaycontrol.RelayControl('COM3')

# Initialize the Agilent DMM connected to Mag-01H
rm = pyvisa.ResourceManager()
dmm = rm.open_resource('USB0::0x0957::0x0A07::MY48003317::0::INSTR')
print(dmm.query('*IDN?'))

# Reset DMM and configure
dmm.write('*RST')                   # Reset the settings
dmm.write('SENS:VOLT:DC:NPLC 10')   # NPLC = 10 (Can change later)
dmm.write('VOLT:DC:IMP:AUTO 1')     # 10G Input Impedance
dmm.write('VOLT:RANG 1')            # Voltage full scale range
dmm.write('VOLT:ZERO:AUTO 1')       # Turn auto zero off
dmm.write('TRIG:SOUR IMM')          # Trigger immediately
dmm.write('TRIG:DEL 0.1')           # First measurement delay

time.sleep(1)

init_time = time.time()

def measure():

    volt = float(dmm.query('READ?'))

    uT = round(volt * volt_uT, 4)

    return uT

# Make sure power is of in the beginning and wait for 8 seconds

offset_out = open("angular_sample.txt", "w+")

for i in range(0,41):
    power.power_state(1)
    time.sleep(6)
    motor.rotate(500)
    time.sleep(3)
    power.power_state(0)
    time.sleep(10)
    field, field_std = measure()
    print(field, field_std)
    offset_out.write(str(field) + " " + str(field_std) + "\n")

offset_out.close()
