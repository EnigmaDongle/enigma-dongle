import serial
import socket
# import sys

USB_DEVICE = '/dev/cu.usbmodem3580210'
PACKET_SIZE = 512

HOST, PORT = "localhost", 9999
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

if __name__ == "__main__":
    ser = serial.Serial(USB_DEVICE)
    data = b'n'*PACKET_SIZE
    ser.write(data)
    while True:
        data = ser.read(PACKET_SIZE)
        print(data)
        ser.write(data)
