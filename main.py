import tkinter as tk
from movement import Movement
from obstacle import UltrasonicSensor
import threading
import time

_movement = Movement()
sensor = UltrasonicSensor()
running = True

def key_input(event):
    global running
    
    print("Key pressed: ", event.char)

    key_press = event.char
    if key_press.lower() == 'w':
        _movement.move_forward()

    elif key_press.lower() == 's':
        _movement.move_backward()

    elif key_press.lower() == 'a':
        _movement.turn_left()

    elif key_press.lower() == 'd':
        _movement.turn_right()
    
    elif key_press.lower() == 'x':
        running = False
    else:
        pass


def key_release(event):
    print("Key released: ", event.char)
    _movement.stop()


def control_robot():
    command = tk.Tk()
    command.bind('<KeyPress>', key_input)
    command.bind('<KeyRelease>', key_release)
    command.mainloop()


def avoid_obstacle():
    global running
    while True:
        distance = sensor.get_distance()
        print(f"Distance: {distance:.2f} cm")

        if distance < 20:
            print("Obstacle detected! Stopping the robot.")
            _movement.stop()
            
            _movement.turn_right(0.4)
            
            _movement.stop()

        time.sleep(0.5)
        if running == False:
            break


try:
    print("Robocar start")

    control_thread = threading.Thread(target=control_robot, daemon=True)
    control_thread.start()
    
    obstacle_thread = threading.Thread(target=avoid_obstacle, daemon=True)
    obstacle_thread.start()
    

    while True:
        time.sleep(0.2)

except KeyboardInterrupt:
    print("Error!!!!")

finally:
    _movement.cleanup()
    # sensor.cleanup()
    print("cleaned")


