import configparser
import numpy as np
import dxcam


configFile = configparser.ConfigParser()

# Network
ip = None
port = None
client = None
com_type = None
com_port = None
board = None

# Aim
offset = None
smooth = None
speed = None
xMultiplier = None
recoilX = None
recoilY = None

# Screen
cam = None
center = None
fov = None
region = None
resolution = None
upper_color = None
lower_color = None
monitor_hz_wait = None

# Booleans
toggleAim = False
toggleRecoil = False


def read_config():
    global configFile
    global ip
    global port
    global client
    global com_type
    global com_port
    global offset
    global smooth
    global speed
    global xMultiplier
    global recoilX
    global recoilY
    global cam
    global center
    global fov
    global region
    global resolution
    global upper_color
    global lower_color
    global monitor_hz_wait
    global toggleAim
    global toggleRecoil

    toggleAim = False
    toggleRecoil = False

    configFile.read("config.ini")
    ip = configFile.get('communication', 'ip')
    port = int(configFile.get('communication', 'port'))
    com_type = configFile.get('communication', 'type')
    com_port = configFile.get('communication', 'com_port')

    upper_color = configFile.get('screen', 'upper_color').split(',')
    lower_color = configFile.get('screen', 'lower_color').split(',')
    for i in range(0, 3):
        upper_color[i] = int(upper_color[i].strip())
    for i in range(0, 3):
        lower_color[i] = int(lower_color[i].strip())
    upper_color = np.array(upper_color)
    lower_color = np.array(lower_color)

    resolution = configFile.get('screen', 'resolution').split('x')
    resolution = (int(resolution[0]), int(resolution[1]))

    fov = int(configFile.get('screen', 'fov'))
    monitor_hz_wait = int(np.floor(1000 / int(configFile.get('screen', 'monitor_hz')) + 1))
    offset = int(configFile.get('aim', 'offset'))
    smooth = float(configFile.get('aim', 'smooth'))
    speed = float(configFile.get('aim', 'speed'))
    xMultiplier = float(configFile.get('aim', 'xMultiplier'))
    recoilX = float(configFile.get('recoil', 'recoilX'))
    recoilY = float(configFile.get('recoil', 'recoilY'))

    if not cam:
        cam = dxcam.create(output_color="BGR")
    left = (resolution[0] - fov) // 2
    top = (resolution[1] - fov) // 2
    right = left + fov
    bottom = top + fov
    region = (left, top, right, bottom)
    center = (fov // 2, fov // 2)

    print(f"""Config: 
- Network: {ip}:{port}
- Communication: {com_type}
- Color: LOWER: {lower_color}, UPPER: {upper_color}
- FOV: {fov}
- Offset: {offset}
- Smooth: {smooth}
- Speed: {speed}
- xMultiplier: {xMultiplier}
- Recoil: ({recoilX}, {recoilY})
Config read, all cheats defaulted to off.""")

read_config()