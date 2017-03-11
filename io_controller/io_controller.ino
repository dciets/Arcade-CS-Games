byte pins[] = {2, 3, 4, 5, 6, 7, 8, 9, 10, 11};
bool flags[10];

void setup() {
  Serial.begin(115200);

  for (byte i = 0; i < 10; i++) {
    pinMode(pins[i], INPUT_PULLUP);
  }

  pinMode(A0, OUTPUT);
  pinMode(A1, OUTPUT);

  digitalWrite(A0, HIGH);
  digitalWrite(A1, HIGH);
}

void loop() {
  if (Serial.available()) {
    byte c = Serial.read();

    digitalWrite(A0, (c & 1) ? LOW : HIGH);
    digitalWrite(A1, (c & 2) ? LOW : HIGH);
  }

  for (byte i = 0; i < 10; i++) {
    bool state = digitalRead(pins[i]) == HIGH;

    if (state != flags[i]) {
      Serial.print(char((i << 1) | (state ? 0 : 1)));

      flags[i] = state;
    }
  }

  delay(10);
}
