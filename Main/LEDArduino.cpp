int ledPins[] = {9, 10, 11, 12, 13};  // LEDs are connected to pins 9 through 13

void setup() {
    Serial.begin(9600);
    for (int i = 0; i < 5; i++) {
        pinMode(ledPins[i], OUTPUT);
    }
}

void loop() {
    if (Serial.available()) {
        int fingerCount = Serial.read();  // Read the number of raised fingers

        printf("fingers: %d\n", fingerCount);
        
        for (int i = 0; i < 5; i++) {
            if (i < fingerCount) {
                digitalWrite(ledPins[i], HIGH);  // Turn ON the LED
            } else {
                digitalWrite(ledPins[i], LOW);  // Turn OFF the LED
            }
        }
    }
}
