#include <Mouse.h>
 
int x = 0;
int y = 0;
int maxValue = 127;
int minValue = -127;
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

        if (x > maxValue) x = maxValue;
        if (x < minValue) x = minValue;
        if (y > maxValue) y = maxValue;
        if (y < minValue) y = minValue;

        Mouse.move(x, y);
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
    cmd = "";
  }
  delay(1);
}