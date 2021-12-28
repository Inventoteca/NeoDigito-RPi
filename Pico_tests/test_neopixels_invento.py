# Test Neopixels
# Based on example of 330ohms
#
# Notes:
# Don't run as main.py, it will brick the RPi Pico
# Change infinite while loop and use a Timer
# https://forums.raspberrypi.com/viewtopic.php?t=321332
# https://forums.raspberrypi.com/viewtopic.php?t=305432

import array, utime
from machine import Pin
import rp2
from rp2 import PIO, StateMachine, asm_pio

# Configure the number of WS2812 LEDs.
NUM_LEDS = 48

@asm_pio(sideset_init=PIO.OUT_LOW, out_shiftdir=PIO.SHIFT_LEFT, autopull=True, pull_thresh=24)
def ws2812():
    T1 = 2
    T2 = 5
    T3 = 3
    label("bitloop")
    out(x, 1) .side(0) [T3 -1]
    jmp(not_x, "do_zero") .side(1) [T1 -1]
    jmp("bitloop") .side(1) [T2 - 1]
    label("do_zero")
    nop() .side(0) [T2 - 1]
    
# Create the StateMachine with the ws2812 program
sm = StateMachine(0, ws2812,freq=8000000, sideset_base=Pin(0))

#Start the StateMachine, it will wait for data on its FIFO
sm.active(1)

ar = array.array("I", [0 for _ in range (NUM_LEDS)])

while 1:
    print("blue")
    #for j in range (0,128):
    for i in range (NUM_LEDS):
        ar[i] = 10
    sm.put(ar,8)
    utime.sleep_ms(200)

    print("red")
    #for j in range (0,128):
    for i in range (NUM_LEDS):
        ar[i] = 10<<8
    sm.put(ar,8)
    utime.sleep_ms(200)

    print("green")
    #for j in range (0,128):
    for i in range (NUM_LEDS):
        ar[i] = 10<<16
    sm.put(ar,8)
    utime.sleep_ms(200)

    print("white")
    #for j in range (0,10):
    for i in range (NUM_LEDS):
        ar[i] = (5<<16) + (5<<8) + 5
    sm.put(ar,8)
    utime.sleep_ms(200)
