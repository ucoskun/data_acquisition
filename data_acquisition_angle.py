import pyvisa
import time
import serial
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import serial4850
import relaycontrol

volt_uT = 10
volt_nT = 10000
uT_mG = 10

# Initialize serial communication with Step Motor Driver
motor = serial4850.Serial4850('COM1')

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



def measure():

    volt = float(dmm.query('READ?'))

    nT = round(volt * volt_nT, 1)

    return nT

# Make sure power is of in the beginning and wait for 8 seconds
measure_out = open("ang_vs_field_7_5_2020_probe19_run1.txt", "w+")

init_time = time.time()

angle_list = [x for x in range(0, 20400, 400)]

for i in angle_list:

    field = []
    power.power_state(0)
    time.sleep(10)

    for i in range(2):
        cur_field = measure()
        field.append(cur_field)
        time.sleep(0.3)
        rel_time = time.time() - init_time
        print("B_read =", cur_field, "nT", "Time =", round(rel_time, 1), "s")

    measure_out.write(str(i) + " " + str(np.mean(field)) + "\n")
    
    power.power_state(1)
    time.sleep(10)
    motor.rotate(400)
    time.sleep(2)

measure_out.close()
