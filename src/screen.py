"""
    Unibot, an open-source colorbot.
    Copyright (C) 2025 vike256

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""
import cv2
import numpy as np
import bettercam
from pyautogui import size


class Screen:
    def __init__(self, config):
        self.cfg = config
        self.cam = bettercam.create(output_color="BGR")

        if self.cfg.auto_detect_resolution:
            screen_size = size()
            self.screen = (screen_size.width, screen_size.height)
        else:
            self.screen = (self.cfg.resolution_x, self.cfg.resolution_y)

        self.screen_center = (self.screen[0] // 2, self.screen[1] // 2)
        self.screen_region = (
            0,
            0,
            self.screen[0],
            self.screen[1]
        )
        self.fov = (self.cfg.capture_fov_x, self.cfg.capture_fov_y)
        self.fov_center = (self.fov[0] // 2, self.fov[1] // 2)
        self.fov_region = (
            self.screen_center[0] - self.fov[0] // 2,
            self.screen_center[1] - self.fov[1] // 2 - self.cfg.screen_center_offset,
            self.screen_center[0] + self.fov[0] // 2,
            self.screen_center[1] + self.fov[1] // 2 - self.cfg.screen_center_offset
        )
        self.thresh = None
        self.target = None
        self.closest_contour = None
        self.img = None
        self.aim_fov = (self.cfg.aim_fov_x, self.cfg.aim_fov_y)

        # Setup debug display
        if self.cfg.debug:
            self.display_mode = self.cfg.display_mode
            self.window_name = 'Python'
            self.window_resolution = (
                self.screen[0] // 2,
                self.screen[1] // 2
            )
            cv2.namedWindow(self.window_name)

    def __del__(self):
        del self.cam

    def screenshot(self, region):
        while True:
            image = self.cam.grab(region)
            if image is not None:
                return np.array(image)

    def get_target(self, recoil_offset):
        # Convert the offset to an integer, since it is used to define the capture region
        recoil_offset = int(recoil_offset)

        # Reset variables
        self.target = None
        trigger = False
        self.closest_contour = None

        # Capture a screenshot
        self.img = self.screenshot(self.get_region(self.fov_region, recoil_offset))

        # Convert the screenshot to HSV color space for color detection
        hsv = cv2.cvtColor(self.img, cv2.COLOR_BGR2HSV)

        # Create a mask to identify pixels within the specified color range
        mask = cv2.inRange(hsv, self.cfg.lower_color, self.cfg.upper_color)

        # Apply morphological dilation to increase the size of the detected color blobs
        kernel = np.ones((self.cfg.group_close_target_blobs_threshold[0], self.cfg.group_close_target_blobs_threshold[1]), np.uint8)
        dilated = cv2.dilate(mask, kernel, iterations=5)

        # Apply thresholding to convert the mask into a binary image
        self.thresh = cv2.threshold(dilated, 60, 255, cv2.THRESH_BINARY)[1]

        # Find contours of the detected color blobs
        contours, _ = cv2.findContours(self.thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

        # Identify the closest target contour
        if len(contours) != 0:
            min_distance = float('inf')
            for contour in contours:
                # Make a bounding rectangle for the target
                rect_x, rect_y, rect_w, rect_h = cv2.boundingRect(contour)

                # Calculate the coordinates of the center of the target
                x = rect_x + rect_w // 2 - self.fov_center[0]
                y = int(rect_y + rect_h * (1 - self.cfg.aim_height)) - self.fov_center[1]

                # Update the closest target if the current target is closer
                distance = np.sqrt(x**2 + y**2)
                if distance < min_distance:
                    min_distance = distance
                    self.closest_contour = contour
                    if (
                            -self.aim_fov[0] <= x <= self.aim_fov[0] and
                            -self.aim_fov[1] <= y <= self.aim_fov[1]
                    ):
                        self.target = (x, y)

            if (
                # Check if crosshair is inside the closest target
                cv2.pointPolygonTest(
                    self.closest_contour, (self.fov_center[0], self.fov_center[1]), False) >= 0 and

                # Eliminate a lot of false positives by also checking pixels near the crosshair.
                cv2.pointPolygonTest(
                    self.closest_contour, (self.fov_center[0] + self.cfg.trigger_threshold, self.fov_center[1]), False) >= 0 and
                cv2.pointPolygonTest(
                    self.closest_contour, (self.fov_center[0] - self.cfg.trigger_threshold, self.fov_center[1]), False) >= 0 and
                cv2.pointPolygonTest(
                    self.closest_contour, (self.fov_center[0], self.fov_center[1] + self.cfg.trigger_threshold), False) >= 0 and
                cv2.pointPolygonTest(
                    self.closest_contour, (self.fov_center[0], self.fov_center[1] - self.cfg.trigger_threshold), False) >= 0
            ):
                trigger = True

        if self.cfg.debug:
            self.run_debug_window(recoil_offset)

        return self.target, trigger

    @staticmethod
    def get_region(region, recoil_offset):
        region = (
            region[0],
            region[1] - recoil_offset,
            region[2],
            region[3] - recoil_offset
        )
        return region

    def run_debug_window(self, recoil_offset):
        if self.display_mode == 'game':
            debug_img = self.img
        else:
            debug_img = self.thresh
            debug_img = cv2.cvtColor(debug_img, cv2.COLOR_GRAY2BGR)

        full_img = self.screenshot(self.screen_region)

        # Draw line to the closest target
        if self.target is not None:
            debug_img = cv2.line(
                debug_img,
                self.fov_center,
                (self.target[0] + self.fov_center[0], self.target[1] + self.fov_center[1]),
                (0, 255, 0),
                2
            )

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

        # Draw FOV, a green rectangle
        debug_img = cv2.rectangle(
            debug_img,
            (0, 0),
            (self.fov[0], self.fov[1]),
            (0, 255, 0),
            2
        )

        # Draw Aim FOV, a yellow rectangle
        debug_img = cv2.rectangle(
            debug_img,
            (
                self.fov[0] // 2 - self.aim_fov[0] // 2,
                self.fov[1] // 2 - self.aim_fov[1] // 2
            ),
            (
                self.fov[0] // 2 + self.aim_fov[0] // 2,
                self.fov[1] // 2 + self.aim_fov[1] // 2
            ),
            (0, 255, 255),
            2
        )

        offset_x = (self.screen[0] - self.fov[0]) // 2
        offset_y = (self.screen[1] - self.fov[1]) // 2 - self.cfg.screen_center_offset - recoil_offset
        full_img[offset_y:offset_y+debug_img.shape[0], offset_x:offset_x+debug_img.shape[1]] = debug_img
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
