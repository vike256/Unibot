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
from .base_mouse import DriverMouse
import win32api
import win32con


class WinApiMouse(DriverMouse):
    label = "WinApi"

    def __init__(self, config):
        super().__init__(config)

    def mouse_down(self):
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)

    def mouse_up(self):
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)

    def send_move(self, x, y):
        win32api.mouse_event(win32con.MOUSEEVENTF_MOVE, x, y, 0, 0)
        if self.cfg.debug:
            print(f'({self.label}) Sent: Move({x}, {y})')
