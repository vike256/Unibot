// Copyright (C) 2026 vike256 — Unibot. See LICENSE.txt for full GPL-3.0 license.
//
// Raspberry Pi Pico variant of the serial mouse firmware.
//
// Wire protocol is identical to src/microcontroller/serial/serial.ino, so the
// Python side needs no changes: `type = serial` in config.ini talks to either
// board. Differences are Pico specific:
//   - the onboard LED reports state (lit = ready, off while a click is held,
//     so every shot shows as a blink),
//   - no per-iteration delay(): readBytesUntil() already waits up to 1 ms, so
//     the extra delay only added idle latency.
//
// Reboot into UF2/Bootloader mode: the core reboots on a 1200 baud open, so
// `python -c "import serial; serial.Serial('COM4', 1200).close()"` is enough.

#include <Mouse.h>

#define CMD_BUF_SIZE 32
#define RESP_OK "a\r\n"
// Board identification, answered by 'V'. Distinguishes this firmware from the
// generic serial sketch when two boards are plugged in at once.
#define RESP_VERSION "a pico\r\n"

#define HID_MOVE_MIN -128
#define HID_MOVE_MAX 127

#define CLICK_DELAY_MIN 15
#define CLICK_DELAY_MAX 25

#define SERIAL_BAUD 115200

char cmdBuffer[CMD_BUF_SIZE] = {0};

void ledReady() {
  digitalWrite(LED_BUILTIN, HIGH);
}

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
  digitalWrite(LED_BUILTIN, LOW);
  Mouse.press(MOUSE_LEFT);
  delay(randomDelay);
  Mouse.release(MOUSE_LEFT);
  ledReady();
}

void executeButton(char state) {
  if (state == '1') {
    digitalWrite(LED_BUILTIN, LOW);
    Mouse.press(MOUSE_LEFT);
  } else if (state == '0') {
    Mouse.release(MOUSE_LEFT);
    ledReady();
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
  pinMode(LED_BUILTIN, OUTPUT);
  ledReady();
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
    } else if (cmdBuffer[0] == 'V') {
      Serial.print(RESP_VERSION);
      Serial.flush();
      return;
    }

    sendResponse(Serial);
  }
}
