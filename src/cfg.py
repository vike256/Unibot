import configparser
import numpy as np
import dxcam
import os


configFile = configparser.ConfigParser()
runtime = 0

# Network
ip = None
port = None
client = None
com_type = None
com_port = None
board = None

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
recoil_offset = 0

# Keybinds
key_reload_config = None
key_toggle_aim = None
key_toggle_recoil = None

# Debug
debug = False
display_mode = None

# Booleans
toggleAim = False
toggleRecoil = False



def read_config():
    global configFile

    # Network
    global ip
    global port
    global client
    global com_type
    global com_port

    # Screen
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

    # Aim
    global aim_type
    global offset
    global smooth
    global speed
    global xMultiplier
    global head_height

    # Recoil
    global recoil_mode
    global max_offset
    global recoilX
    global recoilY
    global recoil_recover

    # Keybinds
    global key_reload_config
    global key_toggle_aim
    global key_toggle_recoil

    # Debug
    global debug
    global display_mode

    # Booleans
    global toggleAim
    global toggleRecoil

    # Set all cheats off everytime config is read
    toggleAim = False
    toggleRecoil = False

    # Get config path and read it
    path = os.path.join(os.path.dirname(__file__), '../config.ini')
    configFile.read(path)


    # Get communication settings
    ip = configFile.get('communication', 'ip')
    port = int(configFile.get('communication', 'port'))

    value = configFile.get('communication', 'type').lower()
    com_type_list = ['none', 'driver', 'serial', 'socket']
    if value in com_type_list:
        com_type = value
    else:
        print('ERROR: Invalid com_type value')
        exit(1)

    com_port = configFile.get('communication', 'com_port')


    # Get screen settings
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


    # Get aim settings
    value = configFile.get('aim', 'type').lower()
    aim_type_list = ['pixel', 'shape']
    if value in aim_type_list:
        aim_type = value
    else:
        print('ERROR: Invalid aim_type value')
        exit(1)

    offset = int(configFile.get('aim', 'offset'))

    value = float(configFile.get('aim', 'smooth'))
    if 0 < value <= 1:
        smooth = value
    else:
        print('ERROR: Invalid smooth value')
        exit(1)

    speed = float(configFile.get('aim', 'speed'))
    xMultiplier = float(configFile.get('aim', 'xMultiplier'))

    value = float(configFile.get('aim', 'head_height'))
    if 0 <= value <= 1:
        head_height = value
    else:
        print('ERROR: Invalid head_height value')
        exit(1)


    # Get recoil settings
    value = configFile.get('recoil', 'mode').lower()
    recoil_mode_list = ['move', 'offset']
    if value in recoil_mode_list:
        recoil_mode = value
    else:
        print('ERROR: Invalid recoil_mode value')
        exit(1)

    max_offset = int(configFile.get('recoil', 'max_offset'))
    recoilX = float(configFile.get('recoil', 'recoilX'))
    recoilY = float(configFile.get('recoil', 'recoilY'))
    recoil_recover = float(configFile.get('recoil', 'recover'))
    

    # Get keybind settings
    key_reload_config = configFile.get('keybinds', 'key_reload_config')
    key_toggle_aim = configFile.get('keybinds', 'key_toggle_aim')
    key_toggle_recoil = configFile.get('keybinds', 'key_toggle_recoil')


    # Get debug settings
    if configFile.get('debug', 'enabled').lower() == 'true':
        debug = True
        value = configFile.get('debug', 'display_mode').lower()
        display_mode_list = ['game', 'mask']
        if value in display_mode_list:
            display_mode = value
        else:
            print('ERROR: Invalid display_mode value')
            exit(1)


    # Setup dxcam
    if not cam:
        cam = dxcam.create(output_color="BGR")
    region_left = (resolution[0] - fov) // 2
    region_top = (resolution[1] - fov) // 2
    center = (fov // 2, fov // 2)

    str_communication = f'\n- Type: {com_type}'

    if type == 'serial':
        str_communication += f'\n- COM port: {com_port}'
    elif type == 'socket':
        str_communication += f'\n- Network: {ip}:{port}'

    str_screen = f'\n- Color: {lower_color}-{upper_color} \n- FOV: {fov} \n- Resolution: {resolution[0]}x{resolution[1]} \n- FPS: {fps_value}'

    str_aim = f'\n- Offset: {offset} \n- Smooth: {smooth} \n- Speed: {speed} \n- xMultiplier: {xMultiplier}'''

    str_recoil = f'\n- Mode: {recoil_mode}'

    if recoil_mode == 'move':
        str_recoil += f'\n- Recoil: ({recoilX}, {recoilY})'
    elif recoil_mode == 'offset':
        str_recoil += f'\n- RecoilY: {recoilY} \n- Max Offset: {max_offset} \n- Recover: {recoil_recover}'

    str_debug = f'\n- Enabled: {debug}'
    
    if debug:
        str_debug += f'\n- Display mode: {display_mode}'

    print(f'Config: \nCOMMUNICATION {str_communication} \nSCREEN {str_screen} \nAIM {str_aim} \nRECOIL {str_recoil} \nDEBUG {str_debug} \nConfig read, all cheats defaulted to off.')

read_config()