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

    startTime = time.time()
    previousX = 0
    previousY = 0

    print("Connecting...")

    try:
        if cfg.com_type == 'socket':
            cfg.client.connect((cfg.ip, cfg.port))
        print("Connected")

        while True:
            deltaTime = time.time() - startTime
            startTime = time.time()
            deltaTime *= 1000
            x = 0
            y = 0
            
            keybinds.check()

            target = screen.get_target()

            # AIM if mouse left or right down
            if cfg.toggleAim and (wapi.GetAsyncKeyState(0x01) < 0 or wapi.GetAsyncKeyState(0x02) < 0):
                if target is not None:
                    cX, cY = target

                    x = -(cfg.center[0] - cX) if cX < cfg.center[0] else cX - cfg.center[0]
                    y = -(cfg.center[1] - cY) if cY < cfg.center[1] else cY - cfg.center[1]
                    x *= cfg.speed
                    y *= cfg.speed / cfg.xMultiplier
                    y += cfg.offset

                    #Smoothing
                    x = previousX + cfg.smooth * (x - previousX)
                    y = previousY + cfg.smooth * (y - previousY)
                    previousX = x
                    previousY = y

            # RECOIL
            if cfg.toggleRecoil and wapi.GetAsyncKeyState(0x01) < 0 and deltaTime != 0:
                x += cfg.recoilX / deltaTime
                y += cfg.recoilY / deltaTime

            # TRIGGERBOT
            if wapi.GetAsyncKeyState(0x06) < 0:
                if screen.get_center():
                    mouse.click()

            mouse.move(x, y)
            
            time.sleep(0.001)     

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