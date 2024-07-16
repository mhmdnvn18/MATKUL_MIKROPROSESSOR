from machine import Pin, ADC, PWM
import time

# Initialize ADC for potentiometer and LDR
potentiometer = ADC(Pin(35))
ldr = ADC(Pin(34))

# Set full range to 3.3V
potentiometer.atten(ADC.ATTN_11DB)
ldr.atten(ADC.ATTN_11DB)

# Main program loop
while True:
    # Read values and convert to duty cycle
    pot_data = potentiometer.read()
    pot_duty = pot_data / 4095.0

    # Invert LDR data
    ldr_data = 4095 - ldr.read()
    ldr_duty = ldr_data / 4095.0

    # Print analog value in percentage
    print("pot: {:.2f}v, ldr: {:.2f}v".format(pot_duty * 3.3, ldr_duty * 3.3))

    # 100 ms delay
    time.sleep_ms(100)
