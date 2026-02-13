**⭐ Give a star if you like the project**  

---


<img src="https://camo.githubusercontent.com/0184d1553919ae0b4efb257c0eefdd615318bd30836dc6b1d53d1e26cce1520b/68747470733a2f2f692e696d6775722e636f6d2f5276354e55556b2e706e67" alt="Unibot debug screen screenshot 1" height=250px width=auto> <img src="https://camo.githubusercontent.com/cfaa25bdf00081bc9cccd4793421620646a809bdb099673f790eec9742c28d25/68747470733a2f2f692e696d6775722e636f6d2f433365364e62322e706e67" alt="Unibot debug screen screenshot 2" height=250px width=auto> <img src="https://camo.githubusercontent.com/46fc4133bafa621c02d6905650fa6aa97873bd1ea2f67b3f6ff7d58576471d18/68747470733a2f2f692e696d6775722e636f6d2f354550714349342e706e67" alt="Unibot debug screen screenshot 3" height=250px width=auto> 

# Unibot

Unibot is a Python-based game hack that works on numerous games because its features don't depend on reading memory. Its configuration file can easily be modified to make it work on any FPS game that has an enemy highlight color such as VALORANT and Overwatch.   

Unibot sends mouse input to assist you in aiming and shooting. Three different mouse input methods have been implemented, and adding another requires only around 20 lines of code.  

Unibot was created as a PoC hobby project that proved that multimillion dollar anti-cheats such as Riot Games' Vanguard could be bypassed by a simple Python script that does not touch any game memory, and instead detects enemies by screengrabbing the user's monitor. 

Currently implemented input methods:  
- **Windows API**  
- **Interception driver** (https://github.com/oblitum/Interception)  
- **External hardware** capable of simulating a human interface device, such as an Arduino Leonardo or any Raspberry Pi Pico variant

Unibot can communicate with these microcontrollers through a COM port or a socket connection (Ethernet or Wi-Fi).

## What it does

### Aim assist
- Detects targets by analyzing pixels within a specified color range on your screen
- Automatically moves the aim towards the detected target

### Triggerbot
- Automatically shoots when the player's crosshair is on a target

### Rapid-fire
- Clicks rapidly to automatically shoot semi-automatic weapons

### Recoil Mitigation
- Counters weapon recoil
- Supports multiple recoil systems:
  - **Point-and-shoot**: Bullets go where your crosshair looks
  - **Offset type recoil**: Bullets go above crosshair
  
**Showcase video:**  
<a href="https://youtube.com/watch?v=8LUBfXCIu6I" target=_blank><img src="https://i.imgur.com/tNO8ZMF.png" alt="Showcase video thumbnail" width="600"></a>    
[*Python colorbot hits world record 220k+ score with 100% accuracy on Aim Lab*](https://youtube.com/watch?v=8LUBfXCIu6I)

## Disclaimer
  
This is a hobby project and intended for learning purposes only. I do not condone cheating in any regard. 

If you are using Unibot to cheat, please take a moment to reflect on why. Cheating ruins competitive integrity, undermines genuine achievement, and leaves you feeling just as empty as before.

## Installation and usage
[Wiki](https://github.com/vike256/Unibot/wiki/Guide)  

---

## Copyright
```
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
```
