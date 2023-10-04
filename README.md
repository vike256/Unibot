Colorbot/aimbot that works for both Raspberry Pi Pico W and Arduino Leonardo.  The board acts as a mouse and gets instructions from the host machine. 

Showcase: https://youtube.com/watch?v=kHSEqLzd-O0  

## How to use:
1. Upload the .ino-file to the board
2. Change HSV values and network settings in config.ini
3. Run main.py on host pc

## Hotkeys:
- F1: Reload config
- F2: Toggle aim
- F3: Toggle recoil
- F4: Toggle triggerbot

## Hardware required:  
### Arduino version:  
- Arduino Leonardo R3
- Ethernet Shield
- USB to Ethernet adapter (Optional)  

### Raspberry version:   
- Raspberry Pi Pico W
  
## Software required:
- Arduino IDE

## Raspberry Pi Pico W setup for Arduino IDE: 
- Add below link to Arduino IDE > File > Preferences > Additional boards manger URLs  
    https://github.com/earlephilhower/arduino-pico/releases/download/global/package_rp2040_index.json
- Add below package to Arduino IDE > Tools > Board > Boards Manager  
    Raspberry Pi Pico/RP2040 by Earle F. Philhower, III

