from time import sleep, ticks_ms
from math import sin, pi
from machine import Pin
from random import randint
from neopixel import NeoPixel

pin = 28
lights = 25

np = NeoPixel(Pin(pin), lights)

while True:
    ms = ticks_ms()
    for light in range(lights):

        phase = int(ms / 30) % 100 / 100 # 0 to 1
        offset_phase = (phase + light / lights / 2) % 1
        brightness = int(50 * (sin(2 * pi * offset_phase) + 1))

        np[light] = (0, 0, brightness)    
        np.write()

