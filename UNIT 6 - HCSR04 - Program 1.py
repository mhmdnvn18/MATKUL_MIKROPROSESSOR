from machine import Pin
from time import sleep
import dht
import ds18x20
import onewire

# Initialize DHT sensor
sensor = dht.DHT22(Pin(26))

# Initialize DS18x20 sensor
pin_ds = Pin(25)
ds_sensor = ds18x20.DS18X20(onewire.OneWire(pin_ds))

# Check if DS18x20 sensor exists
roms = ds_sensor.scan()
print('Found DS devices: ', roms)

# Main program
while True:
    # Execute below code, then if there is a mistake, jump to the exception
    try:
        # Recovers measurements from DHT22
        sensor.measure()

        # Convert temperature from DS18B20
        ds_sensor.convert_temp()

        # The DHT22 and DS18X20 return at most 1 measurement every 2s
        sleep(2)

        # Read temperature and humidity value from DHT22
        print("Temperature: {:.1f} °C, Humidity: {:.1f} %".format(sensor.temperature(), sensor.humidity()))

        # Read temperature value from DS18x20
        for rom in roms:
            temp_ds = ds_sensor.read_temp(rom)
            print("Temperature: {:.1f} °C".format(temp_ds))

    except OSError as e:
        print("Failed reception")
