byte pins[] = {2,3,4,5,6,7,8,9,10,11};
bool flags[10];

void setup() {
  // put your setup code here, to run once:
  Serial.begin(115200);

  for(byte i = 0; i < 10; i++) {
    pinMode(pins[i], INPUT_PULLUP);
  }
}

void loop() {
  if(Serial.available()) {
    byte c = Serial.read();

    analogWrite(A0, c & 1);
    analogWrite(A1, c & 2);
  }

  for(byte i = 0; i < 10; i++) {
    bool state = digitalRead(pins[i]) == LOW;

    if(state != flags[i]) {
      Serial.print(char((i << 1) | (state ? 1 : 0)));
      flags[i] = state;
    }
  }
  
}
