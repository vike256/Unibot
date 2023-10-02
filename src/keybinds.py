import keyboard
from time import sleep
import setup

delay = 0.3

def check(config):
    if keyboard.is_pressed('F1'):
        config = setup.read_config()
        sleep(delay)

    if keyboard.is_pressed('F2'):
        config['toggleAim'] = not config['toggleAim']
        print("AIM: " + str(config['toggleAim']))
        sleep(delay)

    if keyboard.is_pressed('F3'):
        config['toggleRecoil'] = not config['toggleRecoil']
        print("RECOIL: " + str(config['toggleRecoil']))
        sleep(delay)

    if keyboard.is_pressed('F4'):
        config['toggleTriggerbot'] = not config['toggleTriggerbot']
        print("TRIGGER: " + str(config['toggleTriggerbot']))
        sleep(delay)

    return config