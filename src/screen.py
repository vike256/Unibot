# Copyright (C) 2026 vike256 — Unibot. See LICENSE.txt for full GPL-3.0 license.
import time
import cv2
import numpy as np
import dxcam
from comtypes import COMError

# Blobs closer than this kernel get grouped into one target.
BLOB_GROUPING_RADIUS = 5

# Head-band detection. The head is the top of the target, but how tall it is
# depends on what the highlight covers: a standing enemy shows head + shoulders,
# while an enemy behind cover or far away shows the head alone. Treating
# head_height as a fraction of the whole bounding box put the "head" inside the
# top 20% of a bare head, so a crosshair sitting on the head never fired.
NECK_JUMP_RATIO = 0.4         # shoulders at least this much wider than the head
SHOULDER_PERSIST_RATIO = 0.9  # rows below the neck stay this wide (rejects hollow outlines)
HEAD_MAX_ASPECT = 2.0         # taller than this is a body even if the neck is invisible


class Screen:
    def __init__(self, config):
        self.cfg = config
        self.cam = self._create_cam()
        self._apply_screen_geometry()
        self._missed_since = None
        self._last_capture_error = 0.0

        # Preallocated buffers so the hot path does not allocate per frame
        self.hsv = np.empty((self.fov[1], self.fov[0], 3), np.uint8)
        self.mask = np.empty((self.fov[1], self.fov[0]), np.uint8)
        self.dilated = np.empty((self.fov[1], self.fov[0]), np.uint8)

        # Closing = dilate then erode, so nearby blobs get grouped WITHOUT the
        # target growing. A plain dilate inflated every target by the radius and
        # made the triggerbot fire while off target.
        w, h = self.cfg.group_close_target_blobs_threshold
        self.close_kernel = cv2.getStructuringElement(
            cv2.MORPH_RECT,
            (BLOB_GROUPING_RADIUS * (w - 1) + 1, BLOB_GROUPING_RADIUS * (h - 1) + 1)
        )

        self.img = None
        self.closest_contour = None
        self.closest_rect = None
        self._last_ticks = None
        self._last_trigger = False

        if self.cfg.debug:
            self.display_mode = self.cfg.display_mode
            self.window_name = 'Python'
            self.window_resolution = (self.screen[0] // 2, self.screen[1] // 2)
            cv2.namedWindow(self.window_name)

    def _create_cam(self):
        cam = dxcam.create(output_color="BGR")
        if cam is None:
            raise RuntimeError("Could not create a capture device (dxcam).")
        return cam

    def _apply_screen_geometry(self):
        """(Re)derive capture regions from the current capture device.

        Split out of __init__ so display changes can rebuild everything without
        restarting: dxcam's output recovery can recreate the camera with a new
        resolution, and every region depends on it.
        """
        # Read the resolution from the capture device so it always matches the
        # region dxcam validates against (avoids DPI-scaling mismatches).
        if self.cfg.auto_detect_resolution:
            self.screen = (self.cam.width, self.cam.height)
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

    def _recover_capture(self, error):
        """Recreate the capture device after a capture error.

        Display mode changes and HDR toggles invalidate desktop duplication; dxcam's
        internal recovery does not cover every case (e.g. DXGI_ERROR_INVALID_CALL
        raised as COMError from AcquireNextFrame). Returning False instead of
        crashing keeps the triggerbot alive through alt-tabs and resolution swaps.
        """
        now = time.perf_counter()
        if now - self._last_capture_error > 1.0:
            print(f'Screen capture error, recreating capture device: {error}')
        self._last_capture_error = now
        try:
            self.cam.release()
        except Exception:
            pass
        self.cam = None
        # dxcam caches instances per output; give the system a beat before recreating
        time.sleep(0.25)
        for _ in range(10):
            try:
                self.cam = self._create_cam()
                break
            except RuntimeError:
                time.sleep(0.5)
        if self.cam is None:
            raise RuntimeError("Could not recreate the capture device (dxcam).")
        self._apply_screen_geometry()
        self._missed_since = None
        self._last_ticks = None

    def close(self):
        if self.cam is not None:
            self.cam.release()
            self.cam = None
        if self.cfg.debug:
            try:
                cv2.destroyWindow(self.window_name)
            except cv2.error:
                pass

    def screenshot(self, region):
        # Non-blocking: returns the newest frame without pulling a fresh desktop
        # duplication per call.
        try:
            frame = self.cam.grab(region, copy=False, new_frame_only=False)
        except COMError as e:
            self._recover_capture(e)
            return None
        if frame is not None:
            self._missed_since = None
            return frame

        if self._missed_since is None:
            self._missed_since = time.perf_counter()
        elif time.perf_counter() - self._missed_since > 2:
            print("WARNING: Screen capture is returning no frames. "
                  "Use Windowed Fullscreen (Borderless) and disable HDR.")
            self._missed_since = time.perf_counter()

        while True:
            try:
                frame = self.cam.grab(region, copy=False, new_frame_only=True)
            except COMError as e:
                self._recover_capture(e)
                return None
            if frame is not None:
                return frame
            time.sleep(0.0005)

    def _effective_mode(self, trigger_held):
        """Resolve the mode for this frame.
        'normal' = fire anywhere, 'head' = heads only, 'off' = key needed but not held.
        head mode: only the top head_height fraction counts, with a tighter tolerance.
        both mode: no key = head only, key held = anywhere (normal behaviour)."""
        mode = self.cfg.trigger_mode
        if mode == 'both':
            mode = 'normal' if trigger_held else 'head'
        if mode == 'normal' and not trigger_held:
            return 'off'
        return mode

    @staticmethod
    def _row_extents(strip):
        """Width of the leftmost-to-rightmost filled pixel of every row.

        Counting filled pixels per row would report a hollow outline as narrow
        and make the detector think the whole blob is a head.
        """
        if strip.size == 0:
            return np.empty(0, np.int32)
        filled = strip.any(axis=1)
        if not filled.any():
            return np.zeros(strip.shape[0], np.int32)
        first = np.argmax(strip, axis=1)
        last = strip.shape[1] - 1 - np.argmax(strip[:, ::-1], axis=1)
        extents = (last - first + 1).astype(np.int32)
        extents[~filled] = 0
        return extents

    def _head_height(self, rect):
        """Height of the head inside this blob, in pixels from its top.

        head_height is a fraction of the whole *target*, which is only right when
        the highlight includes a body: a standing enemy is head + shoulders, so
        the head really is the top fraction. An enemy behind cover or far away
        highlights as the head alone, and scaling that by head_height put the
        "head" inside the top of the head, so aiming at it never fired.
        """
        x, y, w, h = rect
        if h <= 2 or w <= 0:
            return h * self.cfg.head_height

        # Width per row of this blob, top to bottom. Use the row's extent rather
        # than its pixel count so a hollow (outline-only) highlight measures the
        # same as a filled silhouette.
        widths = self._row_extents(self.dilated[y:y + h, x:x + w])
        if widths.size == 0:
            return h * self.cfg.head_height
        max_width = int(widths.max())
        if max_width == 0:
            return h * self.cfg.head_height

        # A body is present when a widening step is followed by a wide run of
        # rows: the shoulders. Hollow outlines and bare heads have no such run.
        jumps = np.diff(widths.astype(np.int32))
        if jumps.size:
            neck = int(np.argmax(jumps))
            if jumps[neck] >= NECK_JUMP_RATIO * max_width:
                below = widths[neck + 1:]
                if below.size and np.count_nonzero(below >= SHOULDER_PERSIST_RATIO * max_width) >= 2:
                    return h * self.cfg.head_height

        # No visible neck. Distant targets are only a few pixels wide, where the
        # closing kernel rounds the shoulders away; an elongated blob is still a
        # body, and head_height has to keep scaling it or the shot goes at the
        # whole silhouette.
        if h > HEAD_MAX_ASPECT * max(w, 1):
            return h * self.cfg.head_height

        # Otherwise the whole blob is the head.
        return float(h)

    def _check_trigger(self, contour, rect, mode):
        """True if the crosshair is on the target's head (head mode) or anywhere."""
        x, y, w, h = rect
        center_x, center_y = self.fov_center

        if mode == 'off':
            return False

        if mode == 'head':
            threshold = self.cfg.head_threshold
            if not (y - threshold <= center_y <= y + self._head_height(rect) + threshold):
                return False
        else:
            threshold = self.cfg.trigger_threshold

        if not (
            x - threshold <= center_x <= x + w + threshold and
            y - threshold <= center_y <= y + h + threshold
        ):
            return False

        return cv2.pointPolygonTest(contour, self.fov_center, True) >= -threshold

    def get_trigger(self, trigger_held):
        frame = self.screenshot(self.fov_region)

        if frame is None:
            # Capture is down and being recreated; no reliable result this frame
            self._last_trigger = False
            if self.cfg.debug:
                cv2.waitKey(1)
            return False

        # Same frame as last time -> the result cannot have changed, skip the work
        ticks = self.cam.latest_frame_ticks
        # Only skip when the backend actually reports a frame timestamp
        if ticks and ticks == self._last_ticks:
            if self.cfg.debug:
                cv2.waitKey(1)
            return self._last_trigger
        self._last_ticks = ticks
        self.img = frame

        cv2.cvtColor(self.img, cv2.COLOR_BGR2HSV, dst=self.hsv)
        cv2.inRange(self.hsv, self.cfg.lower_color, self.cfg.upper_color, dst=self.mask)
        cv2.morphologyEx(self.mask, cv2.MORPH_CLOSE, self.close_kernel, dst=self.dilated)

        contours, _ = cv2.findContours(self.dilated, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        center_x, center_y = self.fov_center
        min_area = self.cfg.min_target_area
        mode = self._effective_mode(trigger_held)
        min_distance_sq = float('inf')
        closest = None
        closest_rect = None
        trigger = False
        best_area = 0
        triggered = None
        triggered_rect = None

        for contour in contours:
            rect = cv2.boundingRect(contour)
            if rect[2] * rect[3] < min_area:  # ignore specks
                continue

            x = rect[0] + rect[2] // 2 - center_x
            y = rect[1] + rect[3] // 2 - center_y
            distance_sq = x * x + y * y
            if distance_sq < min_distance_sq:
                min_distance_sq = distance_sq
                closest = contour
                closest_rect = rect

            # Test every target, not only the closest one, and prefer the biggest
            # one that matches so a fragment cannot steal the shot
            area = rect[2] * rect[3]
            if area > best_area and self._check_trigger(contour, rect, mode):
                trigger = True
                best_area = area
                triggered = contour
                triggered_rect = rect

        self.closest_contour = triggered if trigger else closest
        self.closest_rect = triggered_rect if trigger else closest_rect

        if self.cfg.debug:
            self.run_debug_window()

        self._last_trigger = trigger
        return trigger

    def _draw_target_overlay(self, debug_img):
        """Draw the bounding box of the matched (or closest) target."""
        if self.closest_contour is not None:
            x, y, w, h = self.closest_rect
            debug_img = cv2.rectangle(debug_img, (x, y), (x + w, y + h), (0, 0, 255), 2)
            if self.cfg.trigger_mode in ('head', 'both'):
                head_y = int(y + self._head_height(self.closest_rect))
                debug_img = cv2.line(debug_img, (x, head_y), (x + w, head_y), (255, 0, 0), 2)
        return debug_img

    def _draw_fov_overlay(self, debug_img):
        """Draw the FOV rectangle on the debug image."""
        return cv2.rectangle(debug_img, (0, 0), (self.fov[0], self.fov[1]), (0, 255, 0), 2)

    def _show_fullscreen_debug(self, debug_img):
        """Show the debug overlay composited onto a full-screen screenshot."""
        full_img = self.screenshot(self.screen_region)

        offset_x = (self.screen[0] - self.fov[0]) // 2
        offset_y = (self.screen[1] - self.fov[1]) // 2 - self.cfg.screen_center_offset
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
        for dx, dy in ((5, 0), (0, 5)):
            debug_img = cv2.line(
                debug_img,
                (self.fov_center[0] - dx, self.fov_center[1] - dy),
                (self.fov_center[0] + dx, self.fov_center[1] + dy),
                (255, 255, 255),
                1
            )
        cv2.imshow(self.window_name, debug_img)

    def run_debug_window(self):
        if self.display_mode == 'game':
            debug_img = self.img
        else:
            debug_img = cv2.cvtColor(self.dilated, cv2.COLOR_GRAY2BGR)

        debug_img = self._draw_target_overlay(debug_img)
        debug_img = self._draw_fov_overlay(debug_img)

        if self.cfg.debug_fullscreen_capture:
            self._show_fullscreen_debug(debug_img)
        else:
            self._show_fov_debug(debug_img)

        cv2.waitKey(1)