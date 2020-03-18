#!/usr/bin/env python3

"""
    Test Code - Jackson Kerr
"""

import scanner_thread
import robot_moves
import time
from threading import Thread

# from ev3dev2.led import Leds
# from ev3dev2.sound import Sound
# from ev3dev2.button import Button
# from ev3dev2.motor import LargeMotor, MoveTank, MoveSteering, OUTPUT_B, OUTPUT_C
# from ev3dev2.motor import SpeedDPS, SpeedRPM, SpeedRPS, SpeedDPM, SpeedPercent
# from ev3dev2.sensor.lego import ColorSensor, TouchSensor, InfraredSensor, UltrasonicSensor, GyroSensor

print("-------------")
print("  main.py")
print("-------------")

scanThread = Thread(target=scanner_thread.main_loop)  # Create the thread that checks the colour
scanThread.setDaemon(True)  # Make the thread a deamon ( will stop when main program stops )
scanThread.start()

num_black_squares = 0


def continuous_checking():
    global num_black_squares
    found = False
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
        if True:
            '''
                THIS CODE WAS CAUSING PROBLEMS FOR OTHER PARTS OF THE PROGRAM
            if robot_moves.object_near() and (not found):
                robot_moves.stop()
                found = True
            elif robot_moves.ts.is_pressed:  # If the robot bumps into something
                robot_moves.stop()
                time.sleep(2)
                robot_moves.go_straight(speed=100)
                time.sleep(5)
                break
                #  print("Contact.", file=stderr)  # file=stderr prints to console instead of robot display
                # robot_moves.step_ahead(size=1, speed=5, rev=True)
                break
            '''
        else:
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


def creep_off_black_tile():
    robot_moves.stop()
    while scanner_thread.recently_black():  # Go backwards slowly until you are off the black square
        robot_moves.go_straight(speed=2, rev=True)
    robot_moves.stop()
    robot_moves.step_ahead(size=0.075, rev=False)


def turn_in_middle(rev=False):
    """ Makes the robot creep to the edge of the black tile it is currently on
        then go forwards to the middle of the tile and turn 90 degrees right """
    robot_moves.stop()  # Stop all movement
    creep_off_black_tile()
    '''0.7 rotations is half one black square'''
    # drive = MoveTank(OUTPUT_B, OUTPUT_C)  # both motors
    # drive.on_for_rotations(5, 5, 0.47)
    robot_moves.step_ahead(size=0.47, speed=5)

    robot_moves.spin_right(angle=90, speed=4, rev=rev)  # Turn 90 degrees to the right (Not Accurate)
    # robot_moves.go_straight()


def straighten():
    robot_moves.stop()
    total_turns = 0
    num_right_turns = 0
    while robot_moves.is_black():  # Turn right until you see white
        time.sleep(0.3)
        robot_moves.spin_right(angle=5, rev=False)
        num_right_turns += 1
        total_turns += 1
    while num_right_turns > 0:  # Turn back to original position (to the left)
        time.sleep(0.3)
        robot_moves.spin_right(angle=5, rev=True)
        num_right_turns -= 1
    while robot_moves.is_black():  # Turn left until you see white
        time.sleep(0.3)
        robot_moves.spin_right(angle=5, rev=True)
        num_right_turns += 1
        total_turns += 1
    i = total_turns
    while i > total_turns / 2:
        time.sleep(0.3)
        robot_moves.spin_right(angle=5, rev=False)  # Turn to straightened position
        i -= 1

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
    squares_straightened = 0
    creep_off_black_tile()
    straighten()
    #robot_moves.go_straight()
    '''
    while True:
        # r = 2.16
        # c = 13.57
        # d = 9.5
        # 0.7 steps min = 9.5 cm
        # 0.95 halfway into square
        if squares_straightened < num_black_squares:
            robot_moves.stop()
            creep_off_black_tile()
            straighten()
            robot_moves.go_straight()
            squares_straightened += 1
        if num_black_squares == robot_moves.secondMoves:  # turn after completing first moves
            turn_in_middle()
            num_black_squares = 0
            break
    '''

def stage_three():
    global num_black_squares
    robot_moves.go_straight()
    while True:
        if num_black_squares == robot_moves.thirdMoves:  # turn after completing first moves
            turn_in_middle(True)
            num_black_squares = 0
            break


def stage_four():
    global num_black_squares
    robot_moves.go_straight()
    while True:
        if num_black_squares == robot_moves.fourthMoves:  # turn after completing first moves
            num_black_squares = 0
            robot_moves.stop()
            robot_moves.spin_right(angle=360, speed=10)
            break


def stage_five():
    robot_moves.go_straight()
    robot_moves.stop()


'''
-----------------------------------------------

            Starting Instructions

-----------------------------------------------
'''

# Start's the checking thread
'''
continuous_checking_thread = Thread(target=continuous_checking)  # Create the thread that checks the colour
continuous_checking_thread.setDaemon(True)  # Make the thread a deamon ( will stop when main program stops )
continuous_checking_thread.start()
'''

# Start's robot's first task
time.sleep(1)  # Wait's one second before moving to ensure robot is on black square
# stage_one()
stage_two()
# stage_three()
# stage_four()
# stage_five()


while True:
    time.sleep(1)
