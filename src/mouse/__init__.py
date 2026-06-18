# Copyright (C) 2026 vike256 — Unibot. See LICENSE.txt for full GPL-3.0 license.
def get_mouse_implementation(config):
    name = config.communication_type

    if name == 'winapi':
        print('Using WinApiMouse')
        from .winapi_mouse import WinApiMouse
        return WinApiMouse(config)
    elif name == 'interception_driver':
        print('Using InterceptionMouse')
        from .interception_mouse import InterceptionMouse
        return InterceptionMouse(config)
    elif name == 'serial':
        print('Using MicrocontrollerSerialMouse')
        from .microcontroller_serial_mouse import MicrocontrollerSerialMouse
        return MicrocontrollerSerialMouse(config)
    elif name == 'socket':
        from .microcontroller_socket_mouse import MicrocontrollerSocketMouse
        print('Using MicrocontrollerSocketMouse')
        return MicrocontrollerSocketMouse(config)
    else:
        raise ValueError("Unknown mouse implementation")