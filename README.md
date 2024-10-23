**This project is free and open-source. I am a student who spends their free time on this project so please if you like the project and want it's development to continue:**  
**🎁 Consider donating:** [Ways to donate](https://github.com/vike256#donations)   
**⭐ Give a star**  

---


<img src=https://i.imgur.com/c55L14T.png alt="Unibot logo" width="250"> 

# Unibot

Unibot is a multi-functional assistant tool developed for PC shooter games. It simulates mouse input using various methods:  
- **Windows mouse_event functions**
- **Interception driver**
- **External hardware** capable of simulating a human interface device, such as an Arduino Leonardo or any Raspberry Pi Pico variant

Unibot can communicate with these boards through a COM port or a socket connection (Ethernet or Wi-Fi).

## Key Features  

**1. Aim Assist**
- Detects targets by analyzing pixels within a specified color range on your screen
- Automatically moves the aim towards the detected target
- Uses OpenCV to merge color dots into a valid target blob

**2. Triggerbot**
- Works in sync with aim assist
- Automatically shoots when the player is aiming at a target

**3. Rapid-fire**
- Clicks rapidly to automatically shoot semi-automatic weapons

**4. Recoil Mitigation**
- Counters weapon recoil
- Supports multiple recoil systems:
  - **Point-and-shoot**: Commonly used in games like Call of Duty & Rainbow Six Siege
  - **Offset type recoil**: Used in tactical shooters like Counter-Strike and VALORANT
  
Showcase videos:  
- [Python colorbot hits world record 220k+ score with 100% accuracy on Aim Lab](https://youtube.com/watch?v=8LUBfXCIu6I)  
- [Unibot showcase 2023-11-29](https://youtube.com/watch?v=-wMSt16IAQY)  


---

### Disclaimer
  
This is a hobby project and intended for learning purposes only. I do not condone cheating in any regard. 

If you are using Unibot to cheat, please take a moment to reflect on why. Cheating ruins competitive integrity, undermines genuine achievement, and leaves you feeling just as empty as before.

---

### Installation and usage guide
[Wiki](https://github.com/vike256/Unibot/wiki/Guide)  

---

### Copyright
```
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
```
