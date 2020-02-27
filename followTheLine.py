#!/usr/bin/env python3
from ev3dev2.sensor.lego import TouchSensor
from ev3dev2.led import Leds
from ev3dev2.button import Button
from ev3dev2.sound import Sound
from time import sleep
from threading import Thread
from ev3dev2.motor import LargeMotor, OUTPUT_B, OUTPUT_C, MoveTank, SpeedPercent
from ev3dev2.sound import Sound
from time import sleep
from ev3dev2.sensor.lego import ColorSensor

# Variables
drive = MoveTank(OUTPUT_B, OUTPUT_C)
mLeft = LargeMotor(OUTPUT_B)
mRight = LargeMotor(OUTPUT_C)
ts = TouchSensor()
sound = Sound()
onTrack = True



#Move Forward
def goForwards():
    while(onTrack):
        # Run the wheels forwards ( left at 50% of speed , right also at
        # 50% speed , for 3 rotations )
        drive.on_for_rotations(SpeedPercent(30), SpeedPercent(30), 0.5)
        sleep(0.5)
        # Beep and stop for 2 seconds
        sound.beep()

#Create Thread
driveThread = Thread(target = goForwards) # Create a thread that will execute the playtone function
driveThread.setDaemon(True) # Make the thread a deamon ( will stop when main program stops )
driveThread.start()# Run the thread
btn = Button() # will use buttons
leds = Leds()

# Moves the robot back onto the track
def findTrack():
    mLeft = LargeMotor(OUTPUT_B)
    mRight = LargeMotor(OUTPUT_C)
    drive.on_for_rotations(SpeedPercent(30), SpeedPercent(30), -0.2)
    sleep(0.2)
    mLeft.on_for_rotations(SpeedPercent(75), -0.5)
    sleep(0.5)
    sound.tone(300, 200);


searchThread = Thread(target = findTrack) # Create a thread that will execute the playtone function
searchThread.setDaemon(True) # Make the thread a deamon ( will stop when main program stops )


#Checking Color, Interupting thread if not==black
cl = ColorSensor()
while not btn.backspace:
    if (cl.reflected_light_intensity > 42.5 and driveThread.is_alive()):
        onTrack = False
        #searchThread = Thread(target=findTrack)  # Create a thread that will execute the playtone function
        #searchThread.setDaemon(True)  # Make the thread a deamon ( will stop when main program stops )
        #searchThread.start()
        findTrack()
        onTrack = True
        driveThread = Thread(target=goForwards)  # Create a thread that will execute the playtone function
        driveThread.setDaemon(True)  # Make the thread a deamon ( will stop when main program stops )
        driveThread.start()  # Run the thread
        sound.tone(1000 , 200) # 1000 Hz for 0.2 s

sound.beep()
leds.all_off()