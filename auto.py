from movement import Movement
from obstacle import UltrasonicSensor
import threading
import time
import math

_move = Movement()
_sensor = UltrasonicSensor()

stop_signal = False
stop_program = False


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


def get_angle(theta_pre=0, start=(0, 0), end=(0, 0)):
    x1, y1 = start
    x2, y2 = end

    theta_goal = math.atan2(y2 - y1, x2 - x1)
    delta_theta = theta_goal - theta_pre
    delta_theta = math.atan2(math.sin(delta_theta), math.cos(delta_theta))
    angle = round(math.degrees(delta_theta), 1)

    return angle, theta_goal


def get_current_point(start, theta, speed, duration):
    x0, y0 = start
    distance_traveled = speed * duration
    x = x0 + distance_traveled * math.cos(theta)
    y = y0 + distance_traveled * math.sin(theta)

    return round(x, 3), round(y, 3)


def move_to_point(theta_pre=0, start=(0, 0), end=(0, 0)):
    global stop_signal
    x1, y1 = start
    x2, y2 = end
    speed = 66.7
    angle, theta_goal = get_angle(theta_pre, start, end)
    time.sleep(0.1)
    if angle <= 0:
        _move.turn_right_by_angle(-angle)
        print("turn right ", angle)
    else:
        _move.turn_left_by_angle(angle)
        print("turn left ", -angle)

    distance = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
    duration = distance / speed
    time.sleep(0.1)
    start_time = time.time()
    _move.move_forward()
    while time.time() - start_time < duration:
        if stop_signal:
            _move.stop()
            time.sleep(0.5)
            time_current = time.time()
            time_total = time_current - start_time - 0.5
            print("thoi gian diem dau: ", time_total)
            point1 = get_current_point(start, theta_goal, speed, time_total)

            print("tim thay vat can")
            print("diem dau: ", point1)

            _move.turn_right_by_angle(90)
            print("xoay phai 90 do")
            time_current = time.time()
            _move.move_forward(0.4)
            print("tien ve phia truoc")
            _move.stop()
            time.sleep(0.1)
            time_total = time.time() - time_current
            point2 = get_current_point(point1, theta_goal - math.pi / 2, speed, time_total)

            print("toa do hien tai ", point2)
            print("thoi gian diem dau: ", time_total)
            
            _move.turn_left_by_angle(90)
            
            time_current = time.time()
            _move.move_forward(0.4)
            print("tien ve phia truoc")
            _move.stop()
            
            time_total = time.time() - time_current
            point3 = get_current_point(point2, theta_goal, speed, time_total)
            print("Toa do 3: ", point3)
            return move_to_point(theta_goal, point3, end)

        time.sleep(0.01)

    _move.stop()
    time.sleep(0.5)
    print("Goal point with angle: ", round(math.degrees(theta_goal), 1))
    return theta_goal


try:
    thread = threading.Thread(target=distance_monitor)
    thread.start()

    theta_pre = math.radians(90)
    time.sleep(2)
    # points = [(0, 0), (50, 50), (-50, 50), (-50, 100), (0, 100), (0, 0)]
    points = [(0, 0), (0, 60), (40, 60), (40,0)]
    for i in range(1, len(points)):
       theta_pre = move_to_point(theta_pre, points[i - 1], points[i])
    
    print("Goal")

except KeyboardInterrupt:
    print("Error!!!!")

finally:
    stop_program = True
    thread.join()
    _move.cleanup()
    print("cleaned")


