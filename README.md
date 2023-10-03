Colorbot/aimbot that works for both Raspberry Pi Pico W and Arduino Leonardo.  
The board acts as a mouse and gets instructions from host machine. 

Hardware required:  
Arduino version:  
- Arduino Leonardo R3
- Ethernet Shield
- USB to Ethernet adapter (Optional)  

Raspberry version:   
- Raspberry Pi Pico W
  
Software required:
- Arduino IDE

Raspberry Pi Pico W instructions: 
- Add below link to Arduino IDE > File > Preferences > Additional boards manger URLs  
    https://github.com/earlephilhower/arduino-pico/releases/download/global/package_rp2040_index.json
- Add below package to Arduino IDE > Tools > Board > Boards Manager  
    Raspberry Pi Pico/RP2040 by Earle F. Philhower, III
