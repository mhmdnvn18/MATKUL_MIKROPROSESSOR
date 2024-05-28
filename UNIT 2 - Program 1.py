from machine import Pin
from time import sleep
led = [0, 0, 0, 0]
led[3] = Pin(26, Pin.OUT)
led[2] = Pin(25, Pin.OUT)
led[1] = Pin(33, pin.OUT)
led[0] = Pin(32, Pin.OUT)
while True:
  led[0].value(1)
  sleep(1)
  led[0].value(0)
  led[1].value(1)
  sleep(1)
  led[1].value(0)
  led[2].value(1)
  sleep(1)
  led[2].value(0)
  led[3].value(1)
  sleep(1)
  led[3].value(0)
