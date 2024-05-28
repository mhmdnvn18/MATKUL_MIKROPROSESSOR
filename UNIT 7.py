from machine import Pin, I2C, Timer
from time import sleepimport ssd1306
import mpu6050
import math
from bmp180 import bmp180
timer = Timer(0)
i2c = I2C (sda=PIN(21), scl=Pin(22))
display = ssd1306.SSD1306_I2C(128, 64, i2c)
mpu = mpu6050.accel(i2c)
bmp180 = BMP180(i2c)
bmp180.oversample_sett = 2
bmp180.baseline = 101325
altitude, pitch, roll = 0, 0, 0
display.fill(0)
display.fill_rect(0, 0, 32, 32, 1)
displat.fill_rect(2, 2, 28, 28, 0)
display.vline(9, 8, 22, 1)
display.vline(16, 2, 22, 1)
display.vline(23, 8, 22, 1)
display.fill_rect(26, 24, 2, 4, 1)
display.text('Micropython', 40, 0, 1)
display.text('Project', 40, 12, 1)
display.text('EE - UMY', 40, 24, 1)
display.show()
def handleInterrup (timer):
    global altitude, pitch, roll
    display.fill_rect(0, 35, 128, 64, 0)
    display.text('Roll: {:.2f} deg'
                .format(pitch), 0, 35, 1)
    display.text('Pitch: {:.2f} deg'
                .format(roll), 0, 45, 1)
    display.text('Alt: {:.2f} m'
                .format(altitude), 0, 55, 1)
    display.show()
timer.init(period=1000,
    mode=Timer.PERIODIC,
    callback=handleInterrup)

while True:
    try:
        data = mpu.get_value()
        roll = math.atan2(data['AcY'],


                        data['AcZ']) * 180/math.pi;
        altitude = bmp180.altitude
        print("Pitch: {:.2f},"
            "Roll: {:.2f},"
            "Alt: {:.2f}m"
            .format(pitch, roll, altitude))
        sleep(0.05)
    except OSError as e:
        print("Failed reception")

