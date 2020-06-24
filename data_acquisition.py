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



def measure():

    volt = float(dmm.query('READ?'))

    nT = round(volt * volt_nT, 1)

    return nT

# Make sure power is of in the beginning and wait for 8 seconds
offset_out = open("offset_1_6-24-2020-rand.txt", "w+")
measure_out = open("field_1_6-24-2020-rand.txt", "w+")

init_time = time.time()

angle_list = [i for x in range(0, 20200, 200)]

for i in angle_list:

    field = []
    field_flip = []
    power.power_state(0)
    time.sleep(10)

    for i in range(10):
        cur_field = measure()
        field.append(cur_field)
        time.sleep(0.3)
        rel_time = time.time() - init_time
        print("0 deg Field =", cur_field, "nT", "Time = ", rel_time)
        measure_out.write(str(rel_time) + " " + str(cur_field) + "\n")
    
    power.power_state(1)
    time.sleep(6)
    motor.rotate(200)
    time.sleep(4)
    power.power_state(0)
    time.sleep(10)

    for i in range(10):
        cur_field = measure()
        field_flip.append(cur_field)
        time.sleep(0.3)
        rel_time = time.time() - init_time
        print("180 deg Field =", cur_field, "nT", "Time = ", rel_time)
        measure_out.write(str(rel_time) + " " + str(cur_field) + "\n")

    offset = (np.mean(field) + np.mean(field_flip)) * 0.5
    print("Offset:", offset, "nT")
    offset_out.write(str(offset) + "\n")
    power.power_state(1)
    time.sleep(6)
    motor.rotate(-10000)
    time.sleep(4)
    print("Doing random rotation")
    motor.rotate(np.random.randint(10000)-5000)
    time.sleep(4)
    power.power_state(0)

offset_out.close()
measure_out.close()