import keyboard
from time import sleep

import cfg


delay = 0.2


def check():
    if keyboard.is_pressed('F1'):
        config = cfg.read_config()
        sleep(delay)

    if keyboard.is_pressed('F2'):
        cfg.toggleAim = not cfg.toggleAim
        print("AIM: " + str(cfg.toggleAim))
        sleep(delay)

    if keyboard.is_pressed('F3'):
        cfg.toggleRecoil = not cfg.toggleRecoil
        print("RECOIL: " + str(cfg.toggleRecoil))
        sleep(delay)