/*
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
*/

#include <Mouse.h>
 
int x = 0;
int y = 0;
String cmd = "";

void setup() {
  Mouse.begin();
  Serial.begin(115200);
  Serial.setTimeout(1);
}
 
void loop() {
  String cmd = Serial.readStringUntil('\r');

  if (cmd.length() > 0) {
    if (cmd[0] == 'M') {
      int commaIndex = cmd.indexOf(',');
      if (commaIndex != -1) {
        x = cmd.substring(1, commaIndex).toInt();
        y = cmd.substring(commaIndex + 1).toInt();

        while (x != 0 || y != 0) {
          int moveX = constrain(x, -128, 127);
          int moveY = constrain(y, -128, 127);

          Mouse.move(moveX, moveY);

          x -= moveX;
          y -= moveY;
        }
      }
    } else if (cmd[0] == 'C') {
      int randomDelay = random(40, 80);
      Mouse.press(MOUSE_LEFT);
      delay(randomDelay);
      Mouse.release(MOUSE_LEFT);
    } else if (cmd[0] == 'B') {
      if (cmd[1] == '1') {
        Mouse.press(MOUSE_LEFT);
      } else if (cmd[1] == '0') {
        Mouse.release(MOUSE_LEFT);
      }
    }
    Serial.print("a\r\n");
    Serial.flush();
  }
}