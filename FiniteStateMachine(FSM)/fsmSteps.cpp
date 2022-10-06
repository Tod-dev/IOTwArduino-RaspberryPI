int ledPin = 13;   // Il led è connesso al pin 13
int pulsante = 12; // Il pulsante è connesso al pin 7
int val = 0;
// v4
int oldTime;
int buttonState, ledState;
// v5
int previousState;
// v6
// input & output pins
const int inPin = 12;
const int outPin = 13;
// input simbols = 0:released, 1:pressed
int inSymb;
// states = 0:A, 1:B , 2:C , 3:D
int state, futureState;

/*NB: lo stesso circuito (Bottone e LED) si poteva fare solo con circuiteria
ma in questo modo abbiamo un digital twin, la copia digitale del
circuito e possiamo interagire con essa e fare delle elaborazioni
*/
void setup()
{
  Serial.begin(9600);
  pinMode(ledPin, OUTPUT);  // Il pin del led è un'uscita
  pinMode(pulsante, INPUT); // Il pin del pulsante è un'entrata
  // v4
  buttonState = 0;
  ledState = 0;
  oldTime = millis();
  // v5
  previousState = 0;
  // v6
  pinMode(inPin, INPUT);
  pinMode(outPin, OUTPUT);
  // initialState
  state = 0;
}

void loop()
{
  /*
  //v1 - v2 con Serial.println(val);
  val = digitalRead(pulsante);  //Lettura del pulsante
  Serial.println(val);
  if (val == HIGH){  //Se il valore del pulsante è HIGH
    digitalWrite(ledPin, HIGH);  //Accendi il led
  }
  else {  //Altrimenti:
    digitalWrite(ledPin, LOW);  //Spegni il led
  }
  delay(100);
  */
  // v3 - quando tengo premuto il pulsante, il led lampeggia 500ms on , 500ms off, altrimenti spento
  /*
   val = digitalRead(pulsante);
   if(val == HIGH){
     digitalWrite(ledPin, HIGH);
     delay(500);
     digitalWrite(ledPin, LOW);
     delay(500);
   }else{
     digitalWrite(ledPin, LOW);
   }
   */
  // Non funziona se ho un altro bottone con un altro led -> Il DELAY è bloccante!!!
  // come possiamo fare senza DELAY, cosi da modularizzare il nostro sistema -> millis()
  // v4
  /*
  buttonState = digitalRead(pulsante);
  int freq = 100;
  if((ledState == 1 && buttonState ==1 && (millis()-oldTime)>freq) || buttonState==0){
    oldTime = millis();
    digitalWrite(ledPin,LOW);
    ledState=0;
  }
  if(ledState == 0 && buttonState ==1 && (millis()-oldTime)>freq){
    oldTime = millis();
    digitalWrite(ledPin,HIGH);
    ledState=1;
  }
  */
  // ora il loop gira velocemente -> non abbiamo inserito codice bloccante
  //è molto importante non usare codice bloccante su microcontrollori!!!
  // La funzione Loop DEVE girare velocemente
  // v5 toggle del led
  /*
  buttonState = digitalRead(pulsante);
  int freq = 100;
  if(buttonState == HIGH && previousState == LOW){
     if(ledState == 0 ){
      digitalWrite(ledPin,HIGH);
      ledState=1;
     }else{
      digitalWrite(ledPin,LOW);
      ledState=0;
     }
  }
  previousState = buttonState;
  */
  // v6 - macchina a stati finiti (FSM) -> tantissimi vantgaggi (semplicità, modularità...) -> fare a corredo il diagramma degli stati
  // 1. read external inputs and generate input symbols -> divide la lettura del sensore reale dal valore simbolico della macchina a stati -> disaccoppiamento, facile cambiare poi il sensore
  int inVal = digitalRead(inPin);
  if (inVal == LOW)
    inSymb = 0;
  else
    inSymb = 1;

  // 2. future state estimation -> è una traduzine del diagramma degli stati
  switch (state)
  {
  case 0:
  {
    if (inSymb == 1) // press
      futureState = 1;
    if (inSymb == 0) // release
      futureState = 0;
    break;
  }
  case 1:
  {
    if (inSymb == 1) // press
      futureState = 1;
    if (inSymb == 0) // release
      futureState = 2;
    break;
  }
  case 2:
  {
    if (inSymb == 1) // press
      futureState = 3;
    if (inSymb == 0) // release
      futureState = 2;
    break;
  }
  case 3:
  {
    if (inSymb == 1) // press
      futureState = 3;
    if (inSymb == 0) // release
      futureState = 0;
    break;
  }
  }
  // 3. OnEntry && OnExit actions, if required
  // if(state == A && futureState == B){}

  // 4. state transition (clock edge)
  state = futureState;

  // 5. update the output [Moore -> dipende solo dallo stato attuale e non dall'ingresso]
  switch (state)
  {
  case 0:
  case 3:
    digitalWrite(outPin, LOW);
    break;
  case 1:
  case 2:
    digitalWrite(outPin, HIGH);
    break;
  }
}
