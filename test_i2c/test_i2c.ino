

#include <i2c_driver_wire.h>
/* LED Blink, Teensyduino Tutorial #1
   http://www.pjrc.com/teensy/tutorial.html
 
   This example code is in the public domain.
*/
#define SLAVE_ADDRESS 0x04
const int ledPin = 13;

void setup() {
  // initialize the digital pin as an output.
  pinMode(ledPin, OUTPUT);
  Wire.begin(SLAVE_ADDRESS);
  Wire.onReceive(receiveData);
  Serial.begin(9600);
  Mouse.screenSize(1920, 1080);
}

// the loop() methor runs over and over again
// as long as the board has power

void loop() {
  Serial.println("loop");
  delay(10000);
}

void receiveData(int byteCount) {
  int coords[2] = {0};
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
  Serial.println();
  String message = "Received data";
  Serial.println(coords[0]);
  Serial.println(coords[1]);
  Mouse.moveTo(coords[0], coords[1]);
 
}
