/************************************************
   Universidade Federal do Rio de Janeiro
   Engenharia Eletrônica e da Computação
   DCM - Data Center Manager
   Aluno: Ewerton Vasconcelos da Silva
   Orientador: Rodrigo de Souza Couto
 *************************************************
   Emulador de Teclado USB baseado no Arduino pro micro / Leonardo
   Last update: 10/01/2021
  / *************************************************/
#include <HID-Project.h>
#include <HID-Settings.h>
unsigned int key;
int pinPower = 2;
int pinReset = 3;


String readString = "";
void setup() { // initialize the buttons' inputs:
  digitalWrite(pinPower, HIGH);
  digitalWrite(pinReset, HIGH);
  Serial1.begin(9600);
  Keyboard.begin();
}
void loop() {
  readString = "";
  while (Serial1.available()) {
    delay(5);
    if (Serial1.available() >0) {
      char c = Serial1.read();  //gets one byte from serial buffer     
      readString += c; //makes the string readString
    }
  }

if (readString.length()>0) {
    key = readString.toInt();
    // Serial.print("Arduino received: "); 
    // Serial.println(key); //see what was received
    
    if (key >= 200 ) {
      // Serial1.print("key coomand:");
      // Serial1.println(String(key));
      switch(key) {
        case 1000:
          BootKeyboard.write(KEY_UP_ARROW);
          delay(20);
        break;
        case 1001:
          BootKeyboard.write(KEY_DOWN_ARROW);
          delay(20);
        break;
        case 1002:
          BootKeyboard.write(KEY_LEFT_ARROW);
          delay(20);
        break;
        case 1003:
          BootKeyboard.write(KEY_RIGHT_ARROW);
          delay(20);
        break;
        case 1004:
          BootKeyboard.write(KEY_DELETE);
          delay(20);
        break;
        case 1005:
          BootKeyboard.write(KEY_ENTER);
          delay(20);
        break; 
        case 1006:
          BootKeyboard.write(KEY_ESC);
          delay(20);
        break;
        case 1007:
          BootKeyboard.write(KEY_BACKSPACE);
          delay(20);
        break;  
        case 1008:
          BootKeyboard.write(KEY_TAB);
          delay(20);
        break;
        case 1009:
          BootKeyboard.write(KEY_PRINTSCREEN);
          delay(20);
        break; 
        case 1010:
          BootKeyboard.write(KEY_HOME);
          delay(20);
        break; 
        case 1011:
          BootKeyboard.write(KEY_END);
          delay(20);
        break; 
        case 1012:
          BootKeyboard.write(KEY_INSERT);
          delay(20);
        break; 
        case 1013:
          BootKeyboard.write(KEY_PAGE_UP);
          delay(20);
        break;  
        case 1014:
          BootKeyboard.write(KEY_PAGE_DOWN);
          delay(20);
        break; 
        case 1015:
          BootKeyboard.write(KEY_LEFT_SHIFT);
          delay(20);
        break;
        case 1016:
          BootKeyboard.write(KEY_LEFT_ALT);
          delay(20);
        break;
        case 1017:
          BootKeyboard.write(KEY_RIGHT_CTRL);
          delay(20);
        break;
        case 1018:
          BootKeyboard.write(KEY_LEFT_GUI);
          delay(20);
        break;
        case 1019:
          BootKeyboard.press(KEY_RIGHT_CTRL);
          BootKeyboard.press(KEY_LEFT_ALT);
          BootKeyboard.press(KEY_DELETE);
          delay(100);
          BootKeyboard.releaseAll();
          delay(10);
        break;
        case 1020:
          BootKeyboard.write(KEY_NUM_LOCK);
          delay(20);
        break;
        case 1021:
          BootKeyboard.write(HID_KEYPAD_PIPE);
          delay(20);
        break;
        case 1022:
          BootKeyboard.press(KEY_LEFT_ALT);
          BootKeyboard.press(KEY_F4);
          delay(100);
          BootKeyboard.releaseAll();
          delay(10);
        break;
        case 1101:
          BootKeyboard.write(KEY_F1);
          delay(20);
        break;  
         case 1102:
          BootKeyboard.write(KEY_F2);
          delay(20);
        break;        
        case 1103:
          BootKeyboard.write(KEY_F3);
          delay(20);
        break;  
        case 1104:
          BootKeyboard.write(KEY_F4);
          delay(20);
        break;
        case 1105:
          BootKeyboard.write(KEY_F5);
          delay(20);
        break; 
        case 1106:
          BootKeyboard.write(KEY_F6);
          delay(20);
        break; 
        case 1107:
          BootKeyboard.write(KEY_F7);
          delay(20);
        break;
        case 1108:
          BootKeyboard.write(KEY_F8);
          delay(20);
        break;
        case 1109:
          BootKeyboard.write(KEY_F9);
          delay(20);
        break;
        case 1110:
          BootKeyboard.write(KEY_F10);
          delay(20);
        break;
        case 1111:
          BootKeyboard.write(KEY_F11);
          delay(20);
        break;
        case 1112:
          BootKeyboard.write(KEY_F12);
          delay(20);
        break;
        case 1200:
          digialWrite(pinPower, LOW);
          delay(1500);
          digitalWrite(pinPower, HIGH);
        break;
        case 1201:
          digitalWrite(pinReset, LOW);
          delay(1500);
          digitalWrite(pinReset, HIGH);
        break;
        default:
        break;
      }
    } else {
      // Serial1.print("key:");
      // Serial1.println(readString);
      BootKeyboard.print(readString);
    }

    readString = "";

      
}
}
