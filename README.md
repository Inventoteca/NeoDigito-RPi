# NeoDigito-RPi
This is a WIP.  
NeoDigito library port to Python and MicroPython, compatible with Raspberry Pi.  
The original library was developed for Arduino https://github.com/Inventoteca/NeoDigito  

The Python version is compatible with Raspberry Pi computers.  

The MicroPython is compatible with Raspberry Pi Pico.  

The library must have this features:
- Work with displays of 7, 14 and 16 segments
- Smart use of delimiters (decimal separator and colon)
- Configurable segment order
- Color effects
- Configurable number of LEDs per segment

The displays can have delimiters or not.  
Create different pattern sets for different NeoDigito models. Take inspiration from here https://github.com/dmadison/LED-Segment-ASCII  
Patterns are grouped in Python tuples (working as constant arrays).

The order of segments can be defined as a string
```
For example 'abcdefg' for a 7-segment display
 aaa
f   b
f   b
 ggg
e   c
e   d
 ddd
```
