/*
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
*/

#include <Mouse.h>
#include <Ethernet.h>
#include <SPI.h>
 
int port = 50124;
int x = 0;
int y = 0;
String cmd = "";
char symbols[] = "-,0123456789";
char code[] = "UNIBOTCYPHER";
bool encrypt = false;

void decryptCommand(String &command) {
  if (encrypt) {
    for (int i = 0; i < command.length(); i++) {
      for (int j = 0; j < sizeof(code) - 1; j++) {
        if (command[i] == code[j]) {
          command[i] = symbols[j];
          break;
        }
      }
    }
  }
}

byte mac[] = {0x00, 0x00, 0x00, 0x00, 0x00, 0x00}; 
IPAddress ip(0,0,0,0); 
EthernetServer server(port); 
EthernetClient client;
 
void setup() {
  Mouse.begin();
  Ethernet.begin(mac, ip); 
  if (Ethernet.localIP() == INADDR_NONE) {
    while (true) {
      delay(1000);
    }
  }

  server.begin();
}
 
void loop() {
  if (!client || !client.connected()) {
    client = server.available();
  } 

  while (client.connected()) {
    String cmd = client.readStringUntil('\r');

    if (cmd.length() > 0) {
      if (cmd[0] == 'M') {
        decryptCommand(cmd);
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
      client.print("a\r\n");
      client.flush();
    }
  }
  delay(1);
}
