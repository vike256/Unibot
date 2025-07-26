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
from .base_mouse import BaseMouse
import abc
import numpy as np
import threading
import time


class BaseMicrocontrollerMouse(BaseMouse, abc.ABC):
    def __init__(self, config):
        super().__init__(config)
        self.send_command_lock = threading.Lock()  # used to not send multiple mouse clicks at the same time


    def __del__(self):
        self.close_connection()


    @abc.abstractmethod
    def close_connection(self):
        pass


    @abc.abstractmethod
    def send_command(self, command):
        pass
    
    def send_move(self, x: int, y: int):
        self.send_command(f'M{x},{y}\r')
    

    def send_click(self, delay_before_click: int = 0):
        time.sleep(delay_before_click)
        self.last_click_time = time.time()

        self.send_command('C\r')
        
        time.sleep((np.random.randint(10) + 25) / 1000)  # Sleep to avoid sending another click instantly after mouseup
