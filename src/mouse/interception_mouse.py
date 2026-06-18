# Copyright (C) 2026 vike256 — Unibot. See LICENSE.txt for full GPL-3.0 license.
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
