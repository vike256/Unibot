# Unibot Wi-Fi guide

## Wi-Fi setup
Setup Windows Mobile hotspot like this:  
- Set your own Wi-Fi name and password
- Set band to 2.4 GHz  
![Settings preview](https://i.imgur.com/Ghh0aka.png)

## Control Panel setup
Set up sharing with your main connection:
- Turn on Windows Mobile hotspot
- Go to `Control Panel\Network and Internet\Network Connections`
- Go to your main network's properties
- Go to `Sharing`
- Turn on `Allow other network users to connect through this computer's Internet connection`
- Select your Wi-Fi hotspot from the dropdown
- Click `OK`  
![Settings preview](https://i.imgur.com/kHX00BN.png)

## Configure and upload ino file to board
- Connect the board to the PC
- Open `Unibot/src/wifi/wifi.ino` with Arduino IDE
- Go to `Tools > Board` and select the board you are using 
- Go to `Tools > Port` and select the correct port
- In `wifi.ino` change variables `ssid` and `password` to match your Wi-Fi name and password
- Click `Upload`

## Check board IP
- Turn on Mobile hotspot in Windows (Also check [Control Panel setup](#control-panel-setup))
- Connect the board to the PC
- Open Mobile hotspot settings
- You should see the board and its IP in the connected devices