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

void parseData(){
  //Parses input buffer 
  /*
   * Needs the following command options:
   * pinMode
   * analogReference
   * digitalWrite
   * digitalRead
   * analogRead
   * analogWrite (this is what pwm is called)
   * 
   * Will also need a control framework;
   * e.g. prior to a data request, a command will be recieved to take a reading or whatever, that data should be queued to a buffer 
   * in anticipation of a read request to offload everything.
   */
}
