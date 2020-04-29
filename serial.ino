void setup(){
    Serial1.begin(38400); // According to the Teensy Docs, this is the RX1 & TX1 on my board.
    // Serial itself corrosponds to the micro-usb port
}

String readSerial() {
  String buf = "";
  if (Serial1.available() > 0) {
    while (true) {
    while (Serial1.available() > 0) {
      if (Serial1.peek() == '#') { // END of buffer
        Serial1.read(); // Read it to clear.
        return buf;
      } else {
        buf += (char) Serial1.read();
      }
    }
    }
    // Serial1.println("Partial Buffer Received");
  }
  return buf;
}
void loop(){
  String cmd = readSerial();
  delay(10);
    if (cmd[0] == 'M') {
      Serial1.println(cmd.substring(1,5) + "," + cmd.substring(5));
      Mouse.move(cmd.substring(1,5).toInt(), cmd.substring(5).toInt());
    } else if (cmd[0] == 'C') {
      Mouse.set_buttons(cmd.substring(1,2).toInt(), 0, 0);
    } else if (cmd != "") {
      //Serial1.println("AAAA");
      // this is bad
    }
    
  }
    
