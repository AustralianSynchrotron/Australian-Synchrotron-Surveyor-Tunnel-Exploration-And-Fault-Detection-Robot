/*
  The circuit:
 * LCD RS pin to digital pin 11
 * LCD Enable pin to digital pin 13
 * LCD D4 pin to digital pin 5
 * LCD D5 pin to digital pin 4
 * LCD D6 pin to digital pin 3
 * LCD D7 pin to digital pin 2
 * LCD R/W pin to 12 
 */

// include the library code:
#include <LiquidCrystal.h>

#define batt_1Pin  0
#define batt_2Pin  1
#define v1_add  11.14
#define v2_add  22.50
// initialize the library with the numbers of the interface pins

LiquidCrystal lcd(11, 12, 13, 5, 4, 3, 2);
int in_1 = 0;
int in_2 = 0;
float volt_1 = 0.0;
float volt_2 = 0.0;
float test = 0.0;
boolean flip = true;

void setup() {
  // set up the LCD's number of columns and rows: 
  lcd.begin(20, 4);
  analogReference(DEFAULT);
  Serial.begin(9600);
  
  // Print start message to the LCD.
  lcd.setCursor(6,0);
  lcd.print("ASS BOT");
  lcd.setCursor(4,1);
  lcd.print("POWERING UP");
  lcd.setCursor(2,2);
  lcd.print("monitoring in...");
  for(int i= 4; i > 0; i--){
    lcd.setCursor(9,3);
    lcd.print(i);
    delay(1000);
  }
  lcd.setCursor(1,3);
  lcd.print("ASS-POWER ONLINE!!");
  delay(1000);
}

void loop() {
  // set the cursor to column 0, line 1
  in_1 = analogRead(batt_1Pin);
  in_2 = analogRead(batt_2Pin);
  
  volt_1 = ( float(in_1) / 1023 ) * 5.0 + v1_add;
  volt_2 = ( ( float(in_2) / 1023 ) * 5.0 + v2_add ) - volt_1;
  
  lcd.clear();
  
  lcd.setCursor(5,0);
  lcd.print("ASS-POWER!");
  lcd.setCursor(0,2);
  lcd.print("Battery 1: ");
  if(volt_1 < 12.0) {
    if(flip)
      lcd.print("Low!!!");
  } else {
    lcd.print(volt_1);
    lcd.print("V");
  }
  lcd.setCursor(0,3);
  lcd.print("Battery 2: ");
  if(volt_2 < 12.0) {
    if(flip)
      lcd.print("Low!!!");
  } else {
    lcd.print(volt_2);
    lcd.print("V");
  }
  
  if(flip){
    Serial.print("{\"v1\":");
    Serial.print(volt_1);
    Serial.print(", \"v2\":");
    Serial.print(volt_2);
    Serial.print("}\r\n");
  }
  flip = !flip;
  delay(500);
}

