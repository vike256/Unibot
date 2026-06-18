"""
    Unibot, an open-source colorbot.
    Copyright (C) 2026 vike256

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
import time
import cv2
import numpy as np
import dxcam
from pyautogui import size


class Screen:
    def __init__(self, config):
        self.cfg = config
        self.cam = dxcam.create(output_color="BGR")

        if self.cfg.auto_detect_resolution:
            screen_size = size()
            self.screen = (screen_size.width, screen_size.height)
        else:
            self.screen = (self.cfg.resolution_x, self.cfg.resolution_y)

        self.screen_center = (self.screen[0] // 2, self.screen[1] // 2)
        self.screen_region = (0, 0, self.screen[0], self.screen[1])
        self.fov = (self.cfg.capture_fov_x, self.cfg.capture_fov_y)
        self.fov_center = (self.fov[0] // 2, self.fov[1] // 2)
        self.fov_region = (
            self.screen_center[0] - self.fov[0] // 2,
            self.screen_center[1] - self.fov[1] // 2 - self.cfg.screen_center_offset,
            self.screen_center[0] + self.fov[0] // 2,
            self.screen_center[1] + self.fov[1] // 2 - self.cfg.screen_center_offset
        )
        self.dilated = None
        self.target = None
        self.closest_contour = None
        self.closest_rect = None
        self.img = None
        self.aim_fov = (self.cfg.aim_fov_x, self.cfg.aim_fov_y)
        self.dilate_kernel = np.ones(
            (self.cfg.group_close_target_blobs_threshold[0], self.cfg.group_close_target_blobs_threshold[1]),
            np.uint8
        )
        self.trigger_test_points = [
            (self.fov_center[0], self.fov_center[1]),
            (self.fov_center[0] + self.cfg.trigger_threshold, self.fov_center[1]),
            (self.fov_center[0] - self.cfg.trigger_threshold, self.fov_center[1]),
            (self.fov_center[0], self.fov_center[1] + self.cfg.trigger_threshold),
            (self.fov_center[0], self.fov_center[1] - self.cfg.trigger_threshold),
        ]

        # Setup debug display
        if self.cfg.debug:
            self.display_mode = self.cfg.display_mode
            self.window_name = 'Python'
            self.window_resolution = (self.screen[0] // 2, self.screen[1] // 2)
            cv2.namedWindow(self.window_name)

    def close(self):
        if self.cam is not None:
            self.cam.release()
            self.cam = None
        if self.cfg.debug:
            cv2.destroyWindow(self.window_name)

    def screenshot(self, region):
        while True:
            image = self.cam.grab(region)
            if image is not None:
                return image
            time.sleep(0.001)

    @staticmethod
    def get_region(region, recoil_offset):
        return (
            region[0],
            region[1] - recoil_offset,
            region[2],
            region[3] - recoil_offset
        )

    def _is_within_aim_fov(self, x, y):
        """Check if a point is within the aim FOV bounds."""
        return -self.aim_fov[0] <= x <= self.aim_fov[0] and -self.aim_fov[1] <= y <= self.aim_fov[1]

    def _check_trigger(self, contour, rect):
        """Check if the crosshair is inside the target contour with a bounding-box pre-filter."""
        cx, cy, cw, ch = rect
        if not (
            cx <= self.fov_center[0] - self.cfg.trigger_threshold and
            self.fov_center[0] + self.cfg.trigger_threshold <= cx + cw and
            cy <= self.fov_center[1] - self.cfg.trigger_threshold and
            self.fov_center[1] + self.cfg.trigger_threshold <= cy + ch
        ):
            return False

        points = self.trigger_test_points
        return all(cv2.pointPolygonTest(contour, pt, False) >= 0 for pt in points)

    def get_target(self, recoil_offset):
        recoil_offset = int(recoil_offset)

        self.target = None
        trigger = False
        self.closest_contour = None
        self.closest_rect = None

        self.img = self.screenshot(self.get_region(self.fov_region, recoil_offset))
        hsv = cv2.cvtColor(self.img, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv, self.cfg.lower_color, self.cfg.upper_color)

        self.dilated = cv2.dilate(mask, self.dilate_kernel, iterations=5)

        contours, _ = cv2.findContours(self.dilated, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        if len(contours) != 0:
            min_distance_sq = float('inf')
            for contour in contours:
                rect_x, rect_y, rect_w, rect_h = cv2.boundingRect(contour)
                x = rect_x + rect_w // 2 - self.fov_center[0]
                y = int(rect_y + rect_h * (1 - self.cfg.aim_height)) - self.fov_center[1]

                distance_sq = x * x + y * y
                if distance_sq < min_distance_sq:
                    min_distance_sq = distance_sq
                    self.closest_contour = contour
                    self.closest_rect = (rect_x, rect_y, rect_w, rect_h)
                    if self._is_within_aim_fov(x, y):
                        self.target = (x, y)

            if self.closest_contour is not None and self._check_trigger(self.closest_contour, self.closest_rect):
                trigger = True

        if self.cfg.debug:
            self.run_debug_window(recoil_offset)

        return self.target, trigger

    def _draw_target_overlay(self, debug_img):
        """Draw target line and bounding box on the debug image."""
        if self.target is not None:
            debug_img = cv2.line(
                debug_img,
                self.fov_center,
                (self.target[0] + self.fov_center[0], self.target[1] + self.fov_center[1]),
                (0, 255, 0),
                2
            )

        if self.closest_contour is not None:
            x, y, w, h = self.closest_rect
            debug_img = cv2.rectangle(
                debug_img,
                (x, y),
                (x + w, y + h),
                (0, 0, 255),
                2
            )

        return debug_img

    def _draw_fov_overlay(self, debug_img):
        """Draw FOV and Aim FOV rectangles on the debug image."""
        debug_img = cv2.rectangle(
            debug_img,
            (0, 0),
            (self.fov[0], self.fov[1]),
            (0, 255, 0),
            2
        )

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

        return debug_img

    def _show_fullscreen_debug(self, debug_img, recoil_offset):
        """Show the debug overlay composited onto a full-screen screenshot."""
        full_img = self.screenshot(self.screen_region)

        offset_x = (self.screen[0] - self.fov[0]) // 2
        offset_y = (self.screen[1] - self.fov[1]) // 2 - self.cfg.screen_center_offset - recoil_offset
        full_img[offset_y:offset_y+debug_img.shape[0], offset_x:offset_x+debug_img.shape[1]] = debug_img

        full_img = cv2.rectangle(
            full_img,
            (self.screen_center[0] - 5, self.screen_center[1] - 5),
            (self.screen_center[0] + 5, self.screen_center[1] + 5),
            (255, 255, 255),
            1
        )
        full_img = cv2.resize(full_img, self.window_resolution)
        cv2.imshow(self.window_name, full_img)

    def _show_fov_debug(self, debug_img):
        """Show only the FOV region debug overlay."""
        debug_img = cv2.line(
            debug_img,
            (self.fov_center[0] - 5, self.fov_center[1]),
            (self.fov_center[0] + 5, self.fov_center[1]),
            (255, 255, 255),
            1
        )
        debug_img = cv2.line(
            debug_img,
            (self.fov_center[0], self.fov_center[1] - 5),
            (self.fov_center[0], self.fov_center[1] + 5),
            (255, 255, 255),
            1
        )
        cv2.imshow(self.window_name, debug_img)

    def run_debug_window(self, recoil_offset):
        if self.display_mode == 'game':
            debug_img = self.img
        else:
            debug_img = cv2.cvtColor(self.dilated, cv2.COLOR_GRAY2BGR)

        debug_img = self._draw_target_overlay(debug_img)
        debug_img = self._draw_fov_overlay(debug_img)

        if self.cfg.debug_fullscreen_capture:
            self._show_fullscreen_debug(debug_img, recoil_offset)
        else:
            self._show_fov_debug(debug_img)

        cv2.waitKey(1)
