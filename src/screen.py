import cv2
import numpy as np

import cfg


thresh = None


def get_target():
    global thresh
    target = None
    min_distance = float('inf')
    img = cfg.cam.grab(region=cfg.region)
    if img is not None:
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv, cfg.lower_color, cfg.upper_color)
        kernel = np.ones((3,3), np.uint8)
        dilated = cv2.dilate(mask, kernel, iterations=5)
        thresh = cv2.threshold(dilated, 60, 255, cv2.THRESH_BINARY)[1]
        contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

        if len(contours) != 0:
            for contour in contours:
                M = cv2.moments(contour)
                cX = int(M["m10"] / M["m00"])
                cY = int(M["m01"] / M["m00"])
                distance = np.sqrt((cX - cfg.center[0])**2 + (cY - cfg.center[1])**2)

                if distance < min_distance:
                    min_distance = distance
                    target = (cX, cY)
    return target

def get_center():
    global thresh

    target = False
    if thresh is None:
        return target

    value = 8
    if thresh[cfg.center[0] + value, cfg.center[1]] == 255:
        if thresh[cfg.center[0] - value, cfg.center[1]] == 255:
            if thresh[cfg.center[0], cfg.center[1] - value] == 255:
                if thresh[cfg.center[0], cfg.center[1] + value] == 255:
                    target = True
    thresh = None
    return target