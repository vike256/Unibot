# Copyright (C) 2026 vike256 — Unibot. See LICENSE.txt for full GPL-3.0 license.
from .base_mouse import DriverMouse
import win32api
import win32con


class WinApiMouse(DriverMouse):
    label = "WinApi"

    def mouse_down(self):
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)

    def mouse_up(self):
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)

    def send_move(self, x, y):
        win32api.mouse_event(win32con.MOUSEEVENTF_MOVE, x, y, 0, 0)
        if self.cfg.debug:
            print(f'({self.label}) Sent: Move({x}, {y})')
