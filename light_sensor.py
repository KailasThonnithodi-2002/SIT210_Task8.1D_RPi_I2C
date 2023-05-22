import smbus
import time

# creating bus transporter from raspberry pi to light sensor
bus = smbus.SMBus(1)

# initalising an adddress location for the ligth sensor in the raspberry slave
a_location = 0x23

# writing data using a 7 byte at 0x23 of the bus
bus.write_byte(a_location, 0x7)

def read_light():
	data = bus.read_i2c_block_data(a_location, 0x20) # reads the block of data from the 0x20 register
	light = (data[1] + (256 * data[0])) / 1.2 # equation to recieve data from lux to light
	return light

# categories (threshold for the following)
too_bright = 5000
bright = 1000
medium = 100
dark = 10
no_light = 0

# creating else and if statements based on light read
def categorise(light):
	print(f"Light Intensity: {light}; ", end="")
	if light >= too_bright:
		print("Too Bright!")
	elif (light < too_bright) and (light >= bright):
		print("Bright!")
	elif (light < bright) and (light >= medium):
		print("Medium!")
	elif (light < medium) and (light >= dark):
		print("Dark!")
	else:
		print("Very Dark or No Light!")
		
try:
	while True:
		light = round(read_light(), 2)
		categorise(light)
		time.sleep(0.5)
except KeyboardInterrupt:
	bus.close()
	pass
