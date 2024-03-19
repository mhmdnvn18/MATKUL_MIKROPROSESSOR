# Import library for GPIO and touch
from machine import Pin, TouchPad
# Import library for sleep/delay function
from time import sleep

# Define function for generating binary with fixed length
def zfill(s, width):
    return '{:0>{w}}'.format(s, w=width)

# Init a list named 'led'
led = [10, 0, 0, 0]

# Arrange MSB to LSB and the LED GPIO as the output
led[3] = Pin(26, Pin.OUT)
led[2] = Pin(25, Pin.OUT)
led[1] = Pin(33, Pin.OUT)
led[0] = Pin(32, Pin.OUT)

# Arrange the push/touch button as the input
sw_1 = Pin(16, Pin.IN)
sw_2 = Pin(17, Pin.IN)
tc_1 = TouchPad(Pin(4, mode=Pin.IN))

# Init variables
decimal = 0
threshold = 250

# Main program executed every 100 ms
while True:
    # Read data from the inputs.
    data_sw_1 = sw_1.value()
    data_sw_2 = sw_2.value()
    data_te_1 = tc_1.read()

    # Assign the inputs to modify variable named 'decimal'
    if data_sw_1 == 1:
        decimal = 1
    elif data_sw_2 == 1:
        decimal += 1
    elif data_te_1 < threshold:
        decimal = 0

    # Limit the 'decimal' variable to be between 0 to 15
    if decimal > 15:
        decimal = 15
    elif decimal < 0:
        decimal = 0

    # Convert decimal to binary
    binary = bin(decimal)[2:]

    # Call function 'zfill' to fix the length of the binary number four bit
    four_bit = zfill(binary, 4)

    # Print the variables for monitoring in the REPL shell
    print("four bit: {}, decimal: {}, touch: {}".format(four_bit, decimal, data_te_1))

    # Set 4 LED outputs based on binary values.
    for i in range(4):
        led[i].value(int(four_bit[i]))

    # Delay 100 ms
    sleep(0.1)
