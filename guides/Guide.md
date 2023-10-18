# Guide for Unibot

## Follow these guides to setup Unibot
[Ethernet](Ethernet.md)  
[Serial](Serial.md)  
[Wi-Fi](WiFi.md)  
[WinApi](WinApi.md)  

## Hotkeys
- F1: Reload config
- F2: Toggle aim
- F3: Toggle recoil
- Mouse5: Triggerbot

## Download and install Arduino IDE
DO THIS STEP ONLY IF YOU ARE USING EXTERNAL HARDWARE TO SEND MOUSE INPUT
- Go to https://www.arduino.cc/en/software
- Download and install the latest Arduino IDE version (2.x.x)
- If you are using Raspberry Pi Pico W: [Guide to use setup Raspberry Pi Pico W for Arduino IDE](RaspberryPiPicoW_Setup.md)

## Config
### Communication
- `type` is the communication type used.  
    - `none` to use WinApi calls for mouse input instead of hardware  
    - `serial` to use serial communication  
        - `com_port` is the COM port of your board
    - `socket` to use ethernet or Wi-Fi  
        - `ip` is the IP of your board
        - `port` is the port of your board

### Screen
- `upper_color` and `lower_color` are used for target detection 
    - See [Guide for finding HSV upper and lower color](HSV_Guide.md)  
- `fov` sets the width and height of the target detection area that is in the center of the screen  
- `resolution` is your game resolution.  
- `fps` is the target fps  
    - Unibot will not loop more than `fps` times per second  
    - This setting should not be higher than your monitor's refresh rate  
    - Lower this if the aimbot is jittery

### Aim
- `offset` sets the aimbot to aim _x_ pixels below the target  
- `smooth` sets the value used for calculating smoothess for the aimbot 
    - Should be in range `0 < x <= 1`
    - Higher value = less smoothing. 
- `speed` adjusts the mouse movement amount
- `xMultiplier` divides the y-axis movement amount
- `head_height` determines the vertical position of the aim
    - Should be in range `0 < x < 1`
    - Value `0.5` aims at the center of the target

### Recoil
- `mode` is the recoil method used
    - `move` for games where the bullet always hits the center of the screen
        - `recoilX` and `recoilY` set the move speed
    - `offset` for games where the recoil goes above crosshair
        - `recoilY` increases aiming offset when left button is pressed
        - `max_offset` is the maximum offset the recoil can have
        - `recover` sets how fast the recoil recovers when left button is not pressed


## Run Unibot
Requirements:
- Python  
https://www.python.org/downloads/
- pip  
https://pip.pypa.io/en/stable/installation/

To setup Unibot:
- Open `Unibot` folder in terminal
- Use command `pip install -r requirements.txt`

To run Unibot:
- Run `Unibot/src/main.py` with Python