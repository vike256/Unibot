import cv2
import time
import numpy as np
import win32api as wapi

from mouse import Mouse
from screen import Screen
from utils import Utils


def main():
    while True:
        start_time = time.time()
        previousX = 0
        previousY = 0

        utils = Utils()
        config = utils.config
        mouse = Mouse(config)
        screen = Screen(config)

        print('ON')

        while True:
            delta_time = (time.time() - start_time) * 1000
            start_time = time.time()
            x = 0
            y = 0
            
            reload = utils.check_keybinds()
            if reload:
                break

            target, trigger = screen.get_target()

            # AIM if mouse left or right down
            if utils.get_aim_state():
                if target is not None:
                    x = target[0] - screen.fov_center[0]
                    y = target[1] - screen.fov_center[1]

                    x *= config.speed
                    y *= config.speed / config.x_multiplier

                    # Smoothing
                    x = previousX + config.smooth * (x - previousX)
                    y = previousY + config.smooth * (y - previousY)
                    previousX = x
                    previousY = y

            # RECOIL
            if utils.recoil_state:
                if delta_time != 0:
                    if config.recoil_mode == 'move' and wapi.GetAsyncKeyState(0x01) < 0:
                        x += config.recoil_x / delta_time
                        y += config.recoil_y / delta_time
                    elif config.recoil_mode == 'offset':
                        if wapi.GetAsyncKeyState(0x01) < 0:
                            if config.recoil_offset < config.max_offset:
                                config.recoil_offset += config.recoilY / delta_time
                                if config.recoil_offset > config.max_offset:
                                    config.recoil_offset = config.max_offset
                        else:
                            if config.recoil_offset > 0:
                                config.recoil_offset -= config.recoil_recover / delta_time
                                if config.recoil_offset < 0:
                                    config.recoil_offset = 0


            # TRIGGER
            if utils.get_trigger_state() and trigger:
                mouse.click()

            mouse.move(x, y)
            
            time_spent = (time.time() - start_time) * 1000
            if time_spent < screen.fps:
                time.sleep((screen.fps - time_spent) / 1000)
        
        del utils
        del config
        del mouse
        del screen
        print('Reloading')


if __name__=="__main__":
    main()