#include <Wire.h>

#define SLAVE_ADDRESS 0x04
#define MESSAGE_QUEUE_LENGTH 32

const String pStateArray[5] = {"CREATE", "HIGH", "LOW", "SET", "GET"};
const unsigned long timeDev = 1;

bool logging = false;

String outgoingData = "";

void logger(String a){
  if (logging == true){
      String timeString = (String)(millis()/timeDev);
      Serial.print(timeString+" LOG: ");
      Serial.println(a);
  }
}

// callback for received data
void receiveData(int byteCount){
  logger("Message Start");
  String messageString = "";
  while(Wire.available()) {
    messageString += (char)Wire.read();
  }
  logger(messageString);
  parseData(messageString);
  logger("Message end");
}

// callback for sending data
void sendData(){
  logger("Data RETURN: ");
  logger(outgoingData.c_str());
  logger((String)outgoingData.length());
  Wire.write(outgoingData.c_str(), outgoingData.length());
  outgoingData = "";
}

void parseData(String command){
  int pin;
  char type;
  String state;
  int val;

  char splitter = ',';
  
  String foundString = "";
  int lastPos = 0;
  
  outgoingData = "";
  
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

  if (logging == true) {
    Serial.println(pin);
    Serial.println(type);
    Serial.println(state);
    Serial.println(val);
  }

  char pbuf[2];
  itoa(pin, pbuf, 10);
  if (type == 'i'){ //input
    if (state == pStateArray[0]){ //CREATE
      pinMode(pin, INPUT);
    } else if (state ==  pStateArray[4]){ //GET
      int returnVal = digitalRead(pin);
      char buf[4];
      logger(itoa(returnVal, buf, 10));
      outgoingData = (String)pbuf + ",True,"+ buf + ",Value Read//";
    } else {
      outgoingData = (String)pbuf + ",False,None,Action Error:" + pbuf + "//";
      logger("Action Not Supported");
    }
  } else if (type == 'o'){  //output (digital)
    if (state == pStateArray[0]){ //CREATE
      pinMode(pin, OUTPUT);
    } else if (state == pStateArray[1]){  //HIGH
      digitalWrite(pin, HIGH);
    } else if (state == pStateArray[2]){ //LOW
      digitalWrite(pin, LOW);
    } else {
      outgoingData = (String)pbuf + ",False,None,Action Error:" + pbuf + "//";
      logger("Action Not Supported");
    }
  } else if (type == 'p'){  //output (pwm)
    if (state == pStateArray[3]){ //SET
      if (val >= 0 && val <= 255){
        analogWrite(pin, val);
      } else {
        outgoingData = (String)pbuf + ",False,None,Value Error:" + pbuf + "//";
        logger("PWM values error");
      }
    } else {
      outgoingData = (String)pbuf + ",False,None,Action Error:" + pbuf + "//";
      logger("Action Not Supported");
 
    }
  } else if (type == 'u'){ //input (internal pullup resistors)
    if (state == pStateArray[0]){ //CREATE
      pinMode(pin, INPUT_PULLUP);
    } else if (state == pStateArray[4]){ //GET
      int returnVal = digitalRead(pin);
      logger("returnVal");
      char buf[4];
      logger(itoa(returnVal, buf, 10));
      outgoingData = (String)pbuf + ",True," + buf + ",Value Read successfully//";
    } else {
      outgoingData = (String)pbuf + ",False,None,Action Error:" + pbuf + "//";
      logger("Input Pin (internal Pullup) Doesn't support that action");
    }
  } else if (type == 'a'){ //analogInput
    if (state == pStateArray[4]){ //GET
      int returnVal;
      returnVal = analogRead(pin);
      logger("returnVal");
      char buf[4];
      logger(itoa(returnVal, buf, 10));
      outgoingData = (String)pbuf + ",True," + buf + ",Value Read//";
    } else {
      outgoingData = (String)pbuf + ",False,None,Action Error:" + pbuf + "//";
      logger("Action Not Supported");
    }
  } else {
    outgoingData = (String)pbuf + ",False,None,Pin Type Error:" + pbuf + "//";
    logger("Pin type not recognised");
  }
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
  
}

