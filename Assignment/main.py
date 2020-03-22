#!/usr/bin/env python3

"""
    Test Code - Jackson Kerr
"""

import alternate_robot_moves
import time
from threading import Thread

small_tile_distance = 0.8526
large_tile_distance = 1.9894
sample_distance = 0.05
num_samples = 3


def center():
    """ Centers the robot on a black tile (on a single slice of the tile, in the direction it is facing). """
    num_moves = 0
    while alternate_robot_moves.on_black():  # go forwards until the edge of the tile is reached
        alternate_robot_moves.step_ahead(size=0.05, rev=False)
        num_moves += 1
    i = num_moves
    while i > num_moves * 0.8:
        alternate_robot_moves.step_ahead(size=0.05, rev=True)  # Move to center of tile
        i -= 1


def go_to_next_tile(distance):
    """ Makes the robot go forwards, off the current black tile and then a given number of wheel rotations forwards.
        Returns true is the robot is on a black tile after moving, else returns false"""
    alternate_robot_moves.go_straight()
    while alternate_robot_moves.on_black():
        continue
    alternate_robot_moves.stop()
    alternate_robot_moves.step_ahead(size=distance, rev=False)
    for i in range(0, num_samples-1):
        alternate_robot_moves.step_ahead(size=sample_distance, rev=False)
        if not alternate_robot_moves.on_black():
            alternate_robot_moves.step_ahead(size=sample_distance * i, rev=True)
            return False
    return True


def try_again(num_fails, distance):
    if num_fails % 2 == 1:
        right_turn = True
    else:
        right_turn = False
    alternate_robot_moves.step_ahead(size=distance+(num_samples*sample_distance), rev=True)
    alternate_robot_moves.spin_right(angle=5 * num_fails, rev=right_turn)


def go_to_first_tile():
    alternate_robot_moves.go_straight()
    while alternate_robot_moves.on_black():
        continue
    while not alternate_robot_moves.on_black():
        continue
    center()


def move_small_tiles(tiles_to_travel):
    global small_tile_distance
    attempts = 0
    for i in range(0, tiles_to_travel-1):
        while not go_to_next_tile(small_tile_distance):
            attempts += 1
            try_again(attempts, small_tile_distance)
        attempts = 0


def move_large_tiles(tiles_to_travel):
    global large_tile_distance
    attempts = 0
    for i in range(0, tiles_to_travel-1):
        while not go_to_next_tile(large_tile_distance):
            attempts += 1
            try_again(attempts, large_tile_distance)
        attempts = 0
    center()


'''

    SONAR -------------------------------

'''


def push_off():
    """This is used for pushing the milk bottle off the tile"""
    alternate_robot_moves.go_straight()
    while not alternate_robot_moves.object_touching():  # Keep moving until touch sensor pressed.
        continue
    alternate_robot_moves.test_beep()


def front_of_black():
    """Move to front of black tile, used in stage 5."""
    while alternate_robot_moves.on_black():
        alternate_robot_moves.go_straight()
    alternate_robot_moves.stop()


def push_bottle():
    """Possible technique for stage 5, use a complete turn instead of multiple smaller checks. """
    front_of_black()
    i = 0
    while not alternate_robot_moves.object_near(50):  # Spin in small angle increments until doing a 360.
        alternate_robot_moves.spin_right(angle=4, rev=True)  # Could be smaller?
    while alternate_robot_moves.object_near():  # Spin in small angle increments until doing a 360.
        alternate_robot_moves.spin_right(angle=4, rev=True)  # Could be smaller?
        i += 1
    for x in range(0, i//2):
        alternate_robot_moves.spin_right(angle=4)
    push_off()


'''
-----------------------------------------------

            Starting Instructions

-----------------------------------------------
'''
#go_to_first_tile()
#alternate_robot_moves.spin_right()
#move_small_tiles(7)
#alternate_robot_moves.spin_right()
#move_large_tiles(7)
#alternate_robot_moves.spin_right(rev=True)
#move_small_tiles(7)
#alternate_robot_moves.spin_right()
#alternate_robot_moves.step_ahead(large_tile_distance/2)
push_bottle()