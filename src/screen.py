import cv2
import numpy as np

import cfg


thresh = None

if cfg.debug:
    cv2.namedWindow('Unibot Display')


def get_target():
    global thresh
    target = None
    min_distance = float('inf')
    img = cfg.cam.grab(region=(cfg.region_left, int(cfg.region_top - cfg.recoil_offset), cfg.region_right, cfg.region_bottom))
    if img is not None:
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv, cfg.lower_color, cfg.upper_color)
        kernel = np.ones((3,3), np.uint8)
        dilated = cv2.dilate(mask, kernel, iterations=5)
        thresh = cv2.threshold(dilated, 60, 255, cv2.THRESH_BINARY)[1]
        contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

        if len(contours) != 0:
            for contour in contours:
                x, y, w, h = cv2.boundingRect(contour)
                cX = x + w // 2
                cY = y + h // cfg.head_height
                distance = np.sqrt((cX - cfg.center[0])**2 + (cY - cfg.center[1] - cfg.recoil_offset)**2)
                if distance < min_distance:
                    min_distance = distance
                    target = (cX, cY + cfg.recoil_offset)

        if cfg.debug:
            cv2.imshow('Unibot Display', thresh)
            cv2.waitKey(1)
    
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