# Guide to use Raspberry Pi Pico W with Unibot (Wi-Fi version)

## Hardware needed
- Raspberry Pi Pico W
- Wi-Fi support on your PC

## Wi-Fi setup
[WiFi.md | Wi-Fi setup](WiFi.md#wi-fi-setup)

## Control Panel setup
[WiFi.md | Control Panel setup](WiFi.md#control-panel-setup)

## Install Arduino IDE and required dependencies
[WiFi.md | Download and install Arduino IDE](Guide.md#download-and-install-arduino-ide)

## Change Arduino IDE settings for Pico W
- Open Arduino IDE
- Go to `File > Preferences > Additional boards manager URLs`
- Paste this link there: `https://github.com/earlephilhower/arduino-pico/releases/download/global/package_rp2040_index.json`
- Click OK  
![Settings preview](https://i.imgur.com/aG3Mlpo.png)
- Go to `Tools > Board > Boards Manager`
- Install `Raspberry Pi Pico/RP2040 by Earle F. Philhower, III`  
![Settings preview](https://i.imgur.com/CamVwkN.png)

## Configure and upload ino file to board
[WiFi.md | Configure and upload ino file to board](WiFi.md#configure-and-upload-ino-file-to-board)

## Check board IP
[WiFi.md | Check board IP](WiFi.md#check-board-ip)

## Configure config
[Guide.md | Configure config](Guide.md#configure-config)

## Run Unibot
[Guide.md | Run Unibot](Guide.md#run-unibot)