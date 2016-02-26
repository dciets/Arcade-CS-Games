// magic numbers
#define W 25
#define A 38
#define S 39
#define D 40
#define SPACE 65
#define UP 111
#define DOWN 116
#define LEFT 113
#define RIGHT 114
#define ZERO 19

byte pins[] = {2, 3, 4, 5, 6, 7, 8, 9, 10, 11};
byte keys[] = {W, A, S, D, SPACE, UP, DOWN, LEFT, RIGHT, ZERO};

void setup(){
  Serial.begin(9600);
  for (int i = 0; i < sizeof(pins); i++) {
    pinMode(pins[i], INPUT_PULLUP);
  }
}

void loop(){
  for (int i = 0; i < sizeof(pins); i++) {
    int inputVal = digitalRead(pins[i]);
    if (inputVal == LOW) {
      Serial.println(keys[i]);
    }
  }
  delay(30);
}



