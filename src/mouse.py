import time
import numpy as np

import cfg


def move(x, y):
    x = np.floor(x + 0.5)
    y = np.floor(y + 0.5)

    if x != 0 or y != 0:
        # Mouse.Move takes char (8 bits) as input
        # 8bit signed value range is from -128 to 127
        max = 127
        if abs(x) > abs(max):
            x = x/abs(x) * abs(max)
        if abs(y) > abs(max):
            y = y/abs(y) * abs(max)

        command = f"M{x},{y}\r"
        cfg.client.sendall(command.encode())
        print(f"SENT: Move({x}, {y})", end='')
        waitForResponse()


def click():
    command = "C\r"
    cfg.client.sendall(command.encode())
    print("SENT: Click", end='')
    waitForResponse()


def press():
    command = "B1\r"
    cfg.client.sendall(command.encode())
    print("SENT: LButton down", end='')
    waitForResponse()


def release():
    command = "B0\r"
    cfg.client.sendall(command.encode())
    print("SENT: LButton up", end='')
    waitForResponse()


def waitForResponse():
    start = time.time()
    ack = cfg.client.recv(4).decode()
    if ack == "a\r":
        print(f" (ACK {np.floor((time.time() - start) * 1000 + 0.5):g} ms)") # Print latency in milliseconds