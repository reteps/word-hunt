#include <i2c_driver_wire.h>

#define SLAVE_ADDRESS 0x04

void setup() {
  Wire.begin(SLAVE_ADDRESS);
  Wire.onReceive(receiveData);
  Serial.begin(9600);
  Mouse.screenSize(1125, 2436, true);
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
    Mouse.moveTo(coords[1],coords[2]);
  } else if (coords[0] == 2) {
    Mouse.set_buttons(coords[1], 0, 0);
  } else if (coords[0] == 3) {
    Mouse.move(coords[1], coords[2]);
    
  }
}
