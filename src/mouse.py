import time
import numpy as np

def move(x, y, client):
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

        # Raspberry checks the first character to check if the instruction is to move (M) or click (C)
        command = f"M{x},{y}\r"
        client.sendall(command.encode())
        print(f"SENT: Move({x}, {y})", end='')
        waitForResponse(client)


def click(client):
    # Raspberry checks the first character to check if the instruction is to move (M) or click (C)
    command = "C\r"
    client.sendall(command.encode())
    print("SENT: Click", end='')
    waitForResponse(client)

def press(client):
    # Raspberry checks the first character to check if the instruction is to move (M) or click (C)
    command = "B1\r"
    client.sendall(command.encode())
    print("SENT: LButton down", end='')
    waitForResponse(client)

def release(client):
    # Raspberry checks the first character to check if the instruction is to move (M) or click (C)
    command = "B0\r"
    client.sendall(command.encode())
    print("SENT: LButton up", end='')
    waitForResponse(client)


def waitForResponse(client):
    start = time.time()
    ack = client.recv(4).decode()
    if ack == "a\r":
        print(f" (ACK {np.floor((time.time() - start) * 1000 + 0.5):g} ms)") # Print latency in milliseconds