from machine import I2C, Pin
from pico_i2c_lcd import I2cLcd
from machine import Pin
import machine
import utime
import neopixel
import time
np = neopixel.NeoPixel(machine.Pin(13),8)
np[1] = [0,0,255]

"""
From the 1602A LCD Datasheet. The I2C 1602 LCD module is a 2 line by 16 character display interfaced to an I2C daughter board.
Specifications: 2 lines by 16 characters
I2C Address Range: 0x20 to 0x27 (Default=0x27, addressable) 
Operating Voltage: 5 Vdc 
Contrast: Adjustable by potentiometer on I2C interface
Size: 80mm x 36mm x 20 mm
Viewable area: 66mm x 16mm 

Drivers provided by https://www.circuitschools.com/
Note: Adjust the potentiometer when you do not see any characters on the display 
"""

i2c = I2C(0, sda=Pin(8), scl=Pin(9), freq=400000)

I2C_ADDR = i2c.scan()[0]
lcd = I2cLcd(i2c, I2C_ADDR, 2, 16)

adcpin = 4
sensor = machine.ADC(adcpin)



def status(t, name, game):
    lcd.clear()
    scroll_position = 0

    if t == '0':
        print(I2C_ADDR, "| Hex:", hex(I2C_ADDR))
        lcd.move_to(0, 0)
        lcd.putstr(f'{name} is:')
        lcd.move_to(0, 1)
        lcd.putstr('Offline')
    elif t == '1':
        print(I2C_ADDR, "| Hex:", hex(I2C_ADDR))
        lcd.move_to(0, 0)
        lcd.putstr(f'{name} is:')
        lcd.move_to(0, 1)
        lcd.putstr(f'online is {game}')
    elif t == '2':
        print(I2C_ADDR, "| Hex:", hex(I2C_ADDR))
        lcd.move_to(0, 0)
        lcd.putstr(f'{name} is:')
        lcd.move_to(0, 1)
        lcd.putstr('Busy')
    elif t == '3':
        print(I2C_ADDR, "| Hex:", hex(I2C_ADDR))
        lcd.move_to(0, 0)
        lcd.putstr(f'{name} is:')
        lcd.move_to(0, 1)
        lcd.putstr('Away')
    elif t == '4':
        print(I2C_ADDR, "| Hex:", hex(I2C_ADDR))
        lcd.move_to(0, 0)
        lcd.putstr(f'{name} is:')
        lcd.move_to(0, 1)
        lcd.putstr('Snooze')
    elif t == '5':
        print(I2C_ADDR, "| Hex:", hex(I2C_ADDR))
        lcd.move_to(0, 0)
        lcd.putstr(f'{name} is:')
        lcd.move_to(0, 1)
        lcd.putstr('Looking to trade')
    elif t == '6':
        print(I2C_ADDR, "| Hex:", hex(I2C_ADDR))
        lcd.move_to(0, 0)
        lcd.putstr(f'{name} is:')
        lcd.move_to(0, 1)
        lcd.putstr('Looking to play')
    else:
        print(I2C_ADDR, "| Hex:", hex(I2C_ADDR))
        lcd.move_to(0, 0)
        lcd.putstr('gebruiker is:')
        lcd.move_to(0, 1)
        lcd.putstr('Prive')

def neoPixel(st):
    if st == '0':
        np[0] = [255, 0, 0]
    elif st == '1':
        np[0] = [0,255,0]
    np.write()
    time.sleep(1)

while True:
    t = input()
    st, name, game = t.split(';')
    print(t)
    status(st, name, game)
   

