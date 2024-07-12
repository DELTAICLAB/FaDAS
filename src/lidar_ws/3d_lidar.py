import sys
import rplidar2
import numpy as np
import time
import smbus2
import socket
import struct

PORT_NAME = '/dev/ttyUSB0'
POINT_LIFETIME = 500  # Lifetime of points (in seconds)
SCAN_FREQUENCY_HZ = 5.5  # Scanning frequency (Hz)
IP_ADDR = "192.168.1.100"

# Initialize and start RPLIDAR device
lidar = rplidar2.RPLidar(PORT_NAME, baudrate=115200)
start_time = time.time()

# I2C settings
I2C_BUS = 3
DEVICE_ADDRESS = 0x1f
READ_LENGTH = 3  # Read 3 bytes
bus = smbus2.SMBus(I2C_BUS)

# UDP settings
UDP_IP = IP_ADDR  # IP address of the host computer
UDP_PORT = 5005
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

def get_encoder_z():
    try:
        data = bus.read_i2c_block_data(DEVICE_ADDRESS, 0x00, READ_LENGTH)
        if data[0] != 255:
            return 0  # If flag value is not 255
        pulse_count = data[2] + (data[1] << 8)
        z_distance = pulse_count  # 1 pulse = 1 cm
        return z_distance 
    except OSError as e:
        print(f"I2C read error: {e}")
        return 0  # Return 0 as z value in case of error

def is_valid_measurement(distance, min_distance=200, max_distance=3000):
    return min_distance <= distance <= max_distance

lidar.start_motor()
global initial_encoder_value

data = bus.read_i2c_block_data(DEVICE_ADDRESS, 0x00, READ_LENGTH)
initial_encoder_value = data[2] + (data[1] << 8)

try:
    print('Recording measurements... Press Ctrl+C to stop.')

    while True:
        try:
            lidar_measurements = lidar.measure()
            angle = lidar_measurements[2]
            distance = lidar_measurements[3]
            if not is_valid_measurement(distance):
                continue  # Filter out nearby data

            current_time = time.time()
            z_value = get_encoder_z() - initial_encoder_value  # Get z-coordinates from the encoder

            # Print z-axis value
            print(f"Z-axis value: {z_value}")

            # Accumulate collected data
            x = distance * np.cos(np.radians(angle)) / 10.0
            y = distance * np.sin(np.radians(angle)) / 10.0
            
            # Create data packet
            data_packet = struct.pack('fff', x, y, z_value)
            sock.sendto(data_packet, (UDP_IP, UDP_PORT))

        except rplidar2.RPLidarException as e:
            print(f'Lidar error: {e}')
            lidar.reset()

except KeyboardInterrupt:
    print('Stopping.')
finally:
    lidar.stop()
    lidar.disconnect()
    bus.close()
    sock.close()

