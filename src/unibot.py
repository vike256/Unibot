# Copyright (C) 2026 vike256 — Unibot. See LICENSE.txt for full GPL-3.0 license.
import time
import random
import ctypes

from configReader import ConfigReader
from keybinds import KeybindManager
from mouse import get_mouse_implementation
from screen import Screen


class Unibot:
    def run(self):
        self._boost_process_priority()
        self.print_license()
        while True:
            config = ConfigReader()
            config.read_config()

            keybinds = KeybindManager(config)
            mouse = get_mouse_implementation(config)
            screen = Screen(config)

            if config.trigger_mode == 'head':
                print('Unibot ON - head mode: fires when the crosshair is on a head, no key needed')
            elif config.trigger_mode == 'both':
                print('Unibot ON - both mode: heads always, anything else while the trigger key is held')
            else:
                print('Unibot ON - hold the trigger key to fire, release to stop')
            print('F5 switches mode, F6 pause, F1 reloads config, F4 exits')

            # Triggerbot loop
            try:
                while True:
                    start_time = time.perf_counter()

                    reload_config = keybinds.check_key_binds()
                    if reload_config:
                        break

                    if self._should_process_frame(keybinds, config):
                        trigger = screen.get_trigger(keybinds.get_trigger_state())

                        if trigger:
                            mouse.click(self._calculate_trigger_delay(config))

                    # Do not loop above the set refresh rate (0 = uncapped)
                    if config.min_loop_time:
                        time_spent = (time.perf_counter() - start_time) * 1000
                        if time_spent < config.min_loop_time:
                            time.sleep((config.min_loop_time - time_spent) / 1000)
            finally:
                # Also runs when F4 raises SystemExit, so resources are freed
                screen.close()
                mouse.close()

            print('Reloading')

    def _should_process_frame(self, keybinds, config):
        """Returns True if the frame should be processed for target detection."""
        if keybinds.paused:
            return False
        return (config.trigger_mode in ('head', 'both')
                or keybinds.get_trigger_state()
                or (config.debug and config.debug_always_on))

    @staticmethod
    def _boost_process_priority():
        """Raise the process priority so the triggerbot is scheduled with less jitter."""
        try:
            high_priority_class = 0x00000080
            ctypes.windll.kernel32.SetPriorityClass(
                ctypes.windll.kernel32.GetCurrentProcess(), high_priority_class
            )
        except OSError:
            pass

    def _calculate_trigger_delay(self, config):
        """Calculate the randomized delay before a triggerbot click."""
        if config.trigger_delay == 0:
            return 0
        return (random.randint(0, max(config.trigger_randomization - 1, 0)) + config.trigger_delay) / 1000

    def print_license(self):
        print('Unibot  Copyright (C) 2026  vike256 \n'
              'This program comes with ABSOLUTELY NO WARRANTY. \n'
              'This is free software, and you are welcome to redistribute it under certain conditions. \n'
              'For details see <LICENSE.txt>.')