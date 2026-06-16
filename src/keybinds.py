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
