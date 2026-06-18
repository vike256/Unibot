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
import time
import random

from cheats import Cheats
from configReader import ConfigReader
from keybinds import KeybindManager
from mouse import get_mouse_implementation
from screen import Screen


class Unibot:
    def run(self):
        self.print_license()
        while True:
            # Track delta time
            start_time = time.perf_counter()

            config = ConfigReader()
            config.read_config()

            keybinds = KeybindManager(config)
            cheats = Cheats(config)
            mouse = get_mouse_implementation(config)
            screen = Screen(config)

            print('Unibot ON')

            # Cheat loop
            while True:
                now = time.perf_counter()
                delta_time = now - start_time
                start_time = now

                reload_config = keybinds.check_key_binds(cheats)
                if reload_config:
                    break

                if self._should_process_frame(keybinds, cheats, config):
                    target, trigger = screen.get_target(cheats.recoil_offset)

                    if keybinds.get_trigger_state() and trigger:
                        delay_before_click = self._calculate_trigger_delay(config)
                        mouse.click(delay_before_click)

                    cheats.calculate_aim(cheats.get_aim_state(), target)

                if keybinds.get_rapid_fire_state():
                    mouse.click()

                # Apply recoil
                cheats.apply_recoil(cheats.recoil_state, delta_time)

                # Move the mouse based on the previous calculations
                if cheats.move_x != 0 or cheats.move_y != 0:
                    mouse.move(cheats.move_x, cheats.move_y)

                # Reset move values so the aim doesn't keep drifting when no targets are on the screen
                cheats.move_x, cheats.move_y = (0, 0)

                # Do not loop above the set refresh rate
                time_spent = (time.perf_counter() - start_time) * 1000
                if time_spent < config.min_loop_time:
                    time.sleep((config.min_loop_time - time_spent) / 1000)

            screen.close()
            mouse.close()
            del keybinds
            del cheats
            del mouse
            del screen
            del config
            print('Reloading')

    def _should_process_frame(self, keybinds, cheats, config):
        """Returns True if the frame should be processed for target detection."""
        if keybinds.get_trigger_state() or cheats.get_aim_state():
            return True
        if config.debug and config.debug_always_on:
            return True
        return False

    def _calculate_trigger_delay(self, config):
        """Calculate the randomized delay before a triggerbot click."""
        if config.trigger_delay == 0:
            return 0
        return (random.randint(0, config.trigger_randomization - 1) + config.trigger_delay) / 1000

    def print_license(self):
        print('Unibot  Copyright (C) 2026  vike256 \n'
              'This program comes with ABSOLUTELY NO WARRANTY. \n'
              'This is free software, and you are welcome to redistribute it under certain conditions. \n'
              'For details see <LICENSE.txt>.')
