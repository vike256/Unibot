# Copyright (C) 2026 vike256 — Unibot. See LICENSE.txt for full GPL-3.0 license.
from .base_microcontroller_mouse import BaseMicrocontrollerMouse
import serial


class MicrocontrollerSerialMouse(BaseMicrocontrollerMouse):
    label = "Serial"
    # Response read timeout. The firmware holds the click for 40-80 ms before it
    # answers, so this must exceed that, but it must not be None or readline()
    # would block forever if the board is unplugged mid-run.
    timeout = 0.2

    def __init__(self, config):
        super().__init__(config)
        self.board = None
        self.connect_to_board()

    def connect_to_board(self):
        try:
            self.board = serial.Serial(f'COM{self.cfg.com_port}', 115200, timeout=self.timeout)
            print('Serial connected')
        except Exception as e:
            print(f'ERROR: Could not connect (Serial). {e}')
            self.close_connection()
            raise ConnectionError()

    def send_command(self, command: str):
        with self.send_command_lock:
            try:
                self.board.write(command.encode())
                response = self.get_response()
            except serial.SerialException as e:
                # Board unplugged or port lost while running
                print(f'ERROR: Serial connection lost ({e}). Reconnecting...')
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
        receive = self.board.readline().decode('utf-8', errors='replace').strip()
        return receive