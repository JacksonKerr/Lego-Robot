#!/usr/bin/env python3

"""
    Test Code - Jackson Kerr
"""

import robot_moves
import time
from threading import Thread

small_tile_distance = 0.8526

def try_again(num_fails, distance):
    if num_fails % 2 == 1:
        right_turn = True
    else:
        right_turn = False
    robot_moves.step_ahead(size=distance, rev=True)
    robot_moves.spin_right(angle=5*num_fails, rev=right_turn)


def go_to_next_tile(distance):
    """ Makes the robot go forwards, until it comes off the black tile it is currently on,
        sees a white tile, and then lands on a black one again """
    robot_moves.go_straight()
    while robot_moves.is_black():
        continue
    while not robot_moves.is_black():
        continue
    robot_moves.stop()
    while robot_moves.is_black():
        robot_moves.step_ahead(size=0.05, rev=False)
    robot_moves.step_ahead(size=distance, rev=False)
    if robot_moves.is_black():  # If the robot successfully made it to the tile
        return True
    return False  # If the robot didn't make it to the tile


def stage_one():
    global small_tile_distance
    attempts = 0
    for i in range(0, 6):
        while not go_to_next_tile(small_tile_distance):
            attempts += 1
            try_again(attempts, small_tile_distance)
        attempts = 0


'''
-----------------------------------------------

            Starting Instructions

-----------------------------------------------
'''

# Start's robot's first task
time.sleep(1)  # Wait's one second before moving to ensure robot is on black square
stage_one()

while True:
    time.sleep(1)
