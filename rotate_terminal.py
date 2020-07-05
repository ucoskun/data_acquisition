import serial4850

# Initialize serial communication with Step Motor Driver
motor = serial4850.Serial4850('COM1')

inputt=1
while 1 :
    # get keyboard input
    inputt = input(">> ")
        # Python 3 users
        # input = input(">> ")
    if inputt == 'exit':
        exit()
    else:
        # send the character to the device
        # (note that I happend a \r\n carriage return and line feed to the characters - this is requested by my device)
        motor.rotate(int(inputt))
