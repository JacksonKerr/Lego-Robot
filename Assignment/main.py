#!/usr/bin/env python3

"""
    Test Code - Jackson Kerr
"""

import robot_moves
import time
from threading import Thread

left_error = 0

fine_movement_speed = 5


'''
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


def creep_off_black_tile():
    """ Stops the robot, and causes it to go backwards untll it is off the edge of the tile, then moves it
        forwards slightly so it is only just inside of the tile"""
    robot_moves.stop()
    while robot_moves.is_black():  # Go backwards slowly until you are off the black square
        robot_moves.go_straight(speed=fine_movement_speed, rev=True)
    robot_moves.stop()
    robot_moves.step_ahead(size=0.045, speed=fine_movement_speed, rev=False)  # Old step = 0.075


def center():
    """ Centers the robot on a black tile (on a single slice of the tile, in the direction it is facing). """
    num_moves = 0
    while robot_moves.is_black():  # go forwards until the edge of the tile is reached
        robot_moves.step_ahead(size=0.01, speed=fine_movement_speed, rev=False)
        num_moves += 1
    i = num_moves
    robot_moves.test_beep()
    while i > num_moves * 0.8:
        robot_moves.step_ahead(size=0.01, speed=fine_movement_speed, rev=True)  # Move to center of tile
        i -= 1


def turn_in_middle(rev=False):
    """ Makes the robot creep to the edge of the black tile it is currently on
        then go forwards to the middle of the tile and turn 90 degrees right """
    robot_moves.stop()  # Stop all movement
    creep_off_black_tile()
    robot_moves.test_beep()
    center()
    robot_moves.test_beep()
    robot_moves.spin_right(angle=90, speed=fine_movement_speed, rev=rev)  # Turn 90 degrees to the right (Not Accurate)
    creep_off_black_tile()
    straighten()


def go_to_next_tile():
    """ Makes the robot go forwards, until it comes off the black tile it is currently on,
        sees a white tile, and then lands on a black one again """
    robot_moves.go_straight()
    while robot_moves.is_black():
        continue
    while not robot_moves.is_black():
        continue
    robot_moves.stop()
    robot_moves.step_ahead(size=0.15, rev=False)


def straighten():
    """NEEDS COMMENTING"""
    global left_error
    robot_moves.stop()
    total_turns = 0
    num_right_turns = 0
    while robot_moves.is_black():  # Turn right until you see white
        robot_moves.spin_right(angle=1, speed=fine_movement_speed, rev=False)
        num_right_turns += 1
        total_turns += 1
    while num_right_turns > 0:  # Turn back to original position (to the left)
        robot_moves.spin_right(angle=1, speed=fine_movement_speed, rev=True)
        num_right_turns -= 1
    while robot_moves.is_black():  # Turn left until you see white
        robot_moves.spin_right(angle=1, speed=fine_movement_speed, rev=True)
        num_right_turns += 1
        total_turns += 1
    i = total_turns
    while i > total_turns / 2:
        robot_moves.spin_right(angle=1, speed=fine_movement_speed, rev=False)  # Turn to straightened position
        i -= 1
    if i % 2 == 1:
        if left_error == 1:
            robot_moves.spin_right(angle=1, speed=fine_movement_speed, rev=True)
            left_error = 0
        else:
            left_error = 1


def stage_one():
    go_to_next_tile()
    turn_in_middle()


def stage_two():
    global num_black_squares
    go_to_next_tile()
    num_black_squares = 2
    while True:
        robot_moves.stop()
        creep_off_black_tile()
        straighten()
        go_to_next_tile()
        num_black_squares += 1
        if num_black_squares == robot_moves.secondMoves:  # turn after completing first moves
            turn_in_middle()
            num_black_squares = 0
            break


def stage_three():
    num_black_squares = 2
    go_to_next_tile()
    while True:
        creep_off_black_tile()
        straighten()
        go_to_next_tile()
        num_black_squares += 1
        if num_black_squares == robot_moves.thirdMoves:  # turn after completing first moves
            turn_in_middle(True)
            break


def stage_five():
    robot_moves.go_straight()
    robot_moves.stop()


'''
-----------------------------------------------

            Starting Instructions

-----------------------------------------------
'''

# Start's robot's first task
time.sleep(1)  # Wait's one second before moving to ensure robot is on black square
stage_one()
stage_two()
stage_three()
stage_two()
# stage_five()


while True:
    time.sleep(1)
