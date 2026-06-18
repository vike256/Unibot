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
import interception


class InterceptionMouse(DriverMouse):
    label = "Interception"

    def __init__(self, config):
        super().__init__(config)
        interception.auto_capture_devices(mouse=True)

    def mouse_down(self):
        interception.mouse_down('left')

    def mouse_up(self):
        interception.mouse_up('left')

    def send_move(self, x, y):
        interception.move_relative(x, y)
        if self.cfg.debug:
            print(f'({self.label}) Sent: Move({x}, {y})')
