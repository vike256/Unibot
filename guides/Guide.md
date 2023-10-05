# Guide for Unibot

## Hotkeys
- F1: Reload config
- F2: Toggle aim
- F3: Toggle recoil
- Mouse5: Triggerbot

## Download and install Arduino IDE
DO THIS STEP ONLY IF YOU ARE USING EXTERNAL HARDWARE TO SEND MOUSE INPUT
- Go to https://www.arduino.cc/en/software
- Download and install the latest Arduino IDE version (2.x.x)

## Configure config
### Communication
- `type` is the communication type used.  
    - `none` to use WinAPi calls for mouse input instead of hardware  
    - `serial` to use serial communication  
        - `com_port` is the COM port of your board
    - `socket` to use ethernet or Wi-Fi  
        - `ip` is the IP of your board
        - `port` is the port of your board

### Screen
- `upper_color` and `lower_color` are used for target detection. 
    - You can find the needed HSV values with https://github.com/hariangr/HsvRangeTool  
- `fov` sets the width and height of the target detection area that is in the center of the screen  
- `resolution` is your game resolution.  
- `monitor_hz` is your monitor's refresh rate.  

### Aim
- `offset` sets the aimbot to aim _x_ pixels below the target  
- `smooth` sets the value used for calculating smoothess for the aimbot 
    - Higher value = less smoothing. 
    - Should be in range `0 < smooth <= 1`

### Recoil
- `recoilX` and `recoilY` are used to negate the recoil in some FPS games.

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
- Make sure that `config.ini` is set properly
- Run `run.bat`