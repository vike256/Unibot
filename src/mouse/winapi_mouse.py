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
from mouse import BaseMouse
import numpy as np
import time
import win32api
import win32con


class WinApiMouse(BaseMouse):
    def __init__(self, config):
        super().__init__(config)


    def send_click(self, delay_before_click=0):
        time.sleep(delay_before_click)
        self.last_click_time = time.time()

        random_delay = (np.random.randint(40) + 40) / 1000
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
        time.sleep(random_delay)
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)
        print(f'(WinApi) Sent: Click(random_delay={random_delay * 1000:g})')

        time.sleep((np.random.randint(10) + 25) / 1000)  # Sleep to avoid sending another click instantly after mouseup


    def send_move(self, x, y):
        win32api.mouse_event(win32con.MOUSEEVENTF_MOVE, x, y, 0, 0)
        print(f'(WinApi) Sent: Move({x}, {y})')
