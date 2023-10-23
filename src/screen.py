import cv2
import numpy as np
import dxcam
from pyautogui import size


class Screen:
    def __init__(self, config):
        self.cam = dxcam.create(output_color="BGR")
        self.offset = config.offset
        self.screen = size()
        self.screen_center = (self.screen.width // 2, self.screen.height // 2)
        self.screen_region = (
            0,
            0,
            self.screen.width,
            self.screen.height
        )
        self.fov = config.fov
        self.fov_center = (self.fov // 2, self.fov // 2)
        self.fov_region = (
            self.screen_center[0] - self.fov // 2,
            self.screen_center[1] - self.fov // 2 - self.offset,
            self.screen_center[0] + self.fov // 2,
            self.screen_center[1] + self.fov // 2 - self.offset
        )
        self.detection_type = config.detection_type
        self.upper_color = config.upper_color
        self.lower_color = config.lower_color
        self.fps = config.fps
        self.head_height = config.head_height
        self.debug = config.debug
        self.mask = None
        self.thresh = None
        self.target = None
        self.closest_contour = None
        self.img = None

        # Setup debug display
        if self.debug:
            self.display_mode = config.display_mode
            self.window_name = 'Unibot Display'
            self.window_resolution = (
                self.screen.width // 2, 
                self.screen.height // 2
            )
            cv2.namedWindow(self.window_name)

    def __del__(self):
        del self.cam

    def screenshot(self, region):
        while True:
            image = self.cam.grab(region=region)
            if image is not None:
                return np.array(image)

    def get_target(self):
        self.target = None
        trigger = False
        self.closest_contour = None
        
        self.img = self.screenshot(self.fov_region)
        hsv = cv2.cvtColor(self.img, cv2.COLOR_BGR2HSV)
        self.mask = cv2.inRange(hsv, self.lower_color, self.upper_color)

        if self.detection_type == 'pixel':
            lit_pixels = np.where(self.mask == 255)
            if len(lit_pixels[0]) > 0:
                min_distance = float('inf')

                for x, y in zip(lit_pixels[1], lit_pixels[0]):
                    distance = np.sqrt((x - self.fov_center[0])**2 + (y - self.fov_center[1])**2)
                    
                    if distance < min_distance:
                        min_distance = distance
                        self.target = (x, y)
                        if min_distance == 0:
                            trigger = True
                            break

        elif self.detection_type == 'shape':
            kernel = np.ones((3, 3), np.uint8)
            dilated = cv2.dilate(self.mask, kernel, iterations=5)
            self.thresh = cv2.threshold(dilated, 60, 255, cv2.THRESH_BINARY)[1]
            contours, _ = cv2.findContours(self.thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

            if len(contours) != 0:
                min_distance = float('inf')
                for contour in contours:
                    x, y, w, h = cv2.boundingRect(contour)
                    center_x = x + w // 2
                    center_y = int(y + h * (1 - self.head_height))
                    distance = np.sqrt((center_x - self.fov_center[0])**2 + (center_y - self.fov_center[1])**2)
                    if distance < min_distance:
                        min_distance = distance
                        self.closest_contour = contour
                        self.target = (center_x, center_y)
            
            if self.closest_contour is not None and cv2.pointPolygonTest(self.closest_contour, (self.fov_center[0], self.fov_center[1]), False) >= 0:
                trigger = True

        if self.debug:
            self.debug_display()
 
        return self.target, trigger

    def debug_display(self):
        if self.display_mode == 'game':
            debug_img = self.img
        else:
            if self.detection_type == 'pixel':
                debug_img = self.mask
                debug_img = cv2.cvtColor(debug_img, cv2.COLOR_GRAY2BGR)
            else:
                debug_img = self.thresh
                debug_img = cv2.cvtColor(debug_img, cv2.COLOR_GRAY2BGR)

        full_img = self.screenshot(self.screen_region)

        # Draw line to the closest target
        if self.target is not None:
            debug_img = cv2.line(
                debug_img,
                self.fov_center,
                self.target,
                (0, 255, 0),
                2
            )

        if self.detection_type == 'pixel':
            # Draw FOV circle
            debug_img = cv2.circle(
                debug_img,
                self.fov_center,
                self.fov // 2,
                (0, 255, 0),
                1
            )
        elif self.detection_type == 'shape':
            # Draw rectangle around closest target
            if self.closest_contour is not None:
                x, y, w, h = cv2.boundingRect(self.closest_contour)
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
                (self.fov, self.fov),
                (0, 255, 0),
                2
            )
        
        offset_x = (self.screen.width - self.fov) // 2
        offset_y = (self.screen.height - self.fov) // 2 - self.offset
        full_img[offset_y:offset_y+debug_img.shape[1], offset_x:offset_x+debug_img.shape[0]] = debug_img
        # Draw a rectangle crosshair
        full_img = cv2.rectangle( 
            full_img, 
            (self.screen_center[0] - 5, self.screen_center[1] - 5),
            (self.screen_center[0] + 5, self.screen_center[1] + 5),
            (255, 255, 255),
            1
        ) 
        full_img = cv2.resize(full_img, self.window_resolution)
        cv2.imshow(self.window_name, full_img)
        cv2.waitKey(1)
