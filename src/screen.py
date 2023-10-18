import cv2
import numpy as np

import cfg


if cfg.debug:
    window_name = 'Unibot Display'
    window_resolution = (400, 400)
    cv2.namedWindow(window_name)


def get_target():
    target = None
    trigger = False
    closest_contour = None
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

        if cfg.debug:
            if cfg.aim_type == 'pixel':
                # Draw line to closest target
                if target is not None:
                    img = cv2.line(
                        img,
                        cfg.center,
                        target,
                        (255, 255, 255),
                        1
                    )
                # Draw FOV circle
                img = cv2.circle(
                    img,
                    cfg.center,
                    cfg.fov // 2,
                    (0, 255, 0),
                    1
                )
            elif cfg.aim_type == 'shape':
                # Draw rectangle around closest target
                if closest_contour is not None:
                    x, y, w, h = cv2.boundingRect(closest_contour)
                    img = cv2.rectangle(
                        img,
                        (x, y),
                        (x + w, y + h),
                        (0, 255, 0),
                        2
                    )
            
            img = cv2.resize(img, window_resolution)
            cv2.imshow(window_name, img)
            cv2.waitKey(1)

        if cfg.aim_type == 'pixel':
            for y in range(cfg.fov):
                for x in range(cfg.fov):
                    pixel = hsv[y, x]
                    h, s, v = pixel
                    img_rel_x = x - cfg.center[0]
                    img_rel_y = y - cfg.center[1]
                    distance = np.sqrt(img_rel_x**2 + img_rel_y**2)
                    if  distance <= cfg.fov // 2 and \
                        cfg.lower_color[0] <= h and h <= cfg.upper_color[0] and \
                        cfg.lower_color[1] <= s and s <= cfg.upper_color[1] and \
                        cfg.lower_color[2] <= v and v <= cfg.upper_color[2]:
                        if distance < min_distance:
                            min_distance = distance
                            target = (img_rel_x + cfg.center[0], img_rel_y + cfg.center[1])
                            if distance == 0:
                                trigger = True
                                return target, trigger

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
                        closest_contour = contour
                        target = (cX, cY)
            
            value = 8
            if  thresh[cfg.center[0] + value, cfg.center[1]] == 255 and \
                thresh[cfg.center[0] - value, cfg.center[1]] == 255 and \
                thresh[cfg.center[0], cfg.center[1] - value] == 255 and \
                thresh[cfg.center[0], cfg.center[1] + value] == 255:
                trigger = True
    
    return target, trigger