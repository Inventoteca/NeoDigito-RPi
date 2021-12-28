from machine import Pin, Timer
led = Pin(25, Pin.OUT)
timer = Timer()
#k = 0

def blink(timer):
    led.toggle()
    #global k
    #print(k)
    #k += 1
    
timer.init(freq=2.0, mode=Timer.PERIODIC, callback=blink)
