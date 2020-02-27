#!/ usr/ bin / env python3
from ev3dev2 . motor import LargeMotor , OUTPUT_B , OUTPUT_C , SpeedPercent
from ev3dev2 . sound import Sound
from time import sleep
mLeft = LargeMotor ( OUTPUT_B )
mRight = LargeMotor ( OUTPUT_C )
sound = Sound ()
# Run the left wheel forwards ( rotate 5 times at 75% of its max speed )
mLeft . on_for_rotations ( SpeedPercent (75) , 5)
# Beep and stop for 2 seconds
sound . beep ()
sleep (2)
# Run the right wheel backwards ( rotate 5 times at 75% of its max speed )
mRight . on_for_rotations ( SpeedPercent (75) , -5)
# Beep at program end
sound . beep ()

#!/ usr/ bin / env python3
from ev3dev2 . motor import LargeMotor , OUTPUT_B , OUTPUT_C , MoveTank , SpeedPercent
from ev3dev2 . sound import Sound
from time import sleep
drive = MoveTank ( OUTPUT_B , OUTPUT_C )
sound = Sound ()
# Run the wheels forwards ( left at 50% of speed , right also at
# 50% speed , for 3 rotations )
drive . on_for_rotations ( SpeedPercent (50) , SpeedPercent (50) , 3)
# Beep and stop for 2 seconds
sound . beep ()
sleep (2)
# Run the wheels backwards ( left at 50% of speed , right at
# 30% speed , for 3 rotations )
drive . on_for_rotations ( SpeedPercent (50) , SpeedPercent (30) , -3)
# Beep at program end
sound . beep ()

#!/ usr/ bin / env python3
from ev3dev2 . led import Leds
from ev3dev2 . button import Button
from ev3dev2 . sensor . lego import TouchSensor
from ev3dev2 . sound import Sound
from time import sleep
# Function that flashes LEDS and makes a beep sound to let the user know the robot is ready
def ready ( leds , sound ):
leds . all_off ()
sleep (0.2)
# Function that flashes LEDS and makes a
for i in range (2):
leds . set_color (’LEFT ’, ’AMBER ’)
leds . set_color (’RIGHT ’, ’AMBER ’)
sleep (0.2)
leds . all_off ()
sleep (0.2)
# Play a sound that the robot is ready
sound . beep ()
leds = Leds () # will use leds
btn = Button () # will use buttons
ts = TouchSensor () # will use touch sensor
sound = Sound () # will use sound
# Let the user know bot is ready and wait for Enter to be pressed
ready ( leds , sound )
while not btn . enter :
sleep (0.2)
# Keep running the program
# until backspace button is pressed
while not btn . backspace :
if ts . value () == 1: # touch sensor pressed
leds . set_color (’LEFT ’, ’RED ’)
else :
leds . set_color (’LEFT ’, ’GREEN ’)
sleep (0.01)
# Turn off leds

#!/ usr/ bin / env python3
from ev3dev2 . sensor . lego import TouchSensor
from ev3dev2 . led import Leds
from ev3dev2 . button import Button
from ev3dev2 . sound import Sound
from time import sleep
from threading import Thread
# Will use touch sensor
ts = TouchSensor ()
sound = Sound ()
# Function that plays a tone
def playtone ():
for j in range (0 , 20): # Do twenty times .
sound . tone (1000 , 200) # 1000 Hz for 0.2 s
sleep (0.5)
t = Thread ( target = playtone ) # Create a thread that will execute the playtone function
t. setDaemon ( True ) # Make the thread a deamon ( will stop when main program stops )
t. start () # Run the thread
btn = Button () # will use buttons
leds = Leds ()
while not btn . backspace :
if ts . value () == 0: # while button is not pressed
leds . set_color (’LEFT ’, ’RED ’)
sleep (0.1) # do nothing other than wait
elif ts . value () == 1: # while button is pressed
leds . set_color (’LEFT ’, ’GREEN ’)
sleep (0.1) # do nothing other than wait
sound . beep ()
leds . all_off ()