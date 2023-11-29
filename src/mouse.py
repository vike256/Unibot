"""
    Consider donating: https://github.com/vike256#donations

    Unibot, an open-source colorbot.
    Copyright (C) 2023 vike256

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""
import time
import numpy as np
import win32api
import win32con
import interception
import serial
import socket
import threading


class Mouse:
    def __init__(self, config):
        self.com_type = config.com_type
        self.click_thread = threading.Thread(target=self.send_click)
        self.last_click_time = time.time()
        self.target_cps = config.target_cps

        # Create a lock, so we can use it to not send multiple mouse clicks at the same time
        self.lock = threading.Lock()

        self.symbols = '-,0123456789'
        self.code = 'UNIBOTCYPHER'
        self.encrypt = config.encrypt

        self.ip = config.ip
        self.port = config.port
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        self.com_port = config.com_port
        self.board = None

        # Create variables to store the remainder decimal points for our mouse move function
        self.remainder_x = 0
        self.remainder_y = 0
        
        match self.com_type:
            case 'socket':
                print(f'Connecting to {self.ip}:{self.port}...')
                try:
                    self.client.connect((self.ip, self.port))
                    print('Socket connected')
                except Exception as e:
                    print(f'ERROR: Could not connect (Socket). {e}')
                    self.close_connection()
            case 'serial':
                try:
                    self.board = serial.Serial(self.com_port, 115200)
                    print('Serial connected')
                except Exception as e:
                    print(f'ERROR: Could not connect (Serial). {e}')
                    self.close_connection()
            case 'driver':
                interception.auto_capture_devices(mouse=True)

    def __del__(self):
        self.close_connection()

    def close_connection(self):
        if self.com_type == 'socket':
            if self.client is not None:
                self.client.close()
        elif self.com_type == 'serial':
            if self.board is not None:
                self.board.close()

    def encrypt_command(self, command):
        if self.encrypt:
            encrypted_command = ""
            for char in command:
                if char in self.symbols:
                    index = self.symbols.index(char)
                    encrypted_command += self.code[index]
                else:
                    encrypted_command += char  # Keep non-symbol characters unchanged
            return encrypted_command
        else:
            return command

    def move(self, x, y):
        # Add the remainder from the previous calculation
        x += self.remainder_x
        y += self.remainder_y

        # Round x and y, and calculate the new remainder
        self.remainder_x = x
        self.remainder_y = y
        x = int(x)
        y = int(y)
        self.remainder_x -= x
        self.remainder_y -= y

        if x != 0 or y != 0:
            match self.com_type:
                case 'socket' | 'serial':
                    self.send_command(f'M{x},{y}\r')
                case 'driver':
                    interception.move_relative(x, y)
                    print(f'M({x}, {y})')
                case 'none':
                    win32api.mouse_event(win32con.MOUSEEVENTF_MOVE, x, y, 0, 0)
                    print(f'M({x}, {y})')

    def click(self, delay_before_click=0):
        if (
                not self.click_thread.is_alive() and
                time.time() - self.last_click_time >= 1 / self.target_cps
        ):
            self.click_thread = threading.Thread(target=self.send_click, args=(delay_before_click,))
            self.click_thread.start()

    def send_click(self, delay_before_click=0):
        time.sleep(delay_before_click)
        self.last_click_time = time.time()
        match self.com_type:
            case 'socket' | 'serial':
                self.send_command('C\r')
            case 'driver':
                random_delay = (np.random.randint(40) + 40) / 1000
                interception.mouse_down('left')
                time.sleep(random_delay)
                interception.mouse_up('left')
                print(f'C({random_delay * 1000:g})')
            case 'none':
                random_delay = (np.random.randint(40) + 40) / 1000
                win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
                time.sleep(random_delay)
                win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)
                print(f'C({random_delay * 1000:g})')
        time.sleep((np.random.randint(10) + 25) / 1000)  # Sleep to avoid sending another click instantly after mouseup

    def send_command(self, command):
        command = self.encrypt_command(command)
        with self.lock:
            match self.com_type:
                case 'socket':
                    self.client.sendall(command.encode())
                case 'serial':
                    self.board.write(command.encode())
            print(f'Sent: {command}')
            print(f'Response from {self.com_type}: {self.get_response()}')

    def get_response(self):  # Waits for a response before sending a new instruction
        match self.com_type:
            case 'socket':
                return self.client.recv(4).decode()
            case 'serial':
                while True:
                    receive = self.board.readline().decode('utf-8').strip()
                    if len(receive) > 0:
                        return receive
