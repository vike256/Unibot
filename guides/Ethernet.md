# Unibot ethernet guide

## Download and install Arduino IDE
[Guide.md | Download and install Arduino IDE](Guide.md#download-and-install-arduino-ide)

## Ethernet setup
- Connect an ethernet cable from the board to the PC
- Go to `Control Panel\Network and Internet\Network Connections`
- Go to your main network's properties
- Go to `Sharing`
- Turn on `Allow other network users to connect through this computer's Internet connection`
- Select your board's ethernet from the dropdown
- Click `OK`

## Set ethernet shield IP
- Go to `Windows Settings > Network & internet > Ethernet`
- Find your ethernet shield's settings
- Set IP assignment to manual for IPv4
- Set IP address to the same range as your main connection (`x.x.x.y`, replace the y with any value that is not being used)
- Set subnet mask to the same as your main connection (Command `ipconfig` in terminal might help to find that)
- Click `OK`

## Upload ino file
- Connect the board to the PC
- Open `Unibot/src/ethernet/ethernet.ino` with Arduino IDE
- Go to `Tools > Board` and select the board you are using 
- Go to `Tools > Port` and select the correct port
- In `ethernet.ino` change `mac` to your ethernet shield's MAC address
- Change `ip` to the same range as your main connection (`x.x.x.y`, replace the `y` with any value that is not being used) (NOTE: This should be different from the IP in [Set ethernet shield IP](#set-ethernet-shield-ip))
- Click `Upload`

## Configure config
[Guide.md | Configure config](Guide.md#configure-config)

## Run Unibot
[Guide.md | Run Unibot](Guide.md#run-unibot)