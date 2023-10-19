import cv2
import numpy as np

import cfg


if cfg.debug:
    window_name = 'Unibot Display'
    window_resolution = (1280, 720)
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

        if cfg.aim_type == 'pixel':
            for y in range(cfg.fov):
                for x in range(cfg.fov):
                    pixel = hsv[y, x]
                    h, s, v = pixel
                    img_rel_x = x - cfg.center[0]
                    img_rel_y = y - cfg.center[1]
                    distance = np.sqrt(img_rel_x**2 + img_rel_y**2)
                    if  distance <= cfg.fov // 2 and \
                        cfg.lower_color[0] <= h <= cfg.upper_color[0] and \
                        cfg.lower_color[1] <= s <= cfg.upper_color[1] and \
                        cfg.lower_color[2] <= v <= cfg.upper_color[2]:
                        if distance < min_distance:
                            min_distance = distance
                            target = (img_rel_x + cfg.center[0], img_rel_y + cfg.center[1])
                            if distance == 0:
                                trigger = True
                                break
                if min_distance == 0:
                    break

        elif cfg.aim_type == 'shape':
            kernel = np.ones((3,3), np.uint8)
            dilated = cv2.dilate(mask, kernel, iterations=5)
            thresh = cv2.threshold(dilated, 60, 255, cv2.THRESH_BINARY)[1]
            contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

            if len(contours) != 0:
                for contour in contours:
                    x, y, w, h = cv2.boundingRect(contour)
                    cX = x + w // 2
                    cY = int(y + h * cfg.head_height)
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

        if cfg.debug:
            if cfg.display_mode == 'game':
                debug_img = img
            elif cfg.display_mode == 'mask':
                if cfg.aim_type == 'pixel':
                    debug_img = mask
                    debug_img = cv2.cvtColor(debug_img, cv2.COLOR_GRAY2BGR)
                elif cfg.aim_type == 'shape':
                    debug_img = thresh
                    debug_img = cv2.cvtColor(debug_img, cv2.COLOR_GRAY2BGR)

            full_img = cfg.cam.grab(region=(
                0, 
                0, 
                cfg.resolution[0], 
                cfg.resolution[1]
            ))
            if full_img is not None:
                # Draw line to closest target
                if target is not None:
                    debug_img = cv2.line(
                        debug_img,
                        cfg.center,
                        target,
                        (0, 255, 0),
                        2
                    )

                if cfg.aim_type == 'pixel':
                    # Draw FOV circle
                    debug_img = cv2.circle(
                        debug_img,
                        cfg.center,
                        cfg.fov // 2,
                        (0, 255, 0),
                        1
                    )
                elif cfg.aim_type == 'shape':
                    # Draw rectangle around closest target
                    if closest_contour is not None:
                        x, y, w, h = cv2.boundingRect(closest_contour)
                        debug_img = cv2.rectangle(
                            debug_img,
                            (x, y),
                            (x + w, y + h),
                            (0, 0, 255),
                            2
                        )
                    # Draw FOV
                    debug_img = cv2.rectangle(
                        debug_img,
                        (0, 0),
                        (cfg.fov, cfg.fov),
                        (0, 255, 0),
                        2
                    )
                
                offset_x = (cfg.resolution[0] - cfg.fov) // 2
                offset_y = (cfg.resolution[1] - cfg.fov) // 2
                full_img[offset_y:offset_y+debug_img.shape[1], offset_x:offset_x+debug_img.shape[0]] = debug_img
                full_img = cv2.resize(full_img, window_resolution)
                cv2.imshow(window_name, full_img)
                cv2.waitKey(1)
    
    return target, trigger