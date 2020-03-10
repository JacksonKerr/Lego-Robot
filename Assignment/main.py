#!/usr/bin/env python3

"""
    Test Code - Jackson Kerr
"""

import scanner_thread
import robot_moves
import time
from threading import Thread

print("-------------")
print("  main.py")
print("-------------")

scanThread = Thread(target=scanner_thread.main_loop)  # Create the thread that checks the colour
scanThread.setDaemon(True)  # Make the thread a deamon ( will stop when main program stops )
scanThread.start()

def look():
    # this is what the robot will be doing continuously
    # this runs on a thread
    num_black_squares = 0  # number of black squares travelled
    black = scanner_thread.recently_black()  # True means robot is in a black square
    if scanner_thread.recently_black():
        prev_black = scanner_thread.recently_black()
        num_black_squares += 1
    else:
        num_black_black = False
    while True:

        # This is for testing the sonar
        '''
        if object_near():
            stop()
            print("Object found.", file=stderr)
            break
        '''
        if robot_moves.ts.is_pressed:  # touched something
            robot_moves.stop()
            #  print("Contact.", file=stderr)  # file=stderr prints to console instead of robot display
            robot_moves.step_ahead(1, True)
            break
        if not scanner_thread.recently_black():
            if prev_black:
                # if not in black area but was previously in black area
                # then we left a black square
                robot_moves.test_beep()
                print("Left black square.")
                prev_black = False
        else:
            if not prev_black:
                # if in black area but was previously in non-black area
                # then we entered a black square
                robot_moves.test_beep()
                print("Entered black square.")
                prev_black = True
                num_black_squares += 1
                if num_black_squares == robot_moves.firstMoves:
                    # turn after completing first moves
                    robot_moves.stop()
                    robot_moves.spin_right(90)
                    robot_moves.go_straight()
                if num_black_squares == robot_moves.firstMoves + robot_moves.secondMoves:
                    robot_moves.stop()
                    break

lookThread = Thread(target=look)  # Create the thread that checks the colour
lookThread.setDaemon(True)  # Make the thread a deamon ( will stop when main program stops )
lookThread.start()

robot_moves.go_straight()

while True:
    print(scanner_thread.recently_black())
    time.sleep(0.1)
