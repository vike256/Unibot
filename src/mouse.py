import time
import numpy as np
import cfg

if cfg.com_type == 'none':
    import ctypes


def move(x, y):
    x = int(np.floor(x + 0.5))
    y = int(np.floor(y + 0.5))

    if x != 0 or y != 0:
        command = f"M{x},{y}\r"

        if cfg.com_type == 'socket':
            cfg.client.sendall(command.encode())
        elif cfg.com_type == 'serial':
            cfg.board.write(command.encode())
        elif cfg.com_type == 'none':
            ctypes.windll.user32.mouse_event(0x0001, x, y, 0, 0)

        print(f"Move({x}, {y})", end='')
        if cfg.com_type == 'socket':
            waitForResponse()
        else:
            print('')


def click():
    command = "C\r"
    
    if cfg.com_type == 'socket':
        cfg.client.sendall(command.encode())
    elif cfg.com_type == 'serial':
        cfg.board.write(command.encode())
    elif cfg.com_type == 'none':
        ctypes.windll.user32.mouse_event(0x0002, 0, 0, 0, 0)
        time.sleep((np.random.randint(40) + 40) // 1000)
        ctypes.windll.user32.mouse_event(0x0004, 0, 0, 0, 0)

    print("Click", end='')
    if cfg.com_type == 'socket':
        waitForResponse()
    else:
        print('')


def press():
    command = "B1\r"

    if cfg.com_type == 'socket':
        cfg.client.sendall(command.encode())
    elif cfg.com_type == 'serial':
        cfg.board.write(command.encode())
    elif cfg.com_type == 'none':
        ctypes.windll.user32.mouse_event(0x0002, 0, 0, 0, 0)

    print("LButton down", end='')
    if cfg.com_type == 'socket':
            waitForResponse()
    else:
        print('')


def release():
    command = "B0\r"
    if cfg.comtype == 'socket':
        cfg.client.sendall(command.encode())
    elif cfg.com_type == 'serial':
        cfg.board.write(command.encode())
    elif cfg.com_type == 'none':
        ctypes.windll.user32.mouse_event(0x0004, 0, 0, 0, 0)


    print("LButton up", end='')
    if cfg.com_type == 'socket':
            waitForResponse()
    else:
        print('')


def waitForResponse():
    start = time.time()
    ack = cfg.client.recv(4).decode()
    if ack == "a\r":
        print(f" (ACK {np.floor((time.time() - start) * 1000 + 0.5):g} ms)") # Print latency in milliseconds