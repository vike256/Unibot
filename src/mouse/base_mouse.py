# Copyright (C) 2026 vike256 — Unibot. See LICENSE.txt for full GPL-3.0 license.
import abc
import threading
import time
import queue
import random


class BaseMouse(abc.ABC):
    def __init__(self, config):
        self.cfg = config
        self.click_queue = queue.Queue()
        self.click_worker = threading.Thread(target=self._click_worker, daemon=True)
        self.click_worker.start()
        self.last_click_time = time.time()
        self.remainder_x = 0
        self.remainder_y = 0
        self.min_click_interval = 1 / config.target_cps

    def _click_worker(self):
        while True:
            delay_before_click = self.click_queue.get()
            if delay_before_click is None:
                break
            self.send_click(delay_before_click)

    @abc.abstractmethod
    def send_click(self, delay_before_click: int = 0):
        pass

    @abc.abstractmethod
    def send_move(self, x: int, y: int):
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
        if (time.time() - self.last_click_time >= self.min_click_interval
                and self.click_queue.empty()):
            self.last_click_time = time.time()
            self.click_queue.put(delay_before_click)

    def move(self, x: float, y: float):
        move_x, move_y = self.calculate_move_amount(x, y)
        self.send_move(move_x, move_y)

    def close(self):
        self.click_queue.put(None)
        self.click_worker.join(timeout=1.0)


class DriverMouse(BaseMouse, abc.ABC):
    """Base class for driver-based mice (WinApi, Interception) that handle
    physical mouse_down / mouse_up events."""

    def send_click(self, delay_before_click=0):
        time.sleep(delay_before_click)

        random_delay = random.randint(40, 80) / 1000
        self.mouse_down()
        time.sleep(random_delay)
        self.mouse_up()
        if self.cfg.debug:
            print(f'({self.label}) Sent: Click(random_delay={random_delay * 1000:g})')

        time.sleep(random.randint(25, 34) / 1000)

    @abc.abstractmethod
    def mouse_down(self):
        pass

    @abc.abstractmethod
    def mouse_up(self):
        pass
