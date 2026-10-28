# Copyright (C) 2026 vike256 — Unibot. See LICENSE.txt for full GPL-3.0 license.
from configparser import ConfigParser
import numpy as np
import os
import sys


class ConfigReader:
    def __init__(self):
        self.parser = ConfigParser()

        # Communication
        self.communication_type = None
        self.microcontroller_ip = None
        self.microcontroller_port = None
        self.com_port = None

        # Screen
        self.screen_center_offset = None
        self.group_close_target_blobs_threshold = None
        self.min_target_area = None
        self.upper_color = None
        self.lower_color = None
        self.capture_fov_x = None
        self.capture_fov_y = None
        self.min_loop_time = None
        self.auto_detect_resolution = None
        self.resolution_x = None
        self.resolution_y = None

        # Trigger
        self.trigger_mode = None
        self.head_height = None
        self.head_threshold = None
        self.trigger_delay = None
        self.trigger_randomization = None
        self.trigger_threshold = None
        self.click_rate = None

        # Key binds
        self.key_reload_config = None
        self.key_exit = None
        self.key_toggle_mode = None
        self.key_toggle_pause = None
        self.key_trigger = None

        # Debug
        self.debug = None
        self.debug_always_on = None
        self.display_mode = None
        self.debug_fullscreen_capture = None

        # Get config path and read it
        # Support PyInstaller one-file: config lives next to the exe, not in _MEIPASS
        base = getattr(sys, '_MEIPASS', None)
        if base and hasattr(sys, 'frozen'):
            # frozen exe: look next to the actual exe location
            exe_dir = os.path.dirname(sys.executable)
            self.path = os.path.join(exe_dir, 'config.ini')
        else:
            self.path = os.path.join(os.path.dirname(__file__), '../config.ini')
        self.parser.read(self.path)

    def read_config(self):
        # Get communication settings
        value = self.parser.get('communication', 'type').lower()
        communication_type_list = ['winapi', 'interception_driver', 'serial', 'socket']
        if value in communication_type_list:
            self.communication_type = value
        else:
            print('WARNING: Invalid communication_type value')

        match self.communication_type:
            case 'socket':
                self.microcontroller_ip = self.parser.get('communication', 'microcontroller_ip')
                self.microcontroller_port = self.parser.getint('communication', 'microcontroller_port')
            case 'serial':
                # Accept both "COM3" and "3"
                com_port = self.parser.get('communication', 'com_port').strip().upper()
                self.com_port = com_port.removeprefix('COM')

        # Get screen settings
        self.screen_center_offset = self.parser.getint('screen', 'screen_center_offset')

        values_str = self.parser.get('screen', 'group_close_target_blobs_threshold').split(',')
        self.group_close_target_blobs_threshold = (int(values_str[0].strip()), int(values_str[1].strip()))
        self.min_target_area = self.parser.getint('screen', 'min_target_area')

        self.upper_color = self._parse_color_array('screen', 'upper_color')
        self.lower_color = self._parse_color_array('screen', 'lower_color')

        self.capture_fov_x = self.parser.getint('screen', 'capture_fov_x')
        self.capture_fov_y = self.parser.getint('screen', 'capture_fov_y')
        max_loops_per_sec = self.parser.getint('screen', 'max_loops_per_sec')
        # 0 = uncapped (poll capture as fast as possible for the lowest latency)
        self.min_loop_time = 1000 // max_loops_per_sec + 1 if max_loops_per_sec > 0 else 0

        self.auto_detect_resolution = self.parser.getboolean('screen', 'auto_detect_resolution')

        self.resolution_x = self.parser.getint('screen', 'resolution_x')
        self.resolution_y = self.parser.getint('screen', 'resolution_y')

        # Get trigger settings
        value = self.parser.get('trigger', 'mode').lower()
        if value in ('normal', 'head', 'both'):
            self.trigger_mode = value
        else:
            print('WARNING: Invalid trigger mode value')
            self.trigger_mode = 'normal'

        value = self.parser.getfloat('trigger', 'head_height')
        if 0 < value <= 1:
            self.head_height = value
        else:
            print('WARNING: Invalid head_height value')
            self.head_height = 0.3

        value = self.parser.getfloat('trigger', 'head_threshold')
        if value >= 0:
            self.head_threshold = value
        else:
            print('WARNING: Invalid head_threshold value')
            self.head_threshold = 1

        self.trigger_delay = self.parser.getint('trigger', 'trigger_delay')
        self.trigger_randomization = self.parser.getint('trigger', 'trigger_randomization')
        self.trigger_threshold = self.parser.getint('trigger', 'trigger_threshold')
        self.click_rate = self.parser.getint('trigger', 'click_rate')

        # Get keybind settings
        self.key_reload_config = self.read_hex(self.parser.get('key_binds', 'key_reload_config'))
        self.key_exit = self.read_hex(self.parser.get('key_binds', 'key_exit'))
        self.key_toggle_mode = self.read_hex(self.parser.get('key_binds', 'key_toggle_mode'))
        self.key_toggle_pause = self.read_hex(self.parser.get('key_binds', 'key_toggle_pause'))
        self.key_trigger = self.read_hex(self.parser.get('key_binds', 'key_trigger'))

        # Get debug settings
        self.debug = self.parser.getboolean('debug', 'enabled')
        self.debug_always_on = self.parser.getboolean('debug', 'always_on')

        value = self.parser.get('debug', 'display_mode').lower()
        display_mode_list = ['game', 'mask']
        if value in display_mode_list:
            self.display_mode = value
        else:
            print('WARNING: Invalid display_mode value')

        self.debug_fullscreen_capture = self.parser.getboolean('debug', 'debug_fullscreen_capture', fallback=False)

    def _parse_color_array(self, section, option):
        """Parse a comma-separated color string into a numpy integer array."""
        values = self.parser.get(section, option).split(',')
        return np.array([int(v.strip()) for v in values])

    @staticmethod
    def read_hex(string):
        return int(string, 16)