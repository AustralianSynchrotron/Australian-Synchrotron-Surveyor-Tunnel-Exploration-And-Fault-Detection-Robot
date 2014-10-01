//declare pins for mux channel
const int S0 = 2;
const int S1 = 3;
const int S2 = 4;
const int S3 = 5;
  
const int trig = 6; //pin for echo trigger
const int signal = 7; //pin for mux signal readback

//set up sensor names and mux channel
const int NUMBER_OF_SENSORS = 6;
const int pinChannel[4] = {S0, S1, S2, S3};
const String sensorName[NUMBER_OF_SENSORS] = {"nw","n","ne","sw","s","se"};
const byte sensorChannel[NUMBER_OF_SENSORS] = {B0000, B0001, B0010, B0011, B0100, B0101};

void setup() {
  //configure pins
  pinMode(S0, OUTPUT);
  pinMode(S1, OUTPUT);
  pinMode(S2, OUTPUT);
  pinMode(S3, OUTPUT);
  pinMode(trig, OUTPUT);
  pinMode(signal, INPUT);
  
  digitalWrite(S0, LOW);
  digitalWrite(S1, LOW);
  digitalWrite(S2, LOW);
  digitalWrite(S3, LOW);
  digitalWrite(trig, LOW);
  
  // initialize serial communication:
  Serial.begin(9600);
}

void loop()
{

  long duration, distance;
  
  //scan over all sensors
  for(int sensor_no = 0; sensor_no < NUMBER_OF_SENSORS; sensor_no++){
    Serial.print(sensorName[sensor_no]);
    Serial.print(" ");
    for(int i = 0; i < 4; i++){
      boolean nextbit = bitRead(sensorChannel[sensor_no],i);
      setPin(pinChannel[i],nextbit);
      Serial.print(nextbit);
    }
    //send trigger
    digitalWrite(trig, LOW);
    delayMicroseconds(2);
    digitalWrite(trig, HIGH);
    delayMicroseconds(10);
    digitalWrite(trig, LOW);
    //measure echo pulse
    duration = pulseIn(signal, HIGH, 30000);
    distance = usToCm(duration);
    Serial.print(" ");
    Serial.print(distance);
    Serial.print("cm");  
    Serial.println();
    delay(60);
  }
}

void setPin(int pin_no, boolean set_state){
  if(set_state){
    digitalWrite(pin_no, HIGH);
  }else{
    digitalWrite(pin_no, LOW);
  }
}

long usToCm(long microseconds)
{
  
  return microseconds / 58;
}
