# This file is used to pick up the scalpel and hand it off to the user
# The file used the predictions from the search.py file to find the scalpel and hand


# Libraries for Jetson
import time
from Arm_Lib import Arm_Device

# Libraries for mechanics calculation
import math
import numpy as np

# Import the functions from search.py file to find targed object for handoff and pick up
from search import capture_image
from search import detect_object_scalpel
from search import detect_object_hand


# Connect to the arm
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


# Spin and search function for open palm
def spin_search():
    # Spins Jetson until it finds a open palm
    rotation_angle = 0

    # Searches for open palm at reset position
    # Captures image
    pos, image = capture_image()
    # Detects hand: None if no hand, else returns x, y, confidence
    hand = detect_object_hand(pos)

    # If hand is found, return the position of the hand
    # else continue to search for hand
    while hand is None:
        # Rotates left to search open palm
        rotation_angle += 10
        # if rotation_angle > 180:  break (no hand found)
        if rotation_angle > 180:
            break
        # Rotates the arm
        Arm.Arm_serial_servo_write6(rotation_angle, 90, 90, 90, 90, 90, 500)
        time.sleep(1)
        # Captures image
        pos, image = capture_image()
        # Detects hand: None if no hand, else returns x, y, confidence
        hand = detect_object_hand(pos)

    # Returns the position of the hand
    return hand


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
    # Get the position of the hand
    hand = spin_search()

    # Calculate angle to over the links of the arm
    link1, link2, link3 = arm_angles(hand[0], hand[1])
    # Let's print the confidence of the hand detection
    print("Confidence of hand detection", hand[2])

    # Moves arm according to the angles individually
    Arm.Arm_serial_servo_write6(2, link1, 500)
    time.sleep(1)
    Arm.Arm_serial_servo_write6(3, link2, 500)
    time.sleep(1)
    Arm.Arm_serial_servo_write6(4, link3, 500)
    time.sleep(1)

    # Lets go of tool
    Arm.Arm_serial_servo_write6(6, 130, 500)
    time.sleep(1)

    # Resets arm to original position after dropoff
    reset_arm()


# For single run of the program, let's define a main function
def main():
    # Reset arm to original position
    reset_arm()

    # Moves arm to pick up scalpel
    # Get the position of the scalpel
    # Spins Jetson until it finds a scalpel
    rotation_angle = 0

    # Searches for scalpel at reset position
    # Captures image
    pos, image = capture_image()
    # Detects scalpel: None if no scalpel, else returns x, y, confidence
    scalpel = detect_object_scalpel(pos)

    # If scalpel is found, return the position of the scalpel
    # else continue to search for scalpel
    while scalpel is None:
        # Rotates left to search scalpel
        rotation_angle += 10
        # if rotation_angle > 180:  break (no scalpel found)
        if rotation_angle > 180:
            break
        # Rotates the arm
        Arm.Arm_serial_servo_write6(rotation_angle, 90, 90, 90, 90, 90, 500)
        time.sleep(1)
        # Captures image
        pos, image = capture_image()
        # Detects scalpel: None if no scalpel, else returns x, y, confidence
        scalpel = detect_object_scalpel(pos)

    # Calculate angle to over the links of the arm
    link1, link2, link3 = arm_angles(scalpel[0], scalpel[1])
    # Let's print the confidence of the scalpel detection
    print("Confidence of scalpel detection", scalpel[2])

    # Moves arm according to the angles individually
    Arm.Arm_serial_servo_write6(2, link1, 500)
    time.sleep(1)
    Arm.Arm_serial_servo_write6(3, link2, 500)
    time.sleep(1)
    Arm.Arm_serial_servo_write6(4, link3, 500)
    time.sleep(1)

    # Closes the gripper
    Arm.Arm_serial_servo_write6(6, 10, 500)
    time.sleep(1)

    # Resets arm to original position after pickup
    reset_arm()

    # Moves arm to drop off scalpel
    handoff()

# Execute the main function
main()
