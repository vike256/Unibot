# Copyright (C) 2026 vike256 — Unibot. See LICENSE.txt for full GPL-3.0 license.
from .base_microcontroller_mouse import BaseMicrocontrollerMouse
import serial


class MicrocontrollerSerialMouse(BaseMicrocontrollerMouse):
    label = "Serial"

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
            if self.cfg.debug:
                print(f'({self.label}) Sent: {command}')
            response = self.get_response()
            if self.cfg.debug:
                print(f'({self.label}) Response: {response}')


    def get_response(self):  # Waits for a response before sending a new instruction
        while True:
            receive = self.board.readline().decode('utf-8').strip()
            if len(receive) > 0:
                return receive
