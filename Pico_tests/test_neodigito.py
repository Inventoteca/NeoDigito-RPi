# Test Neopixels 2
# Based on https://core-electronics.com.au/tutorials/how-to-use-ws2812b-rgb-leds-with-raspberry-pi-pico.html
# Print numbers
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
NUM_LEDS = 32

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

def pixels_set(i, color):
    ar[i] = (color[1]<<16) + (color[0]<<8) + color[2]

SevenSegmentASCII = (
    0b0000000000000000, #(space)
    0b10000110, # !
    0b00100010, # "
    0b01111110, # #
    0b01101101, # $
    0b11010010, # %
    0b01000110, # &
    0b00100000, # '
    0b00101001, # (
    0b00001011, # )
    0b00100001, # *
    0b01110000, # +
    0b00010000, # ,
    0b01000000, # -
    0b10000000, # .
    0b01010010, # /
    0b0111111001111110, # 0
    0b0110000001100000, # 1
    0b0001111111111000, # 2
    0b0111100111111000, # 3
    0b0110000111100110, # 4
    0b0111100110011110, # 5
    0b0111111110011110, # 6
    0b0110000001111000, # 7
    0b0111111111111110, # 8
    0b0111100111111110, # 9
    0b00001001, # :
    0b00001101, # ;
    0b01100001, # <
    0b01001000, # =
    0b01000011, # >
    0b11010011, # ?
    0b01011111, # @
    0b01110111, # A
    0b01111100, # B
    0b00111001, # C
    0b01011110, # D
    0b01111001, # E
    0b01110001, # F
    0b00111101, # G
    0b01110110, # H
    0b00110000, # I
    0b00011110, # J
    0b01110101, # K
    0b00111000, # L
    0b00010101, # M
    0b00110111, # N
    0b00111111, # O
    0b01110011, # P
    0b01101011, # Q
    0b00110011, # R
    0b01101101, # S
    0b01111000, # T
    0b00111110, # U
    0b00111110, # V
    0b00101010, # W
    0b01110110, # X
    0b01101110, # Y
    0b01011011, # Z
    0b00111001, # [
    0b01100100, # \
    0b00001111, # ]
    0b00100011, # ^
    0b00001000, # _
    0b00000010, # `
    0b01011111, # a
    0b01111100, # b
    0b01011000, # c
    0b01011110, # d
    0b01111011, # e
    0b01110001, # f
    0b01101111, # g
    0b01110100, # h
    0b00010000, # i
    0b00001100, # j
    0b01110101, # k
    0b00110000, # l
    0b00010100, # m
    0b01010100, # n
    0b01011100, # o
    0b01110011, # p
    0b01100111, # q
    0b01010000, # r
    0b01101101, # s
    0b01111000, # t
    0b00011100, # u
    0b00011100, # v
    0b00010100, # w
    0b01110110, # x
    0b01101110, # y
    0b01011011, # z
    0b01000110, # {
    0b00110000, # |
    0b01110000, # }
    0b00000001, # ~
    0b00000000, #(del)
)

#print(ord('0'))
#print(pattern)
kolor = (0, 5, 10)
pattern = SevenSegmentASCII[ord('0')-32]

for i in range(16):
    if pattern & (1 << i):
        pixels_set(i, kolor)
    else:
        pixels_set(i, (0,0,0))
        
pattern = SevenSegmentASCII[ord('4')-32]
        
for i in range(16):
    if pattern & (1 << i):
        pixels_set(i+16, kolor)
    else:
        pixels_set(i+16, (0,0,0))
        
sm.put(ar, 8)
