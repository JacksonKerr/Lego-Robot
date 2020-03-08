#!/usr/bin/env python3
"""
    scan_thread.py

    Used to check if the ground beneath the robot has been black for awhile.
    Main use is to stop the robot thinking it is on a black tile if it runs over a small bump
    or dark spot on the floor
"""
import robot_moves
import time

blackness = 100  # Start tile is black
checkDelay = 0.01  # The time between scanner checks in seconds


def recently_black():
    return blackness > 50


def main_loop():
    while True:
        if robot_moves.is_black() and blackness < 100:
            blackness += 1
        elif blackness > 0:
            blackness -= 1
        time.sleep(checkDelay)