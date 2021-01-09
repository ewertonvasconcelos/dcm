/************************************************
   Universidade Federal do Rio de Janeiro
   Engenharia Eletrônica e da Computação
   DCM - Data Center Manager
   Aluno: Ewerton Vasconcelos da Silva
   Orientador: Rodrigo de Souza Couto
 *************************************************
   Emulador de Teclado USB baseado no Arduino pro micro / Leonardo
   Last update: 08/01/2021
  / *************************************************/

#include "Keyboard.h"


String readString = "";
void setup() { // initialize the buttons' inputs:

  Serial1.begin(9600);
  // initialize mouse control:
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

  for (int i=0; i<readString.length(); i++) {
    if(readString[i] > 127 && readString[i] < 300) {
      Keyboard.write(readString[i]);
     } else {
      Keyboard.print(readString[i]);
    }
  }
  readString=""; 
      
}