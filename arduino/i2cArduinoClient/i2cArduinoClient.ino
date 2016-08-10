#include <Wire.h>

#define SLAVE_ADDRESS 0x04

void setup() {
  // initialize i2c as slave
  Wire.begin(SLAVE_ADDRESS);

  // define callbacks for i2c communication
  Wire.onReceive(receiveData);
  Wire.onRequest(sendData);
}

void loop() {
  delay(100);
}

// callback for received data
void receiveData(int byteCount){
  while(Wire.available()) {
    Wire.read();
  }
}

// callback for sending data
void sendData(){
  Wire.write();
}

