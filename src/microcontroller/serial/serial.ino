// Copyright (C) 2026 vike256 — Unibot. See LICENSE.txt for full GPL-3.0 license.

#include <Mouse.h>

#define CMD_BUF_SIZE 32
#define RESP_OK "a\r\n"

#define HID_MOVE_MIN -128
#define HID_MOVE_MAX 127

#define CLICK_DELAY_MIN 40
#define CLICK_DELAY_MAX 80

#define SERIAL_BAUD 115200

char cmdBuffer[CMD_BUF_SIZE] = {0};

void processMovement(int& x, int& y) {
  if (x == 0 && y == 0) {
    return;
  }
  int moveX = constrain(x, HID_MOVE_MIN, HID_MOVE_MAX);
  int moveY = constrain(y, HID_MOVE_MIN, HID_MOVE_MAX);
  Mouse.move(moveX, moveY);
  x -= moveX;
  y -= moveY;
}

void processMovementBlocking(int x, int y) {
  while (x != 0 || y != 0) {
    processMovement(x, y);
  }
}

void executeClick() {
  int randomDelay = random(CLICK_DELAY_MIN, CLICK_DELAY_MAX);
  Mouse.press(MOUSE_LEFT);
  delay(randomDelay);
  Mouse.release(MOUSE_LEFT);
}

void executeButton(char state) {
  if (state == '1') {
    Mouse.press(MOUSE_LEFT);
  } else if (state == '0') {
    Mouse.release(MOUSE_LEFT);
  }
}

void sendResponse(Stream& stream) {
  stream.print(RESP_OK);
  stream.flush();
}

bool parseMoveCommand(char* buffer, int& outX, int& outY) {
  if (buffer == nullptr || buffer[0] != 'M') {
    return false;
  }
  char* comma = strchr(buffer + 1, ',');
  if (comma == nullptr) {
    return false;
  }
  *comma = '\0';
  outX = atoi(buffer + 1);
  outY = atoi(comma + 1);
  return true;
}

void setup() {
  Mouse.begin();
  Serial.begin(SERIAL_BAUD);
  Serial.setTimeout(1);
}

void loop() {
  int len = Serial.readBytesUntil('\r', cmdBuffer, sizeof(cmdBuffer) - 1);
  if (len > 0) {
    cmdBuffer[len] = '\0';

    if (cmdBuffer[0] == 'M') {
      int targetX = 0, targetY = 0;
      if (parseMoveCommand(cmdBuffer, targetX, targetY)) {
        processMovementBlocking(targetX, targetY);
      }
    } else if (cmdBuffer[0] == 'C') {
      executeClick();
    } else if (cmdBuffer[0] == 'B') {
      executeButton(cmdBuffer[1]);
    }

    sendResponse(Serial);
  }

  delay(1);
}
