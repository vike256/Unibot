# Copyright (C) 2026 vike256 — Unibot. See LICENSE.txt for full GPL-3.0 license.
from .base_mouse import BaseMouse
import abc
import threading
import time
import random


class BaseMicrocontrollerMouse(BaseMouse, abc.ABC):
    def __init__(self, config):
        super().__init__(config)
        self.send_command_lock = threading.Lock()  # used to not send multiple mouse clicks at the same time
        self.click_cmd = 'C\r'

    @staticmethod
    def get_move_cmd(x, y):
        return f'M{x},{y}\r'

    def __del__(self):
        self.close_connection()

    def send_click(self, delay_before_click: int = 0):
        time.sleep(delay_before_click)

        self.send_command(self.click_cmd)
        
        time.sleep(random.randint(25, 34) / 1000)  # Sleep to avoid sending another click instantly after mouseup

    def send_move(self, x: int, y: int):
        self.send_command(self.get_move_cmd(x, y))

    @abc.abstractmethod
    def connect_to_board(self):
        pass

    @abc.abstractmethod
    def send_command(self, command):
        pass

    @abc.abstractmethod
    def get_response(self):
        pass

    def close_connection(self):
        if self.board is not None:
            self.board.close()
            self.board = None

    def close(self):
        super().close()
        self.close_connection()
