#!/usr/bin/env python3
"""
    scan_thread.py

    Used to check if the ground beneath the robot has been black for awhile.
    Main use is to stop the robot thinking it is on a black tile if it runs over a small bump
    or dark spot on the floor
"""
import robot_moves
import time

blackness = 50  # Start tile is black
checkDelay = 0.001  # The time between scanner checks in seconds


def recently_black():
    return blackness > 25


def main_loop():
    global blackness
    while True:
        if robot_moves.is_black() and blackness < 50:
            blackness += 1
        elif (not robot_moves.is_black()) and blackness > 0:
            blackness -= 1
        time.sleep(checkDelay)

