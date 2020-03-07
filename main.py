""" monitor_main.py
Blink ternary counting pattern on neopixels
Designed for a strip of neopixels on the back of a monitor
0 = red
1 = green
2 = blue
"""
import machine
import math
import neopixel
import utime

pin = 14
lights = 48
level = 10

np = neopixel.NeoPixel(machine.Pin(pin), lights)

while True:

    # seconds since the device was powered on
    # devided to increment every 1/4 of a second
    t = int( utime.ticks_ms() / 250 )

    for i in range(0, lights):

        # Repeat the pattern every 10 neopixels
        i_prime = i % 10

        # Calculate the value of the i_prime digit
        v = int( t / pow (3, i_prime)) % 3

        r = (v == 0) * level
        g = (v == 1) * level
        b = (v == 2) * level

        np[i] = ( r, g, b)

    np.write()