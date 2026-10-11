#include <ESP32Servo.h>
Servo cihuyy[5];

int pinServo[5] = {12,13,14,15,16};

void setup() {
  Serial.begin(115200);
  for(int i =0; i < 5; i++) {
    cihuyy[i].attach(pinServo[i]);
  }

  cihuyy[0].write(0);
  cihuyy[1].write(0);
  cihuyy[2].write(0);
  cihuyy[3].write(180);
  cihuyy[4].write(0);

}

void loop() {
  if(Serial.available()) {
    String data = Serial.readStringUntil('\n');
    Serial.println(data);
    cihuyy[0].write(data[0] == '1' ? 0 : 180);
    cihuyy[1].write(data[1] == '1' ? 0 : 180);
    cihuyy[2].write(data[2] == '1' ? 0 : 180);
    cihuyy[3].write(data[3] == '1' ? 180 : 0);
    cihuyy[4].write(data[4] == '1' ? 0 : 180);
}

}
