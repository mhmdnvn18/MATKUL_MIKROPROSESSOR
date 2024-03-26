from machine import Pin, Timer, TouchPad
from micropython import const
import time
def zfill(s, width):
    return '{:0>{w}}'.format(s, w=width)
led = [0, 0, 0, 0]
led[3] = Pin(26, Pin.OUT)
led[2] = Pin(25, Pin.OUT)
led[1] = Pin(33, Pin.OUT)
led[0] = Pin(32, Pin.OUT)
PB_IN_1 = const(17)
PB_IN_2 = const(16) 
PB_IN_3 = const(4)
decimal = 0
threshold = 250
class debouncing:
    def __init__(self, pin, callback, trigger=Pin.IRQ_FALLING,min_ago=300):
        self.callback = callback
        self.min_ago = min_ago
        self.blocked = False
        self._next_call = time.ticks_ms() + self.min_ago
        pin.irq(trigger=trigger, handler=self.debounce_handler)
    def call_callback(self, pin):
        self.callback(pin)
    def debounce_handler(self, pin):
        if time.ticks_ms() > self._next_call:
            self.next_call = time.ticks_ms() + self.min_ago
            self.call_callback(pin)
def button_1_callback(pin):
    global decimal
    decimal = decimal + 1
def button_2_callback(pin):
    global decimal
    decimal = decimal - 1
button_1 = debouncing(pin=Pin(PB_IN_1, mode=Pin.IN, pull=Pin.PULL_UP), callback=button_1_callback)
button_2 = debouncing(pin=Pin(PB_IN_2, mode=Pin.IN, pull=Pin.PULL_UP), callback=button_2_callback)
touch_1 = TouchPad(Pin(PB_IN_3, mode=Pin.IN))
while True:
    data_touch_1 = touch_1.read()

    if touch_1.read() < threshold:
        time.sleep(0.2)
        if touch_1.read() < threshold:
            time.sleep(0.2)
            decimal = decimal - 1
    if decimal > 15:
            decimal = 15
    elif decimal < 0:
            decimal = 0
    binary = bin(decimal) [2:]
    four_bit = zfill(binary, 4)
    print("four_bit: {}, decimal: {}, touch:{}".format(four_bit, decimal, data_touch_1))
    #time.sleep(1)
    for i in range (4):
        led[i].value(int(four_bit[i]))

