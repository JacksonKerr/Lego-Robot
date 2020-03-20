#!/usr/bin/env python3
"""
    new_robot_moves.py

    Contains basic functionality of robot.
    Functions involving basic movement, turning, using sensors
    should go in this file.
"""
from ev3dev2.led import Leds
from ev3dev2.sound import Sound
from ev3dev2.button import Button
from ev3dev2.motor import LargeMotor, MoveTank, MoveSteering, OUTPUT_B, OUTPUT_C
from ev3dev2.motor import SpeedDPS, SpeedRPM, SpeedRPS, SpeedDPM, SpeedPercent
from ev3dev2.sensor.lego import ColorSensor, TouchSensor, InfraredSensor, UltrasonicSensor, GyroSensor

from time import sleep
from threading import Thread
from sys import stderr

mLeft = LargeMotor(OUTPUT_B)                # left motor
mRight = LargeMotor(OUTPUT_C)               # right motor
drive = MoveTank(OUTPUT_B, OUTPUT_C)        # both motors
steer = MoveSteering(OUTPUT_B, OUTPUT_C)    # steering wheel for turning
sound = Sound()
ts = TouchSensor()
cl = ColorSensor()
us = UltrasonicSensor()

defaultSpeed = 10  # 10% of max speed
defaultAngle = 90  # degrees
defaultBlack = 20  # light intensity
defaultDist = 40   # cm


def beep(freq=1000):
    sound.tone(freq, 200)


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


def step_ahead(size, speed=defaultSpeed, rev=False):
    # rev=True will make it move backwards
    if not rev:
        drive.on_for_rotations(speed, speed, size)
    else:
        drive.on_for_rotations(-speed, -speed, size)


def stop():
    # stop all motors
    drive.off()
    steer.off()


def on_black():
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
