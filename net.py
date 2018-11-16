import socket
from time import sleep
import traceback
import serial
import argparse
from datetime import *

USB_DEVICE = '/dev/cu.usbmodem3580231'
PACKET_SIZE = 256

parser = argparse.ArgumentParser(description='Connect')
parser.add_argument("ip", help="other device ip")
parser.add_argument("port", help="Port to listen and write on other device")
parser.add_argument("device", help="provide device name from /dev/")
parser.add_argument('-c', dest='caller', action='store_true',
                    help='if true this script is "calling"')


def wait_for_connection(port):
    in_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    in_sock.bind(('0.0.0.0', int(port)))
    in_sock.listen(1)
    return in_sock.accept()[0]


def connect(ip, port):
    while True:
        try:
            out = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            out.connect((ip, int(port)))
            print("Connected")
            return out
        except:
            traceback.print_exc()
            print("Cannot establish connection to", ip, port)
            sleep(1)


if __name__ == "__main__":
    args = parser.parse_args()
    caller = args.caller
    USB_DEVICE = args.device
    ser = serial.Serial(USB_DEVICE)

    if not caller:
        socket = wait_for_connection(args.port)
    else:
        socket = connect(args.ip, args.port)
    socket.setblocking(False)
    buffer = b""
    ser.reset_input_buffer()
    timestamp = datetime.now()
    while True:
        if (datetime.now()-timestamp).seconds > 2:
            buffer = b""
            ser.reset_input_buffer()
            for i in range(100):
                try:
                    socket.recv()
                except:
                    pass
        to_send = ser.read(PACKET_SIZE)
        socket.send(to_send)
        try:
            buffer += socket.recv(PACKET_SIZE)
        except:
            pass
        while len(buffer) >= PACKET_SIZE:
            print(buffer[:PACKET_SIZE])
            ser.write(buffer[:PACKET_SIZE])
            buffer = buffer[PACKET_SIZE:]
