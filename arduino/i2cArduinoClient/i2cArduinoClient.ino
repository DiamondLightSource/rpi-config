#include <Wire.h>

#define SLAVE_ADDRESS 0x04
#define MESSAGE_QUEUE_LENGTH 32

const String pStateArray[5] = {"CREATE", "HIGH", "LOW", "SET", "GET"};
const unsigned long timeDev = 60000;

bool logging = true;

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
  logger("Data RETURN: "+outgoingData);
  Wire.write(outgoingData.c_str());
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
      logger("returnVal");
      char buf[4];
      logger(itoa(returnVal, buf, 10));
      outgoingData = outgoingData + pbuf + ",True,"+ buf + ", Value Read Successfully//";
    } else {
      outgoingData = outgoingData + pbuf + ",False,None,Action Error on pin:" + pbuf + "//";
      logger("Input Pin Doesn't support that action");
    }
  } else if (type == 'o'){  //output (digital)
    if (state == pStateArray[0]){ //CREATE
      pinMode(pin, OUTPUT);
    } else if (state == pStateArray[1]){  //HIGH
      digitalWrite(pin, HIGH);
    } else if (state == pStateArray[2]){ //LOW
      digitalWrite(pin, LOW);
    } else {
      outgoingData = outgoingData  + pbuf + ",False,None,Action Error on pin:" + pbuf + "//";
      logger("Ouput Pin Doesn't support that action");
    }
  } else if (type == 'p'){  //output (pwm)
    if (state == pStateArray[3]){ //SET
      if (val >= 0 && val <= 255){
        analogWrite(pin, val);
      } else {
        outgoingData = outgoingData  + pbuf + ",False,None,Value Error on pin:" + pbuf + "//";
        logger("PWM values must be between 0 and 255");
      }
    } else {
      outgoingData = outgoingData  +pbuf + ",False,None,Action Error on pin:" + pbuf + "//";
      logger("PWM Pin Doesn'tsupport that action");
 
    }
  } else if (type == 'u'){ //input (internal pullup resistors)
    if (state == pStateArray[0]){ //CREATE
      pinMode(pin, INPUT_PULLUP);
    } else if (state == pStateArray[4]){ //GET
      int returnVal = digitalRead(pin);
      logger("returnVal");
      char buf[4];
      logger(itoa(returnVal, buf, 10));
      outgoingData = outgoingData + pbuf + ",True," + buf + ",Value Read successfully//";
    } else {
      outgoingData = outgoingData  + pbuf + ",False,None,Action Error on pin:" + pbuf + "//";
      logger("Input Pin (internal Pullup) Doesn't support that action");
    }
  } else if (type == 'a'){ //analogInput
    if (state == pStateArray[4]){ //GET
      int returnVal;
      returnVal = analogRead(pin);
      logger("returnVal");
      char buf[4];
      logger(itoa(returnVal, buf, 10));
      outgoingData = outgoingData + pbuf + ",True," + buf + ",Value Read Successfully//";
    } else {
      outgoingData = outgoingData  + pbuf + ",False,None,Action Error on pin:" + pbuf + "//";
      logger("Analog Input Pin Doesn't support that action");
    }
  } else {
    outgoingData = outgoingData + pbuf + ",False,None,Pin Type Error on pin:" + pbuf + "//";
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

