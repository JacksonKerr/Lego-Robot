#!/usr/bin/env python3

"""
    main.py - Group 15
"""

import robot_moves
import time
from threading import Thread

small_tile_distance = 0.8526
large_tile_distance = 1.9894
sample_distance = 0.05
num_samples = 3
tile_count = 0


def center():
    """ Centers the robot on a black tile (on a single slice of the tile, in the direction it is facing). """
    num_moves = 0
    while robot_moves.on_black():  # go forwards until the edge of the tile is reached
        robot_moves.step_ahead(size=0.05, rev=False)
        num_moves += 1
    i = num_moves
    while i > num_moves * 0.8:
        robot_moves.step_ahead(size=0.05, rev=True)  # Move to center of tile
        i -= 1


def go_to_next_tile(distance):
    """ Makes the robot go forwards, off the current black tile and then a given number of wheel rotations forwards.
        Returns true is the robot is on a black tile after moving, else returns false"""
    robot_moves.go_straight()
    while robot_moves.on_black(): # Keep going until off the black tile
        continue
    robot_moves.stop()
    robot_moves.step_ahead(size=distance, rev=False) # Attempt to go to the next tile
    for i in range(0, num_samples-1): # Check if on a black tile, taking a number of samples
        robot_moves.step_ahead(size=sample_distance, rev=False)
        if not robot_moves.on_black():
            robot_moves.step_ahead(size=sample_distance * i, rev=True)
            return False
    tile_count += 1
    robot_moves.beep()
    return True


def try_again(num_fails, distance):
    """ Makes the robot retrace its steps (for distance) backwards to the last tile it was on,
        and turn slightly. The distance and direction will depend on the size of num_fails"""
    right_turn = False   
    if num_fails % 2 == 1:
        right_turn = True
    robot_moves.step_ahead(size=distance+(num_samples*sample_distance), rev=True)
    robot_moves.spin_right(angle=5 * num_fails, rev=right_turn)


def go_to_first_tile():
    """ Moves the robot from the starting position onto the first tile, and centers it  """
    robot_moves.go_straight()
    while robot_moves.on_black():
        continue
    while not robot_moves.on_black():
        continue
    robot_moves.beep()
    tile_count += 1
    center()


def move_tiles(tiles_to_travel, tile_distance):
    """ Moves the robot a number of tiles given by tiles_to_travel, across gaps between 
        tiles of wheel rotations tile_distence"""
    global large_tile_distance
    attempts = 0
    for i in range(0, tiles_to_travel-1):
        while not go_to_next_tile(tile_distance):
            attempts += 1
            try_again(attempts, large_tile_distance)
        attempts = 0
    center()

def push_off():
    """This is used for pushing the milk bottle off the tile"""
    robot_moves.go_straight()
    while not robot_moves.object_touching():  # Keep moving until touch sensor pressed.
        continue
    robot_moves.test_beep()
    robot_moves.step_ahead(size=0.5) # Go forwards half a wheel rotation, pushing the bottle


def push_bottle():
    """ Slowly turns the robot in a circle, once the bottle is seen the robot will center on it
        before driving towards it"""
    i = 0
    while not robot_moves.object_near(100):  # Spin in small angle increments the bottle is seen.
        robot_moves.spin_right(angle=4, rev=True)
    while robot_moves.object_near(100):  # Spin until the bottle is no longer seen, counting movements
        robot_moves.spin_right(angle=4, rev=True)
        i += 1
    for x in range(0, i//2): # Do half of the movements done while the bottle was seen to center on it
        robot_moves.spin_right(angle=4)
    push_off()

''' Robot's instructions: '''
go_to_first_tile()
robot_moves.spin_right()
move_tiles(7, small_tile_distance)
robot_moves.spin_right()
move_tiles(7, large_tile_distance)
robot_moves.spin_right(rev=True)
move_tiles(7, small_tile_distance)
robot_moves.spin_right()
robot_moves.step_ahead(large_tile_distance/2)
push_bottle()
