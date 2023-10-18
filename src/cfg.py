import configparser
import numpy as np
import dxcam
import os


configFile = configparser.ConfigParser()
runtime = 0
recoil_offset = 0

# Network
ip = None
port = None
client = None
com_type = None
com_port = None
board = None

# Aim
aim_type = None
offset = None
smooth = None
speed = None
xMultiplier = None
head_height = None

# Recoil
recoil_mode = None
max_offset = None
recoilX = None
recoilY = None
recoil_recover = None

# Screen
cam = None
center = None
fov = None
region = None
resolution = None
upper_color = None
lower_color = None
fps = None
region_left = None
region_top = None
region_right = None
region_bottom = None

# Booleans
toggleAim = False
toggleRecoil = False

# Misc
debug = False


def read_config():
    global configFile
    global ip
    global port
    global client
    global com_type
    global com_port
    global aim_type
    global offset
    global smooth
    global speed
    global xMultiplier
    global head_height
    global recoil_mode
    global max_offset
    global recoilX
    global recoilY
    global recoil_recover
    global cam
    global center
    global fov
    global region
    global resolution
    global upper_color
    global lower_color
    global fps
    global region_left
    global region_top
    global region_right
    global region_bottom
    global toggleAim
    global toggleRecoil
    global debug

    toggleAim = False
    toggleRecoil = False

    path = os.path.join(os.path.dirname(__file__), '../config.ini')
    configFile.read(path)
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
    fps_value = int(configFile.get('screen', 'fps'))
    fps = int(np.floor(1000 / fps_value + 1))
    aim_type = configFile.get('aim', 'type')
    offset = int(configFile.get('aim', 'offset'))
    smooth = float(configFile.get('aim', 'smooth'))
    speed = float(configFile.get('aim', 'speed'))
    xMultiplier = float(configFile.get('aim', 'xMultiplier'))
    head_height = 1 / (1.0 - float(configFile.get('aim', 'head_height')))
    recoil_mode = configFile.get('recoil', 'mode')
    max_offset = int(configFile.get('recoil', 'max_offset'))
    recoilX = float(configFile.get('recoil', 'recoilX'))
    recoilY = float(configFile.get('recoil', 'recoilY'))
    recoil_recover = int(configFile.get('recoil', 'recover'))
    
    if configFile.get('misc', 'debug').lower() == 'true':
        debug = True

    if not cam:
        cam = dxcam.create(output_color="BGR")
    region_left = (resolution[0] - fov) // 2
    region_top = (resolution[1] - fov) // 2
    center = (fov // 2, fov // 2)

    str_communication = f'''
Type: {com_type}'''

    if type == 'serial':
        str_communication += f'''
COM port: {com_port}'''
    elif type == 'socket':
        str_communication += f'''
Network: {ip}:{port}'''

    str_screen = f'''
Upper color: {upper_color}
Lower color: {lower_color}
FOV: {fov}
Resolution: {resolution}
FPS: {fps_value}'''

    str_aim = f'''
Offset: {offset}
Smooth: {smooth}
Speed: {speed}
xMultiplier: {xMultiplier}'''

    str_recoil = f'''
Mode: {recoil_mode}'''

    if recoil_mode == 'move':
        str_recoil += f'''
Recoil: ({recoilX}, {recoilY})'''
    elif recoil_mode == 'offset':
        str_recoil += f'''
RecoilY: {recoilY}
Max Offset: {max_offset}
Recover: {recoil_recover}'''

    str_misc = f'''\nDebug: {debug}'''

    print(f'''Config: 
COMMUNICATION {str_communication}

SCREEN {str_screen}

AIM {str_aim}

RECOIL {str_recoil}

MISC {str_misc}

Config read, all cheats defaulted to off.''')

read_config()