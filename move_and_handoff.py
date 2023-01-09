# Libraries for Jetson
import time
from Arm_Lib import Arm_Device

# Libraries for mechanics calculation
import math
import numpy as np

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


# Calculates angles using inverse kinematics based on given coordinates function
def arm_angles(x_coordinate, y_coordinate):
    # Define the location/coordinates of the end effector
    x = x_coordinate
    y = y_coordinate

    # Define the lengths of the three links of the Nano arm (lengths are constant)
    LINK1 = 2.0
    LINK2 = 2.5
    LINK3 = 2.5

    # Calculate the angle of the first joint using the inverse kinematics 
    radian1 = np.arctan2(y, x)

    # Calculate the distance from the first joint to the end effector
    distance = np.sqrt(x**2 + y**2)

    # Calculate the angle of the second joint using the inverse kinematics 
    radian2 = np.arccos((distance**2 - LINK2**2 - LINK3**2) / (2*LINK2*LINK3))

    # Calculate the angle of the third joint using the inverse kinematics 
    radian3 = np.arccos((LINK2**2 - LINK3**2 - distance**2) / (2*LINK2*distance))

    # Convert randian angles into degrees
    degree1 = radian1 * 180 / np.pi
    degree2 = radian2 * 180 / np.pi
    degree3 = radian3 * 180 / np.pi

    # Print the angles in degrees
    print("Angle 1: ", degree1)
    print("Angle 2: ", degree2)
    print("Angle 3: ", degree3)

    # Returns angles of the three links needed to reach XY coordinate as tuple
    return degree1, degree2, degree3


# Moves arm function based on angles calculated


def handoff():
    # Get x and y coordinate of center of palm (center of screen)
    # x = getX()
    # y = getY()

    # Test:
    x = 3.0
    y = 4.0

    # Calculate angle to over the links of the arm
    link1, link2, link3 = arm_angles(x, y)

    # Moves arm according to the angles individually
    Arm.Arm_serial_servo_write(2, link1, 500)
    time.sleep(1)
    Arm.Arm_serial_servo_write(3, link2, 500)
    time.sleep(1)
    Arm.Arm_serial_servo_write(4, link3, 500)
    time.sleep(1)

    # Lets go of tool
    Arm.Arm_serial_servo_write(6, 130, 500)
    time.sleep(1)

    # Resets arm to original position after dropoff
    reset_arm()


# Main run
def main():
    reset_arm()
    spin_search()
    handoff()


main()
