**This project is free and open-source. I am a student who spends their free time on this project so please if you like the project and want it's development to continue:**  
**🎁 Consider donating:** [Ways to donate](https://github.com/vike256#donations)   
**⭐ Give a star**  

---

# Unibot

Unibot is a multi-functional assistant tool developed for PC shooter games. Unibot works by simulating mouse input, which works with the following methods:
- Calling Windows mouse_event functions through Python  
- Using the Interception driver to simulate mouse input  
- Using external hardware capable of simulating a human interface device, such as an Arduino Leonardo, or any Raspberry Pi Pico variant. Unibot can communicate with these boards either through a COM port or a socket connection (ethernet or Wi-Fi).  

Unibot's most notable feature, **aim assist**, detects targets by looking for pixels within a specified color range on your screen, and then automatically moves the aim towards the target. The target detection utilizes OpenCV to merge color dots into a valid target blob.  

**Triggerbot** (/autoshoot) works in sync with the same target detection function and automatically shoots when the player is looking directly at a target.  

The **rapid-fire** feature clicks rapidly. This can be used to automatically shoot semi-automatic weapons.  

The **recoil** feature counters weapon recoil. It can be set to work with multiple recoil system types: point-and-shoot, and offset type recoil. Point-and-shoot is the most common recoil system used in FPS games and is used in games such as Call of Duty & Rainbow Six Siege. Offset type recoil is used in some tactical shooters such as Counter-Strike and VALORANT.  
  
Showcase: https://youtube.com/watch?v=-wMSt16IAQY

---

### Disclaimer
  
Unibot is a hobby project and should be treated as such. This project is intended for learning purposes only, but I acknowledge the possibility that this project can be used for malicious purposes such as to gain an unfair advantage in multiplayer shooter games. I do not condone video game cheating in any regard. If you are using Unibot to cheat, consider reading the following disclaimer.  
  
Cheating in video games often stems from deeper psychological needs, such as low self-esteem and a desire for control. If you find yourself resorting to cheats, it's worth taking a moment to reflect on why.  

Cheating can provide a temporary sense of control and accomplishment, but it ultimately undermines your genuine self-worth. True satisfaction comes from overcoming challenges and developing skills through honest effort.  

Overcoming cheating habits may require addressing underlying psychological issues. Talking to a therapist or counselor can help you develop healthier coping mechanisms and cultivate a more positive gaming experience.  

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
