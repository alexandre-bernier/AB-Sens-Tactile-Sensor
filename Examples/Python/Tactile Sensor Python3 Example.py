# Tactile Sensor Python3 Example
# Author: Alexandre Bernier
# Copyright: BSD-3-Clause License

import serial

# Messages header
first_byte = 0x9A
not_used = 0x00

# List of commands
cmd_read_sensors = 0x61
cmd_autosend_sensors = 0x58

# To identify the Tactile Sensor device path, run 'sudo dmesg' after connecting it to your PC.
# Make sure to adjust the device permissions with 'sudo chmod 777 [device_path]' or by adding them in your udev rules.
dev_path = '/dev/ttyACM0'


# Connecting to the sensors
dev = serial.Serial(dev_path, baudrate=115200, timeout=0.5, write_timeout=0.5)
print("Connected to " + dev.name)


# There are two ways to receive messages from the sensors
# 1- Ask for a single message at a time (command = cmd_read_sensors)
# 2- Ask for a continuous stream of messages (command = cmd_autosend_sensors)

# Method 1 (cmd_read_sensors)
msg = [first_byte, not_used, cmd_read_sensors, 0x00]
msg_bytearray = bytearray(msg)
print("Sending READ_SENSORS")

try:
    dev.write(msg_bytearray)
except serial.SerialTimeoutException:
    print("Write timeout, try reconnecting the sensor to your PC")

try:
    while True:
        byte = dev.read(1)
        print(byte)
except serial.SerialTimeoutException:
    print("Read timeout")
    pass

print("Done reading")


# Disconnecting from the sensors
dev.close()
print("Device disconnected")
