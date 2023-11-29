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

from cheats import Cheats
from mouse import Mouse
from screen import Screen
from utils import Utils


def main():
    # Print licensing info
    print('''
Unibot  Copyright (C) 2023  vike256
This program comes with ABSOLUTELY NO WARRANTY.
This is free software, and you are welcome to redistribute it under certain conditions.
For details see <LICENSE.txt>.
    ''')

    # Print donation info
    print('Consider donating: https://github.com/vike256#donations \n')

    # Program loop
    while True:
        # Track delta time
        start_time = time.time()

        utils = Utils()
        config = utils.config
        cheats = Cheats(config)
        mouse = Mouse(config)
        screen = Screen(config)

        print('Unibot ON')

        # Cheat loop
        while True:
            delta_time = time.time() - start_time
            start_time = time.time()
            
            reload_config = utils.check_key_binds()
            if reload_config:
                break

            if (utils.get_aim_state() or utils.get_trigger_state()) or (config.debug and config.debug_always_on):
                # Get target position and check if there is a target in the center of the screen
                target, trigger = screen.get_target(cheats.recoil_offset)

                # Shoot if target in the center of the screen
                if utils.get_trigger_state() and trigger:
                    if config.trigger_delay != 0:
                        delay_before_click = (np.random.randint(config.trigger_randomization) + config.trigger_delay) / 1000
                    else:
                        delay_before_click = 0
                    mouse.click(delay_before_click)

                # Calculate movement based on target position
                cheats.calculate_aim(utils.get_aim_state(), target)

            if utils.get_rapid_fire_state():
                mouse.click()

            # Apply recoil
            cheats.apply_recoil(utils.recoil_state, delta_time)

            # Move the mouse based on the previous calculations
            mouse.move(cheats.move_x, cheats.move_y)

            # Reset move values so the aim doesn't keep drifting when no targets are on the screen
            cheats.move_x, cheats.move_y = (0, 0)

            # Do not loop above the set refresh rate
            time_spent = (time.time() - start_time) * 1000
            if time_spent < screen.fps:
                time.sleep((screen.fps - time_spent) / 1000)

        del utils
        del cheats
        del mouse
        del screen
        print('Reloading')


if __name__ == "__main__":
    main()
