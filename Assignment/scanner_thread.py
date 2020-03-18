#!/usr/bin/env python3
"""
    scanner_thread.py

    Used to check if the ground beneath the robot has been black for awhile.
    Main use is to stop the robot thinking it is on a black tile if it runs over a small bump
    or dark spot on the floor
"""
import robot_moves
import time

default_max = 15
blackness = default_max  # Start tile is black
checkDelay = 0.005  # The time between scanner checks in seconds


def recently_black():
    return blackness >= default_max/2


def main_loop():
    global blackness
    while True:
        if robot_moves.is_black() and blackness < default_max:
            blackness += 1
        elif (not robot_moves.is_black()) and blackness > 0:
            blackness -= 1
        time.sleep(checkDelay)

