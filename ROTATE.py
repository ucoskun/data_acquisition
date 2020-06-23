import serial4850

# Initialize serial communication with Step Motor Driver
motor = serial4850.Serial4850('COM5')
motor.rotate(-20000)
