import keyboard
from time import sleep

import cfg


delay = 0.2


def check():
    if keyboard.is_pressed(cfg.key_reload_config):
        config = cfg.read_config()
        sleep(delay)

    if keyboard.is_pressed(cfg.key_toggle_aim):
        cfg.toggleAim = not cfg.toggleAim
        print("AIM: " + str(cfg.toggleAim))
        sleep(delay)

    if keyboard.is_pressed(cfg.key_toggle_recoil):
        cfg.toggleRecoil = not cfg.toggleRecoil
        cfg.recoil_offset = 0
        print("RECOIL: " + str(cfg.toggleRecoil))
        sleep(delay)
    
    if keyboard.is_pressed(cfg.key_exit):
        print("Exiting")
        exit(1)