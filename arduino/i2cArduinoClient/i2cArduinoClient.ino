#include <Wire.h>

#define SLAVE_ADDRESS 0x04

const String pStateArray[5] = {"CREATE", "HIGH", "LOW", "SET", "GET"};

bool logging = true;
bool stringLock = false;
String messageString = "";

void logger(String a){
  if (logging == true){
      Serial.print("LOG MESSAGE:");
      Serial.println(a);
  }
}

// callback for received data
void receiveData(int byteCount){
  logger("Message Start");
  messageString = "";
  stringLock = true;
  
  while(Wire.available()) {
    messageString += (char)Wire.read();
  }
  stringLock = false;
  logger(messageString);
  logger("Message end");
}

// callback for sending data
void sendData(){
  //Wire.write();
}

void parseData(String command){
  int pin;
  char type;
  String state;
  int val;

  char splitter = ',';
  String foundString = "";
  int lastPos = 0;
  char logString[] = "";
  
  foundString = findString(lastPos, command, splitter);
  pin = atoi(foundString.c_str());
  foundString = findString(lastPos, command, splitter);
  type = (char)foundString[0];
  foundString = findString(lastPos, command, splitter);
  for (int i = 0; i < 5; i++){
    if (foundString == pStateArray[i]){
      state = pStateArray[i];
      break;
    }
  }
  foundString = command.substring(lastPos, command.length());
  val = atoi(foundString.c_str());
  
  Serial.println(pin);
  Serial.println(type);
  Serial.println(state);
  Serial.println(val);
  
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

String findString(int& lastPos, String searchString, char tar){
  int thisPos = 0;
  String foundString = "";
  thisPos = searchString.indexOf(tar, lastPos);
  for (int x = lastPos; x < thisPos; x++){
    foundString += searchString[x];
  }
  lastPos = thisPos + 1;
  return foundString;
}

void setup() {  
  if (logging == true) {
    Serial.begin(9600);
    Serial.println("SERIAL CONNECTED");
  }
  // initialize i2c as slave
  Wire.begin(SLAVE_ADDRESS);

  // define callbacks for i2c communication
  Wire.onReceive(receiveData);
  Wire.onRequest(sendData);
}

void loop() {
  if (stringLock == false){
    if (messageString != ""){
      parseData(messageString);
      messageString = "";
    }
    delay(250);
  } else {
    delay(250);
  }
}

