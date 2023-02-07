#include <Keypad.h>
#include <LedControl.h>

const byte ROWS = 4;
const byte COLS = 4;

const int PAGE_NUMBER = 3;

;char hexaKeys[ROWS][COLS] = {
  {'F','E','D','C'},
  {'B','A','9','8'},
  {'7','6','5','4'},
  {'3','2','1','0'}
};

byte rowPins[ROWS] = {13, 12, 11, 10};
byte colPins[COLS] = {9, 8, 7, 6}; 

Keypad customKeypad = Keypad( makeKeymap(hexaKeys), rowPins, colPins, ROWS, COLS); 

LedControl lc=LedControl(A0,A2,A1,1);

unsigned long delaytime1=500;
unsigned long delaytime2=50;
int currentPage = 0;

const int mutePin = 3;
const int muteLED = 5;
bool muteSwitch = false;
int muteCurrent = 0;

const int buttonLED = 4;

unsigned long buttonsCD = 0;

unsigned char letters[PAGE_NUMBER][8] = {{B00000000, B00000001, B00000001, B01111111, B01000001, B00100001, B00010000, B00000000}, {B00000000, B00110001, B01001001, B01001001, B01001001, B01001001, B01000110, B00000000}, {B00000000, B00110110, B01001001, B01001001, B01001001, B01001001, B01000001, B00000000}};

const int buttonsPin = A5;
int buttonsCurrent;

void setup() {
  lc.shutdown(0,false);
  lc.setIntensity(0,8);
  lc.clearDisplay(0);
  Serial.begin(9600);
  pinMode(buttonsPin, INPUT_PULLUP);
  pinMode(mutePin, INPUT_PULLUP);
  pinMode(muteLED, OUTPUT);
  pinMode(buttonLED, OUTPUT);
}

void displayPage() {
  int j = 0;
    while (j < 8) {
      lc.setRow(0,j,letters[currentPage][j]); 
      j += 1;
    }
}

void blinkLight() {
  digitalWrite(buttonLED, HIGH);
  delay(100);
  digitalWrite(buttonLED, LOW);
}

void loop() { 
  displayPage();

  char customKey = customKeypad.getKey();
  buttonsCurrent = analogRead(buttonsPin);
  muteCurrent = digitalRead(mutePin);
  if (millis() - buttonsCD >= 300) {
    if (muteCurrent == LOW) {
      Serial.println("Mute");
      muteSwitch = !muteSwitch;
      if (muteSwitch) {
        digitalWrite(muteLED, HIGH);
      } else {
        digitalWrite(muteLED, LOW);
      }
      buttonsCD = millis();
    }
    if (buttonsCurrent >= 910 && buttonsCurrent <= 950) {
      currentPage -= 1;
      if (currentPage == -1) {
        currentPage += PAGE_NUMBER;
      }
      buttonsCD = millis();
      blinkLight();
    } else if (buttonsCurrent >= 975 && buttonsCurrent <= 1040) {
      currentPage += 1;
      currentPage %= PAGE_NUMBER;
      buttonsCD = millis();
      blinkLight();
    }
  }
   if (customKey){
    Serial.print("{\"page\": \"");
    Serial.print(currentPage);
    Serial.print("\", \"action\": \"");
    Serial.print(customKey);
    Serial.println("\"}");
    blinkLight();
  }
}
