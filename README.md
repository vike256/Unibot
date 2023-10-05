Colorbot/aimbot that works for both software and hardware. 

Showcase: https://youtube.com/watch?v=kHSEqLzd-O0  

## How to use:
1. Upload the .ino-file to the board (If you use hardware)
2. Change HSV values and communication settings in config.ini (Find HSV values with this tool: https://github.com/hariangr/HsvRangeTool)
3. Run run.bat on host pc

## Hotkeys:
- F1: Reload config
- F2: Toggle aim
- F3: Toggle recoil
- Mouse5: Triggerbot

## Input and communication methods supported + hardware tested:  
### WinApi version:  
- Uses ctypes to call mouse inputs. No hardware needed.  

### Serial version:  
Tested with:
- Arduino Leonardo R3  

### Ethernet version:  
Tested with:  
- Arduino Leonardo R3 + Ethernet Shield + USB to Ethernet adapter (Optional)  

### Wi-Fi version:   
Tested with:  
- Raspberry Pi Pico W

## Raspberry Pi Pico W setup for Arduino IDE: 
- Add below link to Arduino IDE > File > Preferences > Additional boards manager URLs  
    https://github.com/earlephilhower/arduino-pico/releases/download/global/package_rp2040_index.json
- Add below package to Arduino IDE > Tools > Board > Boards Manager  
    Raspberry Pi Pico/RP2040 by Earle F. Philhower, III

