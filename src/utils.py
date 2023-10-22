import keyboard
import win32api as wapi
from time import sleep
from configReader import ConfigReader


class Utils:
    def __init__(self):
        self.config = ConfigReader()
        self.reload_config()

        self.delay = 0.2
        self.key_reload_config = self.config.key_reload_config
        self.key_toggle_aim = self.config.key_toggle_aim
        self.key_toggle_recoil = self.config.key_toggle_recoil
        self.key_trigger = self.config.key_trigger
        self.key_exit = self.config.key_exit
        self.aim_state = False
        self.recoil_state = False
        self.recoil_offset = 0

    def check_key_binds(self):
        if keyboard.is_pressed(self.key_reload_config):
            return True

        if keyboard.is_pressed(self.key_toggle_aim):
            self.aim_state = not self.aim_state
            print("AIM: " + str(self.aim_state))
            sleep(self.delay)

        if keyboard.is_pressed(self.key_toggle_recoil):
            self.recoil_state = not self.recoil_state
            self.recoil_offset = 0
            print("RECOIL: " + str(self.recoil_state))
            sleep(self.delay)
        
        if keyboard.is_pressed(self.key_exit):
            print("Exiting")
            exit(1)
        return False

    def reload_config(self):
        self.config.read_config()

    def get_aim_state(self):
        if self.aim_state and (wapi.GetAsyncKeyState(0x01) < 0 or wapi.GetAsyncKeyState(0x02) < 0):
            return True
        return False

    def get_trigger_state(self):
        if wapi.GetAsyncKeyState(self.key_trigger) < 0:
            return True
        return False

    @staticmethod
    def print_attributes(obj):
        attributes = vars(obj)
        for attribute, value in attributes.items():
            print(f'{attribute}: {value}')
