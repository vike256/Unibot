# Copyright (C) 2026 vike256 — Unibot. See LICENSE.txt for full GPL-3.0 license.
import win32api


class KeybindManager:
    """Handles all keyboard and mouse input state checking."""

    def __init__(self, config):
        self.cfg = config
        self.paused = False
        # Track press edges so a held key does not fire repeatedly. Sampled at
        # construction so a key still held across a config reload does not retrigger.
        self._prev = {}
        for key in (config.key_reload_config, config.key_exit, config.key_toggle_mode, config.key_toggle_pause):
            self._prev[key] = self._is_down(key)

    @staticmethod
    def _is_down(key):
        return win32api.GetAsyncKeyState(key) < 0

    def _pressed(self, key):
        """True only on the frame the key goes from released to pressed."""
        down = self._is_down(key)
        was_down = self._prev.get(key, False)
        self._prev[key] = down
        return down and not was_down

    def check_key_binds(self):
        """Handles mode switch, reload and exit.
        Returns True if the config should be reloaded."""
        if self._pressed(self.cfg.key_toggle_mode):
            modes = ('normal', 'head', 'both')
            index = modes.index(self.cfg.trigger_mode) if self.cfg.trigger_mode in modes else 0
            self.cfg.trigger_mode = modes[(index + 1) % len(modes)]
            print(f'Mode: {self.cfg.trigger_mode}')

        if self._pressed(self.cfg.key_toggle_pause):
            self.paused = not self.paused
            print('Paused' if self.paused else 'Resumed')

        if self._pressed(self.cfg.key_reload_config):
            return True

        if self._pressed(self.cfg.key_exit):
            print("Exiting")
            # SystemExit so Unibot.run()'s finally block releases the camera and port
            raise SystemExit(0)

        return False

    def get_trigger_state(self):
        return self._is_down(self.cfg.key_trigger)