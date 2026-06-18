# Copyright (C) 2026 vike256 — Unibot. See LICENSE.txt for full GPL-3.0 license.
from .base_microcontroller_mouse import BaseMicrocontrollerMouse
import socket


class MicrocontrollerSocketMouse(BaseMicrocontrollerMouse):
    label = "Socket"

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
            raise ConnectionError()


    def send_command(self, command: str):
        with self.send_command_lock:
            self.board.sendall(command.encode())
            if self.cfg.debug:
                print(f'({self.label}) Sent: {command}')
            response = self.get_response()
            if self.cfg.debug:
                print(f'({self.label}) Response: {response}')


    def get_response(self):  # Waits for a response before sending a new instruction
        return self.board.recv(4).decode()
     
