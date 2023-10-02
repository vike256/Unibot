import configparser
from mss import mss
import numpy as np

def read_config():
    configFile = configparser.ConfigParser()
    configFile.read("config.ini")
    config = {
        'toggleAim': False,
        'toggleRecoil': False,
        'toggleTriggerbot': False,
    }
    config['ip'] = configFile.get('network', 'ip')
    config['port'] = int(configFile.get('network', 'port'))

    upper_color = configFile.get('screen', 'upper_color').split(',')
    lower_color = configFile.get('screen', 'lower_color').split(',')
    for i in range(0, 3):
        upper_color[i] = int(upper_color[i].strip())
    for i in range(0, 3):
        lower_color[i] = int(lower_color[i].strip())
    config['upper_color'] = np.array(upper_color)
    config['lower_color'] = np.array(lower_color)

    config['fov'] = int(configFile.get('screen', 'fov'))
    config['offset'] = int(configFile.get('aim', 'offset'))
    config['smooth'] = float(configFile.get('aim', 'smooth'))
    config['speed'] = float(configFile.get('aim', 'speed'))
    config['xMultiplier'] = float(configFile.get('aim', 'xMultiplier'))
    config['recoilX'] = float(configFile.get('recoil', 'recoilX'))
    config['recoilY'] = float(configFile.get('recoil', 'recoilY'))

    sct, screenshot, center = setup_mss(config)
    config['sct'] = sct
    config['screenshot'] = screenshot
    config['center'] = center

    print(f"""Config: 
- Network: {config['ip']}:{config['port']}
- Color: LOWER: {config['lower_color']}, UPPER: {config['upper_color']}
- FOV: {config['fov']}
- Offset: {config['offset']}
- Smooth: {config['smooth']}
- Speed: {config['speed']}
- xMultiplier: {config['xMultiplier']}
- Recoil: ({config['recoilX']}, {config['recoilY']})
Config read, all cheats defaulted to off.""")
    return config


def setup_mss(config):
    sct = mss()
    screenshot = sct.monitors[1]
    screenshot['left'] = int((screenshot['width'] / 2) - (config['fov'] / 2))
    screenshot['top'] = int((screenshot['height'] / 2) - (config['fov'] / 2))
    screenshot['width'] = config['fov']
    screenshot['height'] = config['fov']
    center = (screenshot['width'] // 2, screenshot['height'] // 2)
    return sct, screenshot, center