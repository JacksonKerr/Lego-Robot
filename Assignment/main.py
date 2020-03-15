#!/usr/bin/env python3

"""
    Test Code - Jackson Kerr
"""

import scanner_thread
import robot_moves
import time
from threading import Thread

from ev3dev2.led import Leds
from ev3dev2.sound import Sound
from ev3dev2.button import Button
from ev3dev2.motor import LargeMotor, MoveTank, MoveSteering, OUTPUT_B, OUTPUT_C
from ev3dev2.motor import SpeedDPS, SpeedRPM, SpeedRPS, SpeedDPM, SpeedPercent
from ev3dev2.sensor.lego import ColorSensor, TouchSensor, InfraredSensor, UltrasonicSensor, GyroSensor

print("-------------")
print("  main.py")
print("-------------")

scanThread = Thread(target=scanner_thread.main_loop)  # Create the thread that checks the colour
scanThread.setDaemon(True)  # Make the thread a deamon ( will stop when main program stops )
scanThread.start()

num_black_squares = 0


def continuous_checking():
    global num_black_squares
    # this is what the robot will be doing continuously
    # this runs on a thread
    num_black_squares = 0  # number of black squares travelled
    black = scanner_thread.recently_black()  # True means robot is in a black square
    if black:
        prev_black = True
        num_black_squares += 1
    else:
        prev_black = False
    while True:

        # This is for testing the sonar
        '''
        if object_near():
            stop()
            print("Object found.", file=stderr)
            break
        '''
        if robot_moves.ts.is_pressed:  # If the robot bumps into something
            robot_moves.stop()
            #  print("Contact.", file=stderr)  # file=stderr prints to console instead of robot display
            robot_moves.step_ahead(1, True)
            break
        if scanner_thread.recently_black():
            if not prev_black:  # if in black tile, but was on a white tile
                robot_moves.test_beep()
                print("Entered black square, Left White")
                prev_black = True
                num_black_squares += 1
        else:
            if prev_black:  # And was previously black
                robot_moves.test_beep()
                print("Left black square, Entered White")
                prev_black = False


def turn_in_middle():
    """ Makes the robot creep to the edge of the black tile it is currently on
        then go forwards to the middle of the tile and turn 90 degrees right """
    robot_moves.stop()  # Stop all movement
    while scanner_thread.recently_black():  # Go backwards slowly until you are off the black square
        robot_moves.go_straight(2, True)
    robot_moves.stop()
    '''0.7 rotations is half one black square'''
    drive = MoveTank(OUTPUT_B, OUTPUT_C)  # both motors
    drive.on_for_rotations(5, 5, 0.47)

    robot_moves.spin_right(85, 2)  # Turn 90 degrees to the right (Not Accurate)
    robot_moves.go_straight()


def stage_one():
    global num_black_squares
    robot_moves.go_straight()
    while True:
        if num_black_squares == robot_moves.firstMoves:
            turn_in_middle()
            num_black_squares = 0
            break


def stage_two():
    global num_black_squares
    robot_moves.go_straight()
    while True:
        if num_black_squares == robot_moves.secondMoves:  # turn after completing first moves
            turn_in_middle()
            num_black_squares = 0
            break


def stage_three():
    robot_moves.go_straight()


'''
-----------------------------------------------

            Starting Instructions

-----------------------------------------------
'''

# Start's the checking thread
continuous_checking_thread = Thread(target=continuous_checking)  # Create the thread that checks the colour
continuous_checking_thread.setDaemon(True)  # Make the thread a deamon ( will stop when main program stops )
continuous_checking_thread.start()

# Start's robot's first task
stage_one()
stage_two()
stage_three()
