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
import serial


class MicrocontrollerSerialMouse(BaseMicrocontrollerMouse):
    def __init__(self, config):
        super().__init__(config)
        self.board = None
        self.connect_to_board()
        
    
    def connect_to_board(self):
        try:
            self.board = serial.Serial(f'COM{self.cfg.com_port}', 115200)
            print('Serial connected')
        except Exception as e:
            print(f'ERROR: Could not connect (Serial). {e}')
            self.close_connection()
            raise ConnectionError()


    def send_command(self, command: str):
        with self.send_command_lock:
            self.board.write(command.encode())
            print(f'(Serial) Sent: {command}')
            print(f'(Serial) Response: {self.get_response()}')


    def get_response(self):  # Waits for a response before sending a new instruction
        while True:
            receive = self.board.readline().decode('utf-8').strip()
            if len(receive) > 0:
                return receive
