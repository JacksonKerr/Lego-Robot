#!/usr/bin/env python3

from ev3dev2.led import Leds
from ev3dev2.sound import Sound
from ev3dev2.button import Button
from ev3dev2.motor import LargeMotor, MoveTank, MoveSteering, OUTPUT_B, OUTPUT_C
from ev3dev2.motor import SpeedDPS, SpeedRPM, SpeedRPS, SpeedDPM, SpeedPercent
from ev3dev2.sensor.lego import ColorSensor, TouchSensor, InfraredSensor, UltrasonicSensor, GyroSensor

from time import sleep
from threading import Thread
from sys import stderr

mLeft = LargeMotor(OUTPUT_B)  # left motor
mRight = LargeMotor(OUTPUT_C)  # right motor
drive = MoveTank(OUTPUT_B, OUTPUT_C)  # both motors
steer = MoveSteering(OUTPUT_B, OUTPUT_C)  # steering wheel for turning
sound = Sound()
ts = TouchSensor()
cl = ColorSensor()
# gs = GyroSensor()		# gyrosensor is not there
us = UltrasonicSensor()

defaultSpeed = 15  # 25% of max speed
defaultAngle = 85  # degrees
defaultStep = 1
defaultBlack = 20  # light intensity
defaultDist = 10  # cm


firstMoves = 2  # initial moves
secondMoves = 6  # happens after initial moves and turning
thirdMoves = 6  # third part of test


# rev=True does the reverse of the function

def test_beep():
    sound.tone(1000, 200)  # 1000 Hz for 0.2 s

def go_straight(speed=defaultSpeed, rev=False):
    # rev=True will make it go backwards
    if not rev:
        drive.on(left_speed=speed, right_speed=speed)  # forever
    else:
        drive.on(left_speed=-1 * speed, right_speed=-1 * speed)


def spin_right(angle=defaultAngle, speed=defaultSpeed, rev=False):
    # rev=True will make it turn left
    if not rev:
        steer.on_for_degrees(100, speed, 2 * angle)
    else:
        steer.on_for_degrees(-100, speed, 2 * angle)


def step_ahead(size=defaultStep, speed=25, rev=False):
    # rev=True will make it move backwards
    if not rev:
        drive.on_for_rotations(speed, speed, 0.5 * size)
    else:
        drive.on_for_rotations(speed, speed, -0.5 * size)

def stop():
    # stop all motors
    drive.off()
    steer.off()


def is_black():
    # uses color sensor to detect intensity of reflected light
    if cl.reflected_light_intensity < defaultBlack:
        return True
    else:
        return False


def object_near(distance=defaultDist):
    # uses sonar to detect if an object is close
    if us.distance_centimeters < distance:
        return True
    else:
        return False



# Use this while calibrating
# print("Intensity: ", cl.reflected_light_intensity)

'''
# movement tests

# forward for 3 seconds
sleep(1)
go_straight()
sleep(3)
stop()

# backward for 3 seconds
sleep (1)
go_straight(True)
sleep(3)
stop()

# take a step forward and back
sleep (1)
step_ahead(1)
sleep(2)
step_ahead(1, True)

# spin right by 90 degrees and left by 180
sleep (1)
spin_right(90)
sleep(2)
spin_right(180, True)

vision = Thread(target=look)
vision.setDaemon(True)
vision.start()

sound.beep()

# start moving and the thread controls the rest
# technically we do not need a thread
# we can put everything in the main thread for simplicity
go_straight()

vision.join()  # wait for thread to exit before terminating main thread
'''