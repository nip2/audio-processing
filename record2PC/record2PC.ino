// Have a push button on pin 8 and piezo pickup on pin A0
// piezo input has zener and 1M ohm paralell to common

using namespace std;

#define INPIN A2
#define BUTN 8

const uint16_t samples = 512;
const double samplingFrequency = 10000;

unsigned int sampling_period_us;
unsigned long microseconds;

boolean running = false;


void getSample() {
  /*SAMPLING*/
  microseconds = micros();
  for (int i = 0; i < samples; i++) {
    Serial.println(analogRead(INPIN));
    while (micros() - microseconds < sampling_period_us) {
      //empty loop
    }
    microseconds += sampling_period_us;
  }
}

// record data when button is pushed
void setup() {
  sampling_period_us = round(1000000 * (1.0 / samplingFrequency));
  pinMode(BUTN, INPUT);
  Serial.begin(9600);
  while (!Serial);
  Serial.println("Ready");
}


void loop() {
  if (digitalRead(BUTN) == LOW) {
    Serial.println("start");
    running = true;
  }
  while (digitalRead(BUTN) == LOW) {
    getSample();
  }
  if (running == true) {
    Serial.println("end");
    running = false; 
  }
}
