from movement import Movement
from obstacle import UltrasonicSensor
import threading
import time
import math
import socket

_move = Movement()
_sensor = UltrasonicSensor()

stop_signal = False
stop_program = False
cur_status = '0'


def distance_monitor():
    global stop_signal, stop_program
    while True:
        if stop_program:
            break

        if _sensor.get_distance() < 15:
            stop_signal = True
        else:
            stop_signal = False
        time.sleep(0.01)



def ticker():
    if cur_status == 'R':
        _move.turn_right()
    if cur_status == 'L':
        _move.turn_left()
    if cur_status == 'A':
        _move.move_forward()
    if cur_status == 'B':
        _move.move_backward()
    if cur_status == 'E':
        _move.stop()
        
try:
    thread = threading.Thread(target=distance_monitor)
    thread.start()
    UDP_IP = "192.168.137.187"
    UDP_PORT = 8888
    sock = socket.socket(socket.AF_INET,  socket.SOCK_DGRAM)
    sock.bind((UDP_IP, UDP_PORT))
    
    while True:
        print(cur_status)

        sock.settimeout(0.1)
        try:
            data, addr = sock.recvfrom(1024)  
        except socket.timeout:
            ticker()
            continue
        if data == b'R':
            cur_status = 'R'

        if data == b'L':
            cur_status = 'L'

        if data == b'A':
            cur_status = 'A'

        if data == b'B':
            cur_status = 'B'

        if data == b'E':
            cur_status = 'E'

        if data == b'T':
            cur_status = 'T'

        if data == b'O':
            cur_status = 'O'

except KeyboardInterrupt:
    print("Error!!!!")

finally:
    stop_program = True
    thread.join()
    _move.cleanup()
    print("cleaned")

