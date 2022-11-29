# Libraries for Jetson
import time
from Arm_Lib import Arm_Device

# Libraries for mechanics calculation
import math

# Import the find palm function from search.py file to find open palm
# import search
from search import findPalm

# Define the arm
Arm = Arm_Device()
time.sleep(1)

'''reset, spin and research, and mechanics'''

# Reset function
# Resets arm into reset position
def reset_arm():
    Arm.Arm_serial_servo_write6(0, 90, 90, 90, 90, 90, 500)
    time.sleep(1)
    # need to test reset position angle so camera can see


# Spin and search function
def spin_search():
    # Spins Jetson until it finds a open palm
    rotation_angle = 0

    # Searches for open palm at reset position
    findPalm()  # returns true/false?

    while not findPalm():
        # Rotates left to search open palm
        rotation_angle += 1
        # Rotates arm back to inital position and searches for arm again
        if rotation_angle > 180:
            rotation_angle = 0
        # Rotates the arm
        Arm.Arm_serial_servo_write6(rotation_angle, 90, 90, 90, 90, 90, 500)
        time.sleep(1)
        # Sees if it finds the open palm
        findPalm()


# Mechanics function
def handoff():
    # empty function
    print()


reset_arm()
spin_search()
handoff()
