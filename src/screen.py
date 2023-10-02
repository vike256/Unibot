import numpy as np
import cv2

def screengrab(sct, screenshot, lower_color, upper_color):
    img = np.array(sct.grab(screenshot))
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, lower_color, upper_color)
    kernel = np.ones((3,3), np.uint8)
    dilated = cv2.dilate(mask, kernel, iterations=5)
    thresh = cv2.threshold(dilated, 60, 255, cv2.THRESH_BINARY)[1]
    contours, hierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    return contours, thresh


def get_closest_target(contours, center):
    closest_contour = None
    min_distance = float('inf')

    for contour in contours: # Get center of the closest contour
        mouse = cv2.moments(contour)
        cX = int(mouse["m10"] / mouse["m00"])
        cY = int(mouse["m01"] / mouse["m00"])
        distance = np.sqrt((cX - center[0])**2 + (cY - center[1])**2)

        if distance < min_distance:
            min_distance = distance
            closest_contour = (cX, cY)
    return closest_contour