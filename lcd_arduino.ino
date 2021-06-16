
#include <LiquidCrystal.h> //biblioteca para uso do Display LCD

const int RS = 12, EN = 11, D4 = 10, D5 = 9, D6 = 8, D7 = 7;
LiquidCrystal lcd(RS, EN, D4, D5, D6, D7);

void setup(){
  Serial.begin(9600);
  lcd.begin(16, 2);
  lcd.print("start"); //mensagem inicial do Display LCD
 }

void loop(){
  if (Serial.available()) {
    delay(100);  //delay para obter o dado
    lcd.clear();
    while (Serial.available() > 0) {
      char c = Serial.read();
      lcd.write(c); //exibe o resultado proveniente do test.py
    }
  }
}
