#include "BluetoothSerial.h"

#if !defined(CONFIG_BT_ENABLED) || !defined(CONFIG_BLUEDROID_ENABLED)
#error Bluetooth is not enabled! Please run `make menuconfig` to and enable it
#endif

BluetoothSerial SerialBT;

String val;
char input = 0;
String output = "";

const int limit = 20;
int Index = 0;
float Value = 0;
float Sum = 0;
float Readings[limit];
float Averaged = 0;
int IndexA = 0;
float ValueA = 0;
float SumA = 0;
float ReadingsA[limit];
float AveragedA = 0;

String getValue(String data, char separator, int index){
    int found = 0;
    int strIndex[] = { 0, -1 };
    int maxIndex = data.length() - 1;

    for (int i = 0; i <= maxIndex && found <= index; i++) {
        if (data.charAt(i) == separator || i == maxIndex) {
            found++;
            strIndex[0] = strIndex[1] + 1;
            strIndex[1] = (i == maxIndex) ? i+1 : i;
        }
    }
    return found > index ? data.substring(strIndex[0], strIndex[1]) : "";
}

void setup() {
  Serial.begin(115200);
  Serial2.begin(57600, SERIAL_8N1, 16, 17);

  if(SerialBT.begin("WMouse")){
    Serial.println("Bluetooth Initialized ...");
  }

  pinMode(18, INPUT);
  pinMode(5, INPUT);
}
  
void loop() {
  if (Serial2.available() > 0) {
    
    input = Serial2.read();

    if (input != '\n') {
      output += input;
    } else {      
      Sum = Sum - Readings[Index];
      Value = getValue(output, ',', 1).toFloat();
      Readings[Index] = Value;
      Sum = Sum + Value;
      Index = (Index+1) % limit;
      Averaged = Sum / limit;
      
      SumA = SumA - ReadingsA[IndexA];
      ValueA = getValue(output, ',', 2).toFloat();
      ReadingsA[IndexA] = ValueA;
      SumA = SumA + ValueA;
      IndexA = (IndexA+1) % limit;
      AveragedA = SumA / limit;

      output = getValue(output, ',', 0);
      output += ',';
      output += (String) Averaged;
      output += ',';
      output += (String) AveragedA;
      output += ",";
      output += String(digitalRead(18));
      output += ",";
      output += String(digitalRead(5));

      Serial.println(output);
      SerialBT.println(output);

      output = "";
    }
  }
}
