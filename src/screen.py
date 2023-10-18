import cv2
import numpy as np

import cfg


if cfg.debug:
    cv2.namedWindow('Unibot Display')


def get_target():
    target = None
    trigger = False
    min_distance = float('inf')
    img = cfg.cam.grab(region=(
        cfg.region_left, 
        int(cfg.region_top - cfg.recoil_offset), 
        cfg.region_left + cfg.fov, 
        int(cfg.region_top - cfg.recoil_offset + cfg.fov)
        ))
    if img is not None:
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv, cfg.lower_color, cfg.upper_color)

        if cfg.aim_type == 'pixel':
            size = cfg.fov
            center = (size // 2, size // 2)
            for y in range(size):
                for x in range(size):
                    pixel = hsv[y, x]
                    h, s, v = pixel
                    if (cfg.lower_color[0] <= h and h <= cfg.upper_color[0]
                    and cfg.lower_color[1] <= s and s <= cfg.upper_color[1]
                    and cfg.lower_color[2] <= v and v <= cfg.upper_color[2]):
                        img_rel_x = x - center[0]
                        img_rel_y = y - center[1]
                        distance = np.sqrt(img_rel_x**2 + img_rel_y**2)
                        if distance < min_distance:
                            min_distance = distance
                            target = (img_rel_x + cfg.center[0], img_rel_y + cfg.center[1] + cfg.recoil_offset)
            if min_distance == 0:
                trigger = True

        elif cfg.aim_type == 'shape':
            kernel = np.ones((3,3), np.uint8)
            dilated = cv2.dilate(mask, kernel, iterations=5)
            thresh = cv2.threshold(dilated, 60, 255, cv2.THRESH_BINARY)[1]
            contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

            if len(contours) != 0:
                for contour in contours:
                    x, y, w, h = cv2.boundingRect(contour)
                    cX = x + w // 2
                    cY = y + h // cfg.head_height
                    distance = np.sqrt((cX - cfg.center[0])**2 + (cY - cfg.center[1])**2)
                    if distance < min_distance:
                        min_distance = distance
                        target = (cX, cY + cfg.recoil_offset)
            
            value = 8
            if thresh[cfg.center[0] + value, cfg.center[1]] == 255:
                if thresh[cfg.center[0] - value, cfg.center[1]] == 255:
                    if thresh[cfg.center[0], cfg.center[1] - value] == 255:
                        if thresh[cfg.center[0], cfg.center[1] + value] == 255:
                            trigger = True

        if cfg.debug:
            if cfg.aim_type == 'pixel':
                cv2.imshow('Unibot Display', mask)
                cv2.waitKey(1)
            elif cfg.aim_type == 'shape':
                cv2.imshow('Unibot Display', thresh)
                cv2.waitKey(1)
    
    return target, trigger