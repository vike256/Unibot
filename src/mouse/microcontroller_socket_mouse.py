# Copyright (C) 2026 vike256 — Unibot. See LICENSE.txt for full GPL-3.0 license.
from .base_microcontroller_mouse import BaseMicrocontrollerMouse
import socket


class MicrocontrollerSocketMouse(BaseMicrocontrollerMouse):
    label = "Socket"
    timeout = 0.2

    def __init__(self, config):
        super().__init__(config)
        self.board = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connect_to_board()

    def connect_to_board(self):
        print(f'Connecting to {self.cfg.microcontroller_ip}:{self.cfg.microcontroller_port}...')
        try:
            self.board = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.board.settimeout(self.timeout)
            self.board.connect((self.cfg.microcontroller_ip, self.cfg.microcontroller_port))
            print('Socket connected')
        except OSError as e:
            print(f'ERROR: Could not connect (Socket). {e}')
            self.close_connection()
            raise ConnectionError()

    def send_command(self, command: str):
        with self.send_command_lock:
            try:
                self.board.sendall(command.encode())
                response = self.get_response()
            except OSError as e:
                # Board disconnected while running
                print(f'ERROR: Socket connection lost ({e}). Reconnecting...')
                self.close_connection()
                try:
                    self.connect_to_board()
                except ConnectionError:
                    return
                return
            if self.cfg.debug:
                print(f'({self.label}) Sent: {command}')
                print(f'({self.label}) Response: {response}')

    def get_response(self):  # Waits for a response before sending a new instruction
        try:
            return self.board.recv(4).decode()
        except socket.timeout:
            return ''