#!/usr/bin/env python3

"""
    Test Code - Jackson Kerr
"""

import robot_moves
import time
from threading import Thread

small_tile_distance = 0.8526
large_tile_distance = 1.9894


def center():
    """ Centers the robot on a black tile (on a single slice of the tile, in the direction it is facing). """
    num_moves = 0
    while robot_moves.on_black():  # go forwards until the edge of the tile is reached
        robot_moves.step_ahead(size=0.05, rev=False)
        num_moves += 1
    i = num_moves
    robot_moves.test_beep()
    while i > num_moves * 0.8:
        robot_moves.step_ahead(size=0.05, rev=True)  # Move to center of tile
        i -= 1


def try_again(num_fails, distance):
    if num_fails % 2 == 1:
        right_turn = True
    else:
        right_turn = False
    robot_moves.step_ahead(size=distance, rev=True)
    robot_moves.spin_right(angle=5 * num_fails, rev=right_turn)


def go_to_next_tile(distance):
    """ Makes the robot go forwards, off the current black tile and then a given number of wheel rotations forwards.
        Returns true is the robot is on a black tile after moving, else returns false"""
    robot_moves.go_straight()
    while robot_moves.on_black():
        continue
    robot_moves.stop()
    robot_moves.step_ahead(size=distance, rev=False)
    for i in range(0, 2):
        robot_moves.step_ahead(size=0.05, rev=False)
        if not robot_moves.on_black():
            robot_moves.step_ahead(size=0.05 * i, rev=True)
            return False
    return True


def stage_zero():
    robot_moves.go_straight()
    while robot_moves.on_black():
        continue
    while not robot_moves.on_black():
        continue
    center()
    robot_moves.spin_right()


def stage_one():
    global small_tile_distance
    attempts = 0
    for i in range(0, 6):
        while not go_to_next_tile(small_tile_distance):
            attempts += 1
            try_again(attempts, small_tile_distance)
        attempts = 0


def stage_two():
    robot_moves.spin_right()
    global large_tile_distance
    attempts = 0
    for i in range(0, 6):
        while not go_to_next_tile(large_tile_distance):
            attempts += 1
            try_again(attempts, large_tile_distance)
        attempts = 0
    center()
    robot_moves.spin_right()


'''
-----------------------------------------------

            Starting Instructions

-----------------------------------------------
'''
stage_zero()
stage_one()
stage_two()
