from machine import Pin, Timer
from time import sleep

# Define function for generating binary with fixed length
def zfill(s, width):
    return '{:0>{}}'.format(s, width)

# Initialize a list named 'led'
led = [0, 0, 0, 0]

# Arrange MSB to LSB and set the led GPIOs as outputs
led[3] = Pin(26, Pin.OUT)
led[2] = Pin(25, Pin.OUT)
led[1] = Pin(33, Pin.OUT)
led[0] = Pin(32, Pin.OUT)

# Arrange the push/touch button as the input
sw1 = Pin(16, Pin.IN)
sw2 = Pin(17, Pin.IN)

# Initialize variables
decimal = 0

# Initialize timer
tim0 = Timer(0)
tim1 = Timer(1)

# Define function to output the binary values to the LEDs
def write_led(decimal):
    # Convert decimal to binary
    binary = bin(decimal)[2:]
    
    # Fix the length of the binary number to four bits
    four_bit = zfill(binary, 4)
    
    # Print the variables for monitoring in the REPL shell
    print("decimal: {}, four bit: {}".format(decimal, four_bit))
    
    # Set 4 LED outputs based on binary values
    for i in range(4):
        led[i].value(int(four_bit[i]))

# Define event interrupt for Timer 0
def mycallback_0(t):
    global decimal
    
    # Increment the decimal value
    decimal += 1
    
    # Limit the 'decimal' value to a maximum of 15
    if decimal > 15:
        tim0.deinit()
        print("Timer 0 disabled")
    
    write_led(decimal)

# Configure periodic interrupt for Timer 0
tim0.init(mode=Timer.PERIODIC, period=1000, callback=mycallback_0)

# Main loop (if it exists)
while True:
    # Add your main loop code here if needed
    sleep(1)
