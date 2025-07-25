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
import win32api


class Cheats:
    def __init__(self, config):
        self.cfg = config
        self.move_x, self.move_y = (0, 0)
        self.previous_x, self.previous_y = (0, 0)
        self.recoil_offset = 0

    def calculate_aim(self, state, target):
        if state and target is not None:
            x, y = target

            # Calculate x and y speed
            x *= self.cfg.speed
            y *= self.cfg.speed * self.cfg.y_speed_multiplier

            # Apply smoothing with the previous x and y value
            x = (1 - self.cfg.aim_smoothing_factor) * self.previous_x + self.cfg.aim_smoothing_factor * x
            y = (1 - self.cfg.aim_smoothing_factor) * self.previous_y + self.cfg.aim_smoothing_factor * y

            # Store the calculated values for next calculation
            self.previous_x, self.previous_y = (x, y)
            # Apply x and y to the move variables
            self.move_x, self.move_y = (x, y)

    def apply_recoil(self, state, delta_time):
        if state and delta_time != 0:
            # Mode move just applies configured movement to the move values
            if self.cfg.recoil_mode == 'move' and win32api.GetAsyncKeyState(0x01) < 0:
                self.move_x += self.cfg.recoil_x * delta_time
                self.move_y += self.cfg.recoil_y * delta_time
            # Mode offset moves the camera upward, so it aims below target
            elif self.cfg.recoil_mode == 'offset':
                # Add recoil_y to the offset when mouse1 is down
                if win32api.GetAsyncKeyState(0x01) < 0:
                    if self.recoil_offset < self.cfg.max_offset:
                        self.recoil_offset += self.cfg.recoil_y * delta_time
                        if self.recoil_offset > self.cfg.max_offset:
                            self.recoil_offset = self.cfg.max_offset
                # Start resetting the offset bit by bit if mouse1 is not down
                else:
                    if self.recoil_offset > 0:
                        self.recoil_offset -= self.cfg.recoil_recover * delta_time
                        if self.recoil_offset < 0:
                            self.recoil_offset = 0
        else:
            # Reset recoil offset if recoil is off
            self.recoil_offset = 0
