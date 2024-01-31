from machine import I2C, Pin
from pico_i2c_lcd import I2cLcd
from machine import Pin
import machine
import utime
import neopixel
import time

np = neopixel.NeoPixel(machine.Pin(15), 8)

def neoPixel(st):
    if st == '0':
        for x in range(8):
            np[x] = [255, 0, 0]
    elif st == '1':
        for x in range(8):
            np[x] = [0, 255, 0]
    else:
        for x in range(8):
            np[x] = [255,255,0]
    np.write()
    time.sleep(1)


while True:
    t = input()
    st, name, game = t.split(';')
    neoPixel(st)



