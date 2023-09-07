# Tactile Sensor Python3 Example
# Author: Alexandre Bernier
# Copyright: BSD-3-Clause License


###########
# Imports #
###########
import serial
import time


################
# Declarations #
################
# Messages header
first_byte = 0x9A
not_used = 0x00
zero = 0x00
period_length = 0x01
period = 0x01

# List of commands
cmd_read_sensors = 0x61
cmd_autosend_sensors = 0x58

# Messages
msg_cmd_read_sensors = bytearray([first_byte, not_used, cmd_read_sensors, zero])
msg_cmd_start_autosend_sensors = bytearray([first_byte, not_used, cmd_autosend_sensors, period_length, period])
msg_cmd_stop_autosend_sensors = bytearray([first_byte, not_used, cmd_autosend_sensors, period_length, zero])

# To identify the Tactile Sensor device path, run 'sudo dmesg' after connecting it to your PC.
# Make sure to adjust the device permissions with 'sudo chmod 777 [device_path]' or by adding them in your udev rules.
dev_path = '/dev/ttyACM0'


#############################
# Connection to the sensors #
#############################
dev = serial.Serial(dev_path, baudrate=115200)
print("Connected to " + dev.name)

print("Input bytes waiting:", dev.in_waiting)
##################
# Receiving data #
##################
# There are two ways to receive data from the sensors
# 1- Ask for a single message at a time (command = cmd_read_sensors)
# 2- Ask for a continuous stream of messages (command = cmd_autosend_sensors)

###################################
# Method 2 (cmd_autosend_sensors) #
###################################
# Building the message: cmd_autosend_sensors (0x58)
msg = msg_cmd_start_autosend_sensors
print("Sending START_AUTOSEND_SENSORS: ", "".join('0x{:02x} '.format(x) for x in msg))

# Sending the message
try:
    dev.write(msg)
except serial.SerialTimeoutException:
    print("Write timeout, try reconnecting the sensor to your PC")

# Reading the responses
data = None
while True:
    try:
        # First byte (read until we find it)
        resp_first_byte = None
        correct_first_byte = False
        while correct_first_byte is False:
            resp_first_byte = dev.read(1)

            if resp_first_byte != first_byte.to_bytes(1, "big"):
                print("Byte read =", resp_first_byte)
                print("Doesn't match the expected first byte:", first_byte.to_bytes(1, "big"))
            else:
                correct_first_byte = True
        print("First byte =", resp_first_byte.hex())

        # Not used
        resp_non_used_byte = dev.read(1)

        # Command
        resp_cmd = dev.read(1)
        print("Command =", resp_cmd.hex())

        # Data length
        resp_data_length = dev.read(1)
        print("Data length =", int.from_bytes(resp_data_length, "big"), "bytes")

        # Sensor type
        resp_sensor_type = dev.read(1)
        print("Sensor type=", resp_sensor_type.hex())

        # Data
        resp_data = dev.read(int.from_bytes(resp_data_length, "big")-1)
        print("Data bytes =", resp_data.hex())

        print("\n")

        # Parsing the message
        if resp_sensor_type == 0x10:
            finger_0 = resp_data
        elif resp_sensor_type == 0x14:
            finger_1 = resp_data
        elif resp_sensor_type == 0x20:
            rest = resp_data

    except KeyboardInterrupt:
        break

print("Done reading")


###################################
# Stop auto sending sensor values #
###################################
msg = msg_cmd_stop_autosend_sensors
print("Sending STOP_AUTOSEND_SENSORS: ", "".join('0x{:02x} '.format(x) for x in msg))

# Sending the message
try:
    dev.write(msg)
except serial.SerialTimeoutException:
    print("Write timeout, try reconnecting the sensor to your PC")


##################################
# Disconnection from the sensors #
##################################
dev.close()
print("Device disconnected")
