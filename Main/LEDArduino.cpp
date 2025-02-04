// Ensure LEDs are connected to pins 9 through 13
int ledPins[] = {9, 10, 11, 12, 13};  

// Setup serial communication and LED pins
void setup() {
    Serial.begin(9600);
    for (int i = 0; i < 5; i++) {
        pinMode(ledPins[i], OUTPUT);
    }
}

// Continously display number of fingers raised
void loop() {
    // Read the number of raised fingers from the serial port
    if (Serial.available()) {
        int fingerCount = Serial.read();  

        // Print the number of fingers to the serial port
        printf("fingers: %d\n", fingerCount);
        
        // Display the number of fingers using the LEDs
        for (int i = 0; i < 5; i++) {
            if (i < fingerCount) {
                digitalWrite(ledPins[i], HIGH);  // Turn ON the LED
            } else {
                digitalWrite(ledPins[i], LOW);  // Turn OFF the LED
            }
        }
    }
}
