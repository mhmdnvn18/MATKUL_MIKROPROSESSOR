from machine import Pin, ADC, PWM
import time

# Initialize PWM for RGB LEDs
led_R = PWM(Pin(26), freq=1000)
led_G = PWM(Pin(25), freq=1000)
led_B = PWM(Pin(33), freq=1000)

# Initialize ADC for potentiometer (Pin 35) and LDR (Pin 34)
potentiometer = ADC(Pin(35))
ldr = ADC(Pin(34))

# Set full range 3.3V
potentiometer.atten(ADC.ATTN_11DB)
ldr.atten(ADC.ATTN_11DB)

# Main program executed every 100 ms
while True:
    # Read value then divide by the maximum ADC value
    pot_data = potentiometer.read()
    pot_duty = pot_data / 4095

    # Invert ldr data (4095 - data)
    ldr_data = 4095 - ldr.read()
    ldr_duty = ldr_data / 4095

    # Print analog value in percentage
    print("pot: {:.2f}%, ldr: {:.2f}%".format(pot_duty * 100, ldr_duty * 100))

    # Convert to PWM duty cycle (0-1023)
    pot_pwm = int(pot_duty * 1023)
    ldr_pwm = int(ldr_duty * 1023)

    # Set PWM based on potentiometer value
    led_R.duty(pot_pwm)
    led_G.duty(ldr_pwm)
    led_B.duty(ldr_pwm)

    # 100 ms delay
    time.sleep(0.1)
