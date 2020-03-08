"""
    Test Code - Jackson Kerr
"""

import robot_moves
import scanner_thread
from threading import Thread

scanThread = Thread(target=scanner_thread)  # Create the thread that checks the colour
scanThread.setDaemon(True)  # Make the thread a deamon ( will stop when main program stops )
scanThread.start()


# Checking Color, Interupting thread if not==black
cl = ColorSensor()
while not btn.backspace:
    #  if not scanThread.is_alive():
    sound.tone(1000, 200)  # 1000 Hz for 0.2 s