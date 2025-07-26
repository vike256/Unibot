"""
    Unibot, an open-source colorbot.
    Copyright (C) 2025 vike256

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
from .base_microcontroller_mouse import BaseMicrocontrollerMouse
import numpy as np
import socket
import time


class MicrocontrollerSocketMouse(BaseMicrocontrollerMouse):
    def __init__(self, config):
        super().__init__(config)
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connect_to_board()
        

    def connect_to_board(self):
        print(f'Connecting to {self.cfg.microcontroller_ip}:{self.cfg.microcontroller_port}...')
        try:
            self.client.connect((self.cfg.microcontroller_ip, self.cfg.microcontroller_port))
            print('Socket connected')
        except Exception as e:
            print(f'ERROR: Could not connect (Socket). {e}')
            self.close_connection()


    def close_connection(self):
        if self.client is not None:
            self.client.close()


    def send_command(self, command: str):
        with self.send_command_lock:
            self.client.sendall(command.encode())
            print(f'(Socket) Sent: {command}')
            print(f'(Socket) Response: {self._get_response()}')


    def _get_response(self):  # Waits for a response before sending a new instruction
        return self.client.recv(4).decode()
    
    
    def send_click(self, delay_before_click: int = 0):
        time.sleep(delay_before_click)
        self.last_click_time = time.time()

        self.send_command('C\r')
        
        time.sleep((np.random.randint(10) + 25) / 1000)  # Sleep to avoid sending another click instantly after mouseup


    def send_move(self, x: int, y: int):
        self.send_command(f'M{x},{y}\r')
