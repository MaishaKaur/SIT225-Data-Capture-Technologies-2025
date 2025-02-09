#define TRIG_PIN 9
#define ECHO_PIN 10

void setup() 
{
    Serial.begin(9600); 
    pinMode(TRIG_PIN, OUTPUT);
    pinMode(ECHO_PIN, INPUT);
}

void loop() {
    digitalWrite(TRIG_PIN, LOW);
    delayMicroseconds(2);
    digitalWrite(TRIG_PIN, HIGH);
    delayMicroseconds(10);
    digitalWrite(TRIG_PIN, LOW);

    long duration = pulseIn(ECHO_PIN, HIGH);
    float distance = duration * 0.034 / 2; 

    Serial.print(millis());
    Serial.print(",");
    Serial.println(distance);

    delay(1000); 
}