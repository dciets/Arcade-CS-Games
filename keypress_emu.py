import serial
from serial.tools import list_ports
from pykeyboard import PyKeyboard

ser = None
l = [p for p in list_ports.comports()]
for port in l:
    if 'ttyUSB' in port.device:
        ser = serial.Serial(port.device, 9600)
        print port.device
        break
k = PyKeyboard()
while True:
    s = ser.readline()
    key = int(s.strip())
    k.tap_key(key)