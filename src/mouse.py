import time
import numpy as np
import cfg

if cfg.com_type == 'none':
    import ctypes
elif cfg.com_type == 'driver':
    import interception
    interception.auto_capture_devices(mouse=True)

remainderX = 0
remainderY = 0

symbols = '-,0123456789'
code    = 'UNIBOTCYPHER'

def encrypt_command(command):
    if cfg.encrypt:
        encrypted_command = ""
        for char in command:
            if char in symbols:
                index = symbols.index(char)
                encrypted_command += code[index]
            else:
                encrypted_command += char  # Keep non-symbol characters unchanged
        return encrypted_command
    else:
        return command

def move(x, y):
    global remainderX
    global remainderY

    x += remainderX
    y += remainderY

    remainderX, remainderY = (x, y)

    x = int(np.floor(x + 0.5))
    y = int(np.floor(y + 0.5))

    remainderX -= x
    remainderY -= y

    if x != 0 or y != 0:
        if cfg.com_type == 'socket':
            command = encrypt_command(f'M{x},{y}\r')
            cfg.client.sendall(command.encode())
        elif cfg.com_type == 'serial':
            command = encrypt_command(f'M{x},{y}\r')
            cfg.board.write(command.encode())
        elif cfg.com_type == 'driver':
            interception.move_relative(x, y)
        elif cfg.com_type == 'none':
            ctypes.windll.user32.mouse_event(0x0001, x, y, 0, 0)

        if cfg.com_type == 'socket' or cfg.com_type == 'serial':
            print(f'Sent: {command}')
            print(getResponse())
        else:
            print(f'M({x}, {y})')


def click():
    if cfg.com_type == 'socket':
        cfg.client.sendall('C\r'.encode())
    elif cfg.com_type == 'serial':
        cfg.board.write('C\r'.encode())
    elif cfg.com_type == 'driver':
        randomDelay = (np.random.randint(40) + 40) / 1000
        interception.mouse_down('left')
        time.sleep(randomDelay)
        interception.mouse_up('left')
    elif cfg.com_type == 'none':
        randomDelay = (np.random.randint(40) + 40) / 1000
        ctypes.windll.user32.mouse_event(0x0002, 0, 0, 0, 0)
        time.sleep(randomDelay)
        ctypes.windll.user32.mouse_event(0x0004, 0, 0, 0, 0)

    if cfg.com_type == 'socket' or cfg.com_type == 'serial':
            print(getResponse())
    else:
        print(f'Click ({randomDelay * 1000:g} ms)')


def getResponse():
    receive = ''
    if cfg.com_type == 'socket':
        receive = f'Socket: {cfg.client.recv(4).decode()}'
    elif cfg.com_type == 'serial':
        while True:
            receive = cfg.board.readline().decode('utf-8').strip()
            if len(receive) > 0:
                receive = f'Serial: {receive}'
                break
    return receive