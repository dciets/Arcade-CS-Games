import serial
from serial.tools import list_ports
from pykeyboard import PyKeyboard

ports = list_ports.comports()
k = PyKeyboard()
keys = 'W A S D E U H J K I'.split()

if ports:
    ser = serial.Serial(ports[0].device, 115200)

    while True:
        c = ord(ser.read())
        index = c >> 1
        state = c & 1

        if state == 1:
            k.press_key(keys[index])
        else:
            k.release_key(keys[index])

else:
    print 'No serial ports found'
