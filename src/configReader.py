from configparser import ConfigParser
import numpy as np
import os


class ConfigReader:
    def __init__(self):
        self.parser = ConfigParser()

        # Get config path and read it
        self.path = os.path.join(os.path.dirname(__file__), '../config.ini')
        self.parser.read(self.path)


    def read_config(self):
        # Get communication settings
        value = self.parser.get('communication', 'type').lower()
        com_type_list = ['none', 'driver', 'serial', 'socket']
        if value in com_type_list:
            self.com_type = value
        else:
            print('ERROR: Invalid com_type value')
            exit(1)

        match self.parser.get('communication', 'encrypt').lower():
            case 'true':
                self.encrypt = True
            case _:
                self.encrypt = False
        
        match self.com_type:
            case 'socket':
                self.ip = self.parser.get('communication', 'ip')
                self.port = int(self.parser.get('communication', 'port'))
            case 'serial':
                self.com_port = self.parser.get('communication', 'com_port')


        # Get screen settings  
        value = self.parser.get('screen', 'detection_type').lower()
        detection_type_list = ['pixel', 'shape']
        if value in detection_type_list:
            self.detection_type = value
        else:
            print('ERROR: Invalid detection_type value')
            exit(1)

        upper_color = self.parser.get('screen', 'upper_color').split(',')
        lower_color = self.parser.get('screen', 'lower_color').split(',')
        for i in range(0, 3):
            upper_color[i] = int(upper_color[i].strip())
        for i in range(0, 3):
            lower_color[i] = int(lower_color[i].strip())
        self.upper_color = np.array(upper_color)
        self.lower_color = np.array(lower_color)

        self.fov = int(self.parser.get('screen', 'fov'))
        fps_value = int(self.parser.get('screen', 'fps'))
        self.fps = int(np.floor(1000 / fps_value + 1))


        # Get aim settings
        self.offset = int(self.parser.get('aim', 'offset'))

        value = float(self.parser.get('aim', 'smooth'))
        if 0 <= value < 1:
            self.smooth = 1 - value
        else:
            print('ERROR: Invalid smooth value')
            exit(1)

        self.speed = float(self.parser.get('aim', 'speed'))
        self.x_multiplier = float(self.parser.get('aim', 'x_multiplier'))

        value = float(self.parser.get('aim', 'head_height'))
        if 0 <= value <= 1:
            self.head_height = value
        else:
            print('ERROR: Invalid head_height value')
            exit(1)


        # Get recoil settings
        value = self.parser.get('recoil', 'mode').lower()
        recoil_mode_list = ['move', 'offset']
        if value in recoil_mode_list:
            self.recoil_mode = value
        else:
            print('ERROR: Invalid recoil_mode value')
            exit(1)

        match self.recoil_mode:
            case 'move':
                self.recoil_x = float(self.parser.get('recoil', 'recoil_x'))
                self.recoil_y = float(self.parser.get('recoil', 'recoil_y'))
            case 'offset':
                self.recoil_y = float(self.parser.get('recoil', 'recoil_y'))
                self.max_offset = int(self.parser.get('recoil', 'max_offset'))
                self.recoil_recover = float(self.parser.get('recoil', 'recover'))
        

        # Get keybind settings
        self.key_reload_config = self.parser.get('keybinds', 'key_reload_config')
        self.key_toggle_aim = self.parser.get('keybinds', 'key_toggle_aim')
        self.key_toggle_recoil = self.parser.get('keybinds', 'key_toggle_recoil')
        self.key_trigger = int(self.parser.get('keybinds', 'key_trigger'))
        self.key_exit = self.parser.get('keybinds', 'key_exit')


        # Get debug settings
        value = self.parser.get('debug', 'enabled').lower()
        if value == 'true':
            self.debug = True
            value = self.parser.get('debug', 'display_mode').lower()
            display_mode_list = ['game', 'mask']
            if value in display_mode_list:
                self.display_mode = value
            else:
                print('ERROR: Invalid display_mode value')
                exit(1)
        else:
            self.debug = False
