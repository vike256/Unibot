# Copyright (C) 2026 vike256 — Unibot. See LICENSE.txt for full GPL-3.0 license.
import win32api
from time import sleep


class KeybindManager:
    """Handles all keyboard and mouse input state checking."""

    def __init__(self, config):
        self.cfg = config
        self.delay = 0.25

    def check_key_binds(self, cheats):
        """Check for reload, toggle, and exit key presses.
        Returns True if the config should be reloaded."""
        if win32api.GetAsyncKeyState(self.cfg.key_reload_config) < 0:
            return True

        if win32api.GetAsyncKeyState(self.cfg.key_toggle_aim) < 0:
            cheats.toggle_aim()
            sleep(self.delay)

        if win32api.GetAsyncKeyState(self.cfg.key_toggle_recoil) < 0:
            cheats.toggle_recoil()
            sleep(self.delay)

        if win32api.GetAsyncKeyState(self.cfg.key_exit) < 0:
            print("Exiting")
            exit(1)

        return False

    def get_trigger_state(self):
        return win32api.GetAsyncKeyState(self.cfg.key_trigger) < 0

    def get_rapid_fire_state(self):
        return win32api.GetAsyncKeyState(self.cfg.key_rapid_fire) < 0
