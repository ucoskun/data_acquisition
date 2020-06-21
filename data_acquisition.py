import pyvisa
import time
import serial
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import serial4850
import relaycontrol

volt_uT = 100
uT_mG = 10

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
dmm.write('VOLT:ZERO:AUTO 0')       # Turn auto zero off
dmm.write('TRIG:SOUR IMM')          # Trigger immediately
dmm.write('TRIG:DEL 0.1')           # First measurement delay
dmm.write('SAMPLE:SOURCE TIM')
dmm.write('SAMPLE:TIM 200E-3')      # Time gap between the readings
dmm.write('SAMPLE:COUNT 5')         # Number of counts
dmm.write('CALC:STAT ON')           # Enable statistics
dmm.write('CALC:FUNC AVER')         # Select averaging operations

time.sleep(1)

init_time = time.time()

def measure(sleep_time):
    dmm.write('CALC:AVER:CLEAR')
    dmm.write('SENS:VOLT:DC:ZERO:AUTO ONCE')
    dmm.write('INIT')

    time.sleep(sleep_time)

    volt = float(dmm.query('CALC:AVER:AVER?'))
    volt_std = float(dmm.query('CALC:AVER:SDEV?'))

    uT = round(volt * volt_uT, 3)
    uT_std = round(volt_std * volt_uT, 3)

    return uT, uT_std

# Make sure power is of in the beginning and wait for 8 seconds


for i in range(3):
    power.power_state(0)
    time.sleep(8)
    field, field_std = measure(2.5)
    print(field, field_std)
    power.power_state(1)
    time.sleep(5)
    motor.rotate(10000)
    time.sleep(4)
    power.power_state(0)
    time.sleep(9)
    field_flip, field_flip_std = measure(2.5)
    print(field_flip, field_flip_std)
    offset = (field + field_flip) * 0.5
    print("Offset:", offset, "uT")
    power.power_state(1)
    time.sleep(5)
    motor.rotate(-10000)
    time.sleep(4)
    power.power_state(0)