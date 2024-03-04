import serial
import time
SERIAL_PORT = '/dev/ttyS0' 
def validate_rfid(code):
 
    s = code.decode("ascii")


    if (len(s) == 12) and (s[0] == "\n") and (s[11] == "\r"):
     return s[1:-1]
    
    else:
     return False


ser = serial.Serial(baudrate = 2400,  bytesize = serial.EIGHTBITS,  parity = serial.PARITY_NONE,  port = SERIAL_PORT, stopbits = serial.STOPBITS_ONE,  timeout = 1)


def ser_read():
    while True:
        ser.flushInput()
        ser.flushOutput()
        data=ser.read(12)
        code = validate_rfid(data)
        if code:
            print(code)
            return code
        
##while True:
   ## ser_read()
    


