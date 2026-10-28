**⭐ Give a star if you like the project**  

---


<img src="https://camo.githubusercontent.com/0184d1553919ae0b4efb257c0eefdd615318bd30836dc6b1d53d1e26cce1520b/68747470733a2f2f692e696d6775722e636f6d2f5276354e55556b2e706e67" alt="Unibot debug screen screenshot 1" height=250px width=auto> <img src="https://camo.githubusercontent.com/cfaa25bdf00081bc9cccd4793421620646a809bdb099673f790eec9742c28d25/68747470733a2f2f692e696d6775722e636f6d2f433365364e62322e706e67" alt="Unibot debug screen screenshot 2" height=250px width=auto> <img src="https://camo.githubusercontent.com/46fc4133bafa621c02d6905650fa6aa97873bd1ea2f67b3f6ff7d58576471d18/68747470733a2f2f692e696d6775722e636f6d2f354550714349342e706e67" alt="Unibot debug screen screenshot 3" height=250px width=auto> 

# Unibot

Unibot is a Python-based game hack that works on numerous games because its features don't depend on reading memory. Its configuration file can easily be modified to make it work on any FPS game that has an enemy highlight color such as VALORANT and Overwatch.   

This build is triggerbot only: it shoots when your crosshair is on a target and never moves your aim. Three different mouse input methods have been implemented, and adding another requires only around 20 lines of code.  

Unibot was created as a PoC hobby project that proved that multimillion dollar anti-cheats such as Riot Games' Vanguard could be bypassed by a simple Python script that does not touch any game memory, and instead detects enemies by screengrabbing the user's monitor. 

Currently implemented input methods:  
- **Windows API**  
- **Interception driver** (https://github.com/oblitum/Interception)  
- **External hardware** capable of simulating a human interface device, such as an Arduino Leonardo or any Raspberry Pi Pico variant

Unibot can communicate with these microcontrollers through a COM port or a socket connection (Ethernet or Wi-Fi).

## What it does

### Triggerbot
- Detects targets by analyzing pixels within a specified color range on your screen
- Automatically shoots when the player's crosshair is on a target

**Showcase video:**  
<a href="https://youtube.com/watch?v=8LUBfXCIu6I" target=_blank><img src="https://i.imgur.com/tNO8ZMF.png" alt="Showcase video thumbnail" width="600"></a>    
[*Python colorbot hits world record 220k+ score with 100% accuracy on Aim Lab*](https://youtube.com/watch?v=8LUBfXCIu6I)

## Disclaimer
  
This is a hobby project and intended for learning purposes only. I do not condone cheating in any regard. 

If you are using Unibot to cheat, please take a moment to reflect on why. Cheating ruins competitive integrity, undermines genuine achievement, and leaves you feeling just as empty as before.

## Installation

1. Install **Python 3.10+**
2. Install the dependencies:
   ```
   pip install -r requirements.txt
   ```
3. If you use an RP2040/Pico as the mouse, flash the firmware (Usage → step 1). If you
   have no hardware, skip that and set `type = winapi` in step 2.

## Usage (basics)

### 1. Flash the firmware (RP2040 / Pico only)

Firmware lives in `src/microcontroller/`. Use the `serial` one for a USB connection.

1. Install [Arduino IDE](https://www.arduino.cc/en/software) and add the
   [RP2040 board package](https://github.com/earlephilhower/arduino-pico)
2. Open `src/microcontroller/serial/serial.ino`
3. Select your board (e.g. `Seeed XIAO RP2040`) and set
   **Tools → USB Stack → Pico SDK** (TinyUSB does not work with this sketch)
4. Upload, then note the COM port that appears in Device Manager

### 2. Configure `config.ini`

```ini
[communication]
type = serial      ; winapi, interception_driver, serial or socket
com_port = 3       ; your board's COM port (also accepts "COM3")
```

No hardware? Use `type = winapi`.

### 3. In-game and Windows settings (VALORANT)

- Settings → General → Accessibility → **Enemy Highlight Color = Purple (Tritanopia)**
  - the default HSV values are calibrated for it; recalibrate with the
    [HSV range tool](https://github.com/hariangr/HsvRangeTool) for another color
- Video → **Display Mode = Windowed Fullscreen**
  (exclusive fullscreen can't be captured and shows a black debug mask)
- **Turn off Windows HDR** (it shifts captured colors and breaks detection)
- Keep in-game **Raw Input Buffer** off if shots feel delayed

### 4. Run

```
python src/main.py
```

`Unibot ON` means it's working.

**Hold Mouse 5 down** while your crosshair is on an enemy — it fires and keeps firing
while you hold. **Release Mouse 5 and the triggerbot stops.** It is hold-to-fire, not a
toggle.

In `mode = head` the key is not needed at all — it fires by itself whenever you are on a
head (see [Modes](#6-modes)).

### 5. Controls

| Key | Action |
|---|---|
| **Mouse 5** | **Hold down** to keep the triggerbot active — release to stop |
| **F5** | Cycle mode: `normal` → `head` → `both` |
| **F1** | Reload the config |
| **F4** | Exit |

Pick a trigger key that is **not** bound to an ability in-game.

### 6. Modes

Set `mode` in `[trigger]`:

| Mode | Behaviour |
|---|---|
| `normal` (default) | Fires anywhere on the target. **Hold Mouse 5** to activate. |
| `head` | Fires **only when the crosshair is on the head**. **Always active — no key.** |
| `both` | Both at once: heads always without a key, **and** anywhere on the target while **Mouse 5 is held**. |

`head` and `both` need no key for headshots: just play, and it fires the moment your
crosshair lands on an enemy's head and stops the instant you move off. `head_height`
controls how much counts as the head when a whole body is highlighted (fraction from the
top, default `0.2`, lower = stricter). When only the head is highlighted — an enemy
behind cover, or far away — the entire highlight counts as the head, so you never have to
nudge the aim to make it fire. `both` additionally lets you hold Mouse 5 to spray
anywhere on the body.

Switch modes by editing `mode` and pressing **F1**, or just tap **F5** while playing.

### 7. Tuning

Everything lives in `config.ini` and reloads with **F1**.

| Setting | Meaning |
|---|---|
| `lower_color` / `upper_color` | The target color to detect (HSV) |
| `capture_fov_x` / `capture_fov_y` | Size of the detection box at screen center |
| `mode` | `normal` (hold key, anywhere), `head` (always on, headshots only) or `both` |
| `head_height` | How much counts as the head when a body is highlighted, from the top (`0.2` default). Head-only highlights always count in full |
| `head_threshold` | Head mode tolerance in px (`0` = must be exactly on the head) |
| `trigger_threshold` | Tolerated gap in px between crosshair and target (`0` = must be on it) |
| `min_target_area` | Ignore blobs smaller than this — kills speck false positives |
| `trigger_delay` / `trigger_randomization` | Delay before shooting (ms), for a more human feel |
| `click_rate` | Max clicks per second (keep above your weapon's fire rate) |
| `max_loops_per_sec` | Detection "fps"; `0` = uncapped, otherwise use your refresh rate |
| `screen_center_offset` | Move the detection box up/down to match your crosshair |

### Debugging

Turn `enabled = true` in `[debug]` to see what Unibot sees (`display_mode = mask` shows
the detected color in white). Use it to fix a wrong color range or threshold.

| Problem | Fix |
|---|---|
| Nothing happens | Set `enabled = true` in `[debug]` and check the mask shows the enemy |
| Mask is all black | Use Windowed Fullscreen and disable HDR |
| `PermissionError` on the COM port | Only one instance can use the port — close the app first |
| Shoots at nothing | Raise `trigger_threshold`; lower it to shoot earlier but risk false positives |

---

## Copyright
```
Unibot, an open-source colorbot.
Copyright (C) 2026 vike256

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
```
