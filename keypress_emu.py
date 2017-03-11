import serial
from serial.tools import list_ports
from pykeyboard import PyKeyboard
import sys
import select

ports = list_ports.comports()

k = PyKeyboard()
keys = 'W A S D E U H J K I'.split()

if ports:
    ser = serial.Serial(ports[0].device, 115200, timeout=0)

    while True:
        char = ser.read()

        if char:
            code = ord(char)
            index = code >> 1
            state = code & 1

            if state == 1:
                k.press_key(keys[index])
            else:
                k.release_key(keys[index])

        if sys.stdin in select.select([sys.stdin], [], [], 0)[0]:
            command = sys.stdin.readline().strip()

            if command:
                ser.write(command[0])

else:
    print 'No serial ports found'
