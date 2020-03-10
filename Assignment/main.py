"""
    Test Code - Jackson Kerr
"""

import robot_moves
import scanner_thread
import time
from threading import Thread

scanThread = Thread(target=scanner_thread.mainloop)  # Create the thread that checks the colour
scanThread.setDaemon(True)  # Make the thread a deamon ( will stop when main program stops )
scanThread.start()


# Checking Color, Interrupting thread if not==black
while True:
    #  if not scanThread.is_alive():
    robot_moves.test_beep()
    time.sleep(1)