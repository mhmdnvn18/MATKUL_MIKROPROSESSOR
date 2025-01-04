from machine import Pin, I2C, Timer
from time import sleep
import ssd1306
import mpu6050
import math
from bmp180 import BMP180

# Inisialisasi I2C, display, MPU6050, dan BMP180
timer = Timer(0)
i2c = I2C(sda=Pin(21), scl=Pin(22))
display = ssd1306.SSD1306_I2C(128, 64, i2c)
mpu = mpu6050.accel(i2c)
bmp180 = BMP180(i2c)
bmp180.oversample_sett = 2
bmp180.baseline = 101325

# Inisialisasi variabel global untuk altitude, pitch, dan roll
altitude, pitch, roll = 0, 0, 0

# Pengaturan awal display
display.fill(0)
display.fill_rect(0, 0, 32, 32, 1)
display.fill_rect(2, 2, 28, 28, 0)
display.vline(9, 8, 22, 1)
display.vline(16, 2, 22, 1)
display.vline(23, 8, 22, 1)
display.fill_rect(26, 24, 2, 4, 1)
display.text('Micropython', 40, 0, 1)
display.text('Project', 40, 12, 1)
display.text('EE - UMY', 40, 24, 1)
display.show()

# Definisikan interrupt handler untuk memperbarui display
def handleInterrup(timer):
    global altitude, pitch, roll
    display.fill_rect(0, 35, 128, 64, 0)
    display.text('Roll: {:.2f} deg'.format(roll), 0, 35, 1)
    display.text('Pitch: {:.2f} deg'.format(pitch), 0, 45, 1)
    display.text('Alt: {:.2f} m'.format(altitude), 0, 55, 1)
    display.show()

# Inisialisasi timer untuk memanggil interrupt handler secara periodik
timer.init(period=1000, mode=Timer.PERIODIC, callback=handleInterrup)

# Loop utama untuk membaca data sensor dan menghitung pitch, roll, dan altitude
while True:
    try:
        data = mpu.get_values()
        
        # Tambahkan print statement untuk debugging
        print("MPU6050 raw data:", data)
        
        AcX, AcY, AcZ = data['AcX'], data['AcY'], data['AcZ']
        
        # Menghitung roll
        roll = math.atan2(AcY, AcZ) * 180 / math.pi
        
        # Menghitung pitch
        vector_yz = math.sqrt(AcY * AcY + AcZ * AcZ)
        if vector_yz != 0:  # Pastikan tidak membagi dengan nol
            pitch = math.atan2(AcX, vector_yz) * 180 / math.pi
        else:
            pitch = 0.0
        
        # Menghitung altitude
        altitude = bmp180.altitude
        
        # Mencetak nilai pitch, roll, dan altitude
        print("Pitch: {:.2f}, Roll: {:.2f}, Alt: {:.2f}m".format(pitch, roll, altitude))
        sleep(1)
    
    except OSError as e:
        print("Failed reception")
    
    except ValueError as e:
        print("Math domain error:", e)
