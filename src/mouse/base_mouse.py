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
import abc
import threading
import time


class BaseMouse(abc.ABC):
    def __init__(self, config):
        self.cfg = config
        self.click_thread = threading.Thread(target=self.send_click)
        self.last_click_time = time.time()
        self.remainder_x = 0
        self.remainder_y = 0


    @abc.abstractmethod
    def send_move(self, x: int, y: int):
        pass


    @abc.abstractmethod
    def send_click(self, delay_beforeclick: int = 0):
        pass


    def calculate_move_amount(self, move_x, move_y):
        # Add the remainder from the previous calculation
        move_x += self.remainder_x
        move_y += self.remainder_y

        # Round x and y, and calculate the new remainder
        self.remainder_x = move_x
        self.remainder_y = move_y
        move_x = int(move_x)
        move_y = int(move_y)
        self.remainder_x -= move_x
        self.remainder_y -= move_y

        return (move_x, move_y)


    def click(self, delay_before_click=0):
        if (
                not self.click_thread.is_alive() and
                time.time() - self.last_click_time >= 1 / self.cfg.target_cps
        ):
            self.click_thread = threading.Thread(target=self.send_click, args=(delay_before_click,))
            self.click_thread.start()


    def move(self, x: float, y: float):
        move_x, move_y = self.calculate_move_amount(x, y)
        self.send_move(move_x, move_y)
