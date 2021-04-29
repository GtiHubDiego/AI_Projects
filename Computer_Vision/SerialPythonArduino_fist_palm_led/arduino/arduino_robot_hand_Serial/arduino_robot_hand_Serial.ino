#include <Servo.h>
unsigned long lastTime,sampleTime; // Tiempo muestreo 

String inputString = "";  // Almacenar la cadena recibida   
bool stringComplete = false;// Indicar que ha recibido una cadena
const char separator = ','; // Separador (,)
const int dataLength = 2; // Cantidad de datos que vamos recibir
double data[dataLength]; // Vector que va almacenar los datos recibidos


Servo servoMotor_mano,servoMotor_brazo;
void setup() {

  Serial.begin(9600); // Configurar los baudios 
  
  sampleTime = 100; // Tiempo de muestreo 100ms
  lastTime = millis(); // Tiempo transcurrido
  pinMode(13, OUTPUT);

  servoMotor_mano.attach(10);
  servoMotor_mano.write(0);

  servoMotor_brazo.attach(11);
  servoMotor_brazo.write(90);
 
}

  // Para el sentido negativo
  void close(){
    for (int i = 115; i >110; i--)
    {
      // Desplazamos al ángulo correspondiente
      servoMotor_mano.write(i);
      // Hacemos una pausa de 25ms
      delay(25);
    }
  }

//65 totalmente abierto

 void open(){
    for (int i = 110; i >65; i--)
    {
      // Desplazamos al ángulo correspondiente
      servoMotor_mano.write(i);
      // Hacemos una pausa de 25ms
      delay(25);
    }
  }


void loop() {
  
 
  if (stringComplete) 
  {
    for (int i = 0; i < dataLength ; i++)
    {
      int index = inputString.indexOf(separator);
      data[i] = inputString.substring(0, index).toFloat();
      inputString = inputString.substring(index + 1);
    }
    inputString = "";
    stringComplete = false;

  }
     if (data[0] == 10) {
        digitalWrite(13, LOW);
        servoMotor_mano.write(65);
        //servoMotor_brazo.write(90);
     }else if(data[0] == 11){
        digitalWrite(13, HIGH);
        servoMotor_mano.write(110);
     }else if  (data[0] == 12){
        digitalWrite(13, LOW);
        servoMotor_brazo.write(70);
     }else if  (data[0] == 13){
        digitalWrite(13, HIGH);
        servoMotor_brazo.write(110);
     }
     data[0]=0;
     

 if (millis()-lastTime >= sampleTime)
 {
  lastTime=millis();
  Serial.println(data[0],3);
 }

}

void serialEvent() {
  while (Serial.available()) {
    char inChar = (char)Serial.read();
    inputString += inChar;
    if (inChar == '\n') {
      stringComplete = true;
    }
  }
}
