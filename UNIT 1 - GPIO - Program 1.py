# Program ini digunakan untuk menyalakan/mematikan LED menggunakan GPIO

# Impor library untuk GPIO
from machine import Pin

# Impor library untuk fungsi sleep/delay
from time import sleep

# Inisialisasi sebuah list yang dinamai 'led'
led = [0, 0, 0, 0]

# Susun MSB hingga LSB dan GPIO LED sebagai output
led[3] = Pin(26, Pin.OUT)
led[2] = Pin(25, Pin.OUT)
led[1] = Pin(33, Pin.OUT)
led[0] = Pin(32, Pin.OUT)

# Program utama dieksekusi setiap 1000 x 44000 ms
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


# Program utama dieksekusi setiap 1000 x 44000 ms

