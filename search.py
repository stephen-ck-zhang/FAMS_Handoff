# This file is used to capture real-time images
# and detect the objects in the images with its bounding boxes


# Create a function to capture images from the camera
def capture_image():
    # Import the camera libraries
    import cv2

    # Create a VideoCapture object
    cap = cv2.VideoCapture(0)

    # Check if the webcam is opened correctly
    if not cap.isOpened():
        raise IOError("Cannot open webcam")

    # Capture the frame
    ret, frame = cap.read()

    # Release the VideoCapture object
    cap.release()

    # save the image as a jpg file
    cv2.imwrite('image.jpg', frame)

    # Display the captured image
    cv2.imshow('Input', frame)

    # Return position where the image is saved and the image itself
    return 'image.jpg', frame


# Create a function to detect scalpels in the image
def detect_object_scalpel(image):
    # Download the pre-trained model for detecting scalpels
    from roboflow import Roboflow
    rf = Roboflow(api_key="btax39hMf4xR6kY6A1Nf")
    project = rf.workspace().project("scalpels")
    model = project.version(3).model

    # Detect the objects in the image
    res = model.predict(image, confidence=40, overlap=30).json() # confidence might need to be tuned

    # Get the first prediction in which the class is 'scalpel'
    scalpel_prediction = None
    for prediction in res['predictions']:
        if prediction['class'] == 'Scalpels':
            scalpel_prediction = prediction
            break

    # Let's remove the captured image to prevent cluttering (duplicate images)
    import os
    os.remove(image)

    # If there is no scalpel prediction, return None
    if scalpel_prediction is None:
        return None
    # else, return the prediction coordinates and probability
    else:
        return [scalpel_prediction['x'], scalpel_prediction['y'], scalpel_prediction['confidence']]


# Create a function to detect hands in the image
def detect_object_hand(image):
    # Download the pre-trained model for detecting hands
    from roboflow import Roboflow
    rf = Roboflow(api_key="btax39hMf4xR6kY6A1Nf")
    project = rf.workspace().project("handd-ua3mt")
    model = project.version(1).model

    # Detect the objects in the image
    res = model.predict(image, confidence=30, overlap=30).json() # confidence might need to be tuned

    # Get the first prediction in which the class is 'hand'
    hand_prediction = None
    for prediction in res['predictions']:
        if prediction['class'] == 'palm':
            hand_prediction = prediction
            break

    # Let's remove the captured image to prevent cluttering (duplicate images)
    import os
    os.remove(image)

    # If there is no hand prediction, return None
    if hand_prediction is None:
        return None
    # else, return the prediction coordinates and probability
    else:
        return [hand_prediction['x'], hand_prediction['y'], hand_prediction['confidence']]
