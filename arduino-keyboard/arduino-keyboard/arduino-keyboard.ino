/************************************************
 * Universidade Federal do Rio de Janeiro
 * Engenharia Eletrônica e da Computação
 * DCM - Data Center Manager
 * Aluno: Ewerton Vasconcelos da Silva
 * Orientador: Rodrigo de Souza Couto 
 *************************************************
 * Emulador de Teclado PS2 baseado no Arduino pro Mini
 * Last update: 16/12/2020
/ *************************************************/

#include <ps2dev.h>    //Emulate a PS/2 device
PS2dev keyboard(3,2);  //clock, data

unsigned long timecount = 0;
int incomingByte = 0; 
String readString = "";
int key;
unsigned char leds;

void setup()
{
  keyboard.keyboard_init();
  Serial.begin(9600);
  pinMode(LED_BUILTIN, OUTPUT);
}


void loop()
{

  
  if(keyboard.keyboard_handle(&leds)) {
    //Serial.print('LEDS');
    //Serial.print(leds, HEX);
    digitalWrite(LED_BUILTIN, leds);
  }
  
  while (!Serial.available()) {} // wait for data to arrive
  // serial read section
  while (Serial.available())
  {
     delay(2);
     if (Serial.available() >0)
    {
      char c = Serial.read();  //gets one byte from serial buffer
      readString += c; //makes the string readString
    }
    
  }

  if (readString.length() > 0)
  {
    Serial.print("Arduino received: "); 
    Serial.println(readString.toInt(),HEX); //see what was received
    key = readString.toInt();

    if (key > 2000 ) {
      keyboard.keyboard_special_mkbrk(key-2000);
    } else {
      keyboard.keyboard_mkbrk(key);  
    }

    readString = "";

  } 

 
/*
  if (Serial.available() > 0) {
    incomingByte = Serial.read();
    Serial.print("I received: ");
    Serial.println(incomingByte,HEX);
    //keyboard.keyboard_mkbrk(incomingByte);
  }
 

  
  //Print letter every second
   if((millis() - timecount) > 1000) {
    keyboard.keyboard_mkbrk(0x16); //Make + Break key
    Serial.print('.');
    timecount = millis();
  }*/
}
