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
from .base_mouse import BaseMouse
from .winapi_mouse import WinApiMouse
from .interception_mouse import InterceptionMouse
from .microcontroller_serial_mouse import MicrocontrollerSerialMouse
from .microcontroller_socket_mouse import MicrocontrollerSocketMouse


def get_mouse_implementation(config):
    name = config.bot_input_type

    if name == 'winapi':
        print('Using WinApiMouse')
        return WinApiMouse(config)
    elif name == 'interception_driver':
        print('Using InterceptionMouse')
        return InterceptionMouse(config)
    elif name == 'microcontroller_serial':
        print('Using MicrocontrollerSerialMouse')
        return MicrocontrollerSerialMouse(config)
    elif name == 'microcontroller_socket':
        print('Using MicrocontrollerSocketMouse')
        return MicrocontrollerSocketMouse(config)
    else:
        raise ValueError("Unknown mouse implementation")