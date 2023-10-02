import socket
import cv2
import numpy as np
import keyboard
import time
import keybinds
import mouse
import screen
import setup
import win32api as wapi


def main():
    startTime = time.time()
    previousX = 0
    previousY = 0
    config = setup.read_config()

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    print("Connecting...")

    try:
        client.connect((config['ip'], config['port']))
        print("Connected")

        while True:
            deltaTime = time.time() - startTime
            startTime = time.time()
            deltaTime *= 1000
            x = 0
            y = 0
            
            config = keybinds.check(config)
            
            contours, thresh = screen.screengrab(config['sct'], config['screenshot'], config['lower_color'], config['upper_color'])

            # AIM if mouse left or right down
            if config['toggleAim'] and (wapi.GetAsyncKeyState(0x01) < 0 or wapi.GetAsyncKeyState(0x02) < 0):
                if len(contours) != 0:
                    closest_contour = screen.get_closest_target(contours, config['center'])
                
                    if closest_contour is not None:
                        cX, cY = closest_contour

                        x = -(config['center'][0] - cX) if cX < config['center'][0] else cX - config['center'][0]
                        y = -(config['center'][1] - cY) if cY < config['center'][1] else cY - config['center'][1]
                        x *= config['speed']
                        y *= config['speed'] / config['xMultiplier']
                        y += config['offset']

                        #Smoothing
                        x = previousX + config['smooth'] * (x - previousX)
                        y = previousY + config['smooth'] * (y - previousY)
                        previousX = x
                        previousY = y

            # RECOIL
            if config['toggleRecoil'] and wapi.GetAsyncKeyState(0x01) < 0 and deltaTime != 0:
                x += config['recoilX'] / deltaTime
                y += config['recoilY'] / deltaTime

            if config ['toggleTriggerbot']:
                value = 8
                if thresh[config['center'][0] + value, config['center'][1]] == 255:
                    if thresh[config['center'][0] - value, config['center'][1]] == 255:
                        if thresh[config['center'][0], config['center'][1] - value] == 255:
                            mouse.click(client)

            mouse.move(x, y, client)
            
            time.sleep(0.001)     

    except KeyboardInterrupt:
        pass

    except TimeoutError:
        print("Connection attempt failed")

    finally:
        client.close()
        print("Closed")

if __name__=="__main__":
    main()