#include <i2c_driver_wire.h>

#define SLAVE_ADDRESS 0x04

void setup() {
  Wire.begin(SLAVE_ADDRESS);
  Wire.onReceive(receiveData);
  Serial.begin(9600);
  Mouse.screenSize(1920, 1080);
}

void loop() {}

void receiveData(int byteCount) {
  int coords[3] = {0};
  int pos = 0;
  String buf = "";
  while ( Wire.available()) {
    char c = Wire.read();
    if (c == ',') {
      coords[pos] = buf.toInt();
      pos++;
      buf = "";
    } else {
      buf += c;
    }
  }
  if (coords[0] == 1) {
    Serial.println("Received mouse move instruction.");
    Mouse.moveTo(coords[0],coords[1]);
  } else if (coords[0] == 2) {
    Serial.println("Received click instruction.");
    Mouse.set_buttons(coords[0], 0, coords[1]);
  }
}
