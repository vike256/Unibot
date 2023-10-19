import cv2
import time
import numpy as np
import win32api as wapi

import cfg
import keybinds
import mouse
import screen


def main():
    if cfg.com_type == 'socket':
        import socket
        cfg.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    elif cfg.com_type == 'serial':
        import serial
        cfg.board = serial.Serial(cfg.com_port, 115200)

    start_time = time.time()
    previousX = 0
    previousY = 0

    print("Connecting...")

    try:
        if cfg.com_type == 'socket':
            cfg.client.connect((cfg.ip, cfg.port))
        print("Connected")

        while True:
            delta_time = (time.time() - start_time) * 1000
            start_time = time.time()
            x = 0
            y = 0
            
            keybinds.check()

            target, trigger = screen.get_target()

            # AIM if mouse left or right down
            if cfg.toggleAim and (wapi.GetAsyncKeyState(0x01) < 0 or wapi.GetAsyncKeyState(0x02) < 0):
                if target is not None:
                    cX, cY = target

                    distanceX = cX - cfg.center[0]
                    distanceY = cY - cfg.center[1]
                    x = distanceX * cfg.speed
                    y = distanceY * cfg.speed / cfg.xMultiplier
                    y += cfg.offset

                    #Smoothing
                    x = previousX + cfg.smooth * (x - previousX)
                    y = previousY + cfg.smooth * (y - previousY)
                    previousX = x
                    previousY = y

            # RECOIL
            if cfg.toggleRecoil:
                if delta_time != 0:
                    if cfg.recoil_mode == 'move' and wapi.GetAsyncKeyState(0x01) < 0:
                        x += cfg.recoilX / delta_time
                        y += cfg.recoilY / delta_time
                    elif cfg.recoil_mode == 'offset':
                        if wapi.GetAsyncKeyState(0x01) < 0:
                            if cfg.recoil_offset < cfg.max_offset:
                                cfg.recoil_offset += cfg.recoilY / delta_time
                                if cfg.recoil_offset > cfg.max_offset:
                                    cfg.recoil_offset = cfg.max_offset
                        else:
                            if cfg.recoil_offset > 0:
                                cfg.recoil_offset -= cfg.recoil_recover / delta_time
                                if cfg.recoil_offset < 0:
                                    cfg.recoil_offset = 0


            # TRIGGER
            if wapi.GetAsyncKeyState(cfg.key_trigger) < 0 and trigger:
                mouse.click()

            mouse.move(x, y)
            
            time_spent = (time.time() - start_time) * 1000
            if time_spent < cfg.fps:
                time.sleep((cfg.fps - time_spent) / 1000)
            
            cfg.runtime += delta_time

    except KeyboardInterrupt:
        pass

    except TimeoutError:
        print("Connection attempt failed")

    finally:
        if cfg.com_type == 'socket':
            cfg.client.close()
        print("Closed")


if __name__=="__main__":
    main()