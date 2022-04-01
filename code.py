# SPDX-FileCopyrightText: 2018 Kattni Rembor for Adafruit Industries
#
# SPDX-License-Identifier: MIT

"""CircuitPython Essentials NeoPixel RGBW example"""
import time
import board
import neopixel

pixel_pin = board.A0
num_pixels = 60

pixels = neopixel.NeoPixel(
    pixel_pin, num_pixels, brightness=0.3, auto_write=False, pixel_order=(1, 0, 2, 3)
)

pixel = neopixel.NeoPixel(board.NEOPIXEL, 1)

BACK_LIGHT = list(range(55, 59))
BACK_LIGHT.extend(list(range(0,18)))
FRONT_LIGHT = range(31, 42)
LEFT_SIGNAL = range(18, 31)
RIGHT_SIGNAL = range(40, 55)

WHITE = (255, 255, 255, 0)
RED = (255, 0, 0, 0)
YELLOW = (255, 150, 0, 0)
GREEN = (0, 255, 0, 0)
CYAN = (0, 255, 255, 0)
BLUE = (0, 0, 255, 0)
PURPLE = (180, 0, 255, 0)
BLACK = (0, 0, 0, 0)

MODE_LEFT = 1
MODE_RIGHT = 2
MODE_STOP = 3
MODE_NUMBERS = 4
MODE_CYCLE = 5
MODE_WHEEL = 6
MODE_VEHICLE = 7
MODE_CALM_BREATHING = 8
MODE = MODE_CALM_BREATHING


def colorwheel(pos):
    # Input a value 0 to 255 to get a color value.
    # The colours are a transition r - g - b - back to r.
    if pos < 0 or pos > 255:
        return (0, 0, 0, 0)
    if pos < 85:
        return (255 - pos * 3, pos * 3, 0, 0)
    if pos < 170:
        pos -= 85
        return (0, 255 - pos * 3, pos * 3, 0)
    pos -= 170
    return (pos * 3, 0, 255 - pos * 3, 0)


def color_chase(color, wait):
    for i in range(num_pixels):
        pixels[i] = color
        time.sleep(wait)
        pixels.show()
    time.sleep(0.5)


def breathe(wait):
    while True:
        for color in [BLUE, CYAN, PURPLE]:
            for bt in [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]:
                pixels.brightness = bt
                pixels.fill(color)
                pixels.show()
                time.sleep(0.1)
            for bt in [1.0, 0.9, 0.8, 0.7, 0.6, 0.5, 0.4, 0.3, 0.2, 0.1]:
                pixels.brightness = bt
                pixels.fill(color)
                pixels.show()
                time.sleep(0.1)

def rainbow_cycle(wait):
    for j in range(255):
        for i in range(num_pixels):
            rc_index = (i * 256 // num_pixels) + j
            pixels[i] = colorwheel(rc_index & 255)
        pixels.show()
        time.sleep(wait)
        pixel[0] = colorwheel(j)

def rainbow_wheel(wait):
    for j in range(255):
        for i in range(num_pixels):
            pixels[i] = colorwheel(j & 255)
        pixels.show()
        time.sleep(wait)
        pixel[0] = colorwheel(j)


while True:
    if MODE in [MODE_NUMBERS, MODE_LEFT, MODE_RIGHT, MODE_STOP, MODE_VEHICLE]:
        for i in range(num_pixels):
            if MODE == MODE_STOP:
                pixels.fill(RED)
            else:
                for j in range(num_pixels):
                    if MODE == MODE_NUMBERS:
                        if i == j:
                            pixels[j] = YELLOW
                            print(i)
                        else:
                            pixels[j] = BLACK
                    if MODE == MODE_LEFT:
                        if j in LEFT_SIGNAL:
                            pixels[j] = YELLOW
                        else:
                            pixels[j] = BLACK
                    if MODE == MODE_RIGHT:
                        if j in RIGHT_SIGNAL:
                            pixels[j] = YELLOW
                        else:
                            pixels[j] = BLACK
                    if MODE == MODE_VEHICLE:
                        if j in FRONT_LIGHT:
                            pixels[j] = WHITE
                        elif j in BACK_LIGHT:
                            pixels[j] = RED
                        else:
                            pixels[j] = BLACK

            pixels.show()
            if MODE in [MODE_LEFT, MODE_RIGHT, MODE_STOP]:
                time.sleep(0.5)
                pixels.fill(BLACK)
                pixels.show()
                time.sleep(0.5)
    # Increase the number to slow down the rainbow
    if MODE == MODE_WHEEL:
        rainbow_wheel(0)
# #     color_chase(RED, 0.1)  # Increase the number to slow down the color chase
    elif MODE == MODE_CALM_BREATHING:
        breathe(0)
    elif MODE == MODE_CYCLE:
        rainbow_cycle(0)

