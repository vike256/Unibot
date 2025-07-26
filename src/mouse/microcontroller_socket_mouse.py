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
import socket


class MicrocontrollerSocketMouse(BaseMicrocontrollerMouse):
    def __init__(self, config):
        super().__init__(config)
        self.board = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connect_to_board()
        

    def connect_to_board(self):
        print(f'Connecting to {self.cfg.microcontroller_ip}:{self.cfg.microcontroller_port}...')
        try:
            self.board.connect((self.cfg.microcontroller_ip, self.cfg.microcontroller_port))
            print('Socket connected')
        except Exception as e:
            print(f'ERROR: Could not connect (Socket). {e}')
            self.close_connection()


    def send_command(self, command: str):
        with self.send_command_lock:
            self.board.sendall(command.encode())
            print(f'(Socket) Sent: {command}')
            print(f'(Socket) Response: {self.get_response()}')


    def get_response(self):  # Waits for a response before sending a new instruction
        return self.board.recv(4).decode()
    