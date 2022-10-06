/*
Turn on or off a led using
B) multiple byte commands (eg., «ON» or «OFF»)
*/
int LEDPIN = 13;
int state;
// states = 0:A(nessun carattere valido), 1:B(digitata O) ,
// 2:C(digitata N dopo O) , 3:D(digitata F dopo O), 4:E(digitata F dopo OFF)

void setup()
{
  pinMode(LEDPIN, OUTPUT);
  Serial.begin(9600);
  digitalWrite(LEDPIN, LOW);
  state = 0;
}

void loop()
{
  // 1. read external inputs and generate input symbols
  //-> divide la lettura del sensore reale dal valore simbolico della macchina a stati
  //-> disaccoppiamento, facile cambiare poi il sensore

  char inputSymbol = -1; // input simbols = inputValue in questo caso
  char inputValue;
  if (Serial.available())
  {
    inputValue = Serial.read();
    Serial.print("carattere ricevuto: ");
    Serial.println(inputValue);
    inputSymbol = inputValue;
  }
  // 2. future state estimation -> è una traduzine del diagramma degli stati
  if (inputSymbol == -1)
    return; // non ho letto nessun carattere
  int futureState = 0;
  switch (state)
  {
  case 0:
  case 2:
  case 4:
  {
    if (inputSymbol == 'O')
      futureState = 1;
    break;
  }

  case 1:
  {
    if (inputSymbol == 'N')
      futureState = 2;
    if (inputSymbol == 'F')
      futureState = 3;
    break;
  }

  case 3:
  {
    if (inputSymbol == 'F')
      futureState = 4;
    break;
  }
  }
  // 3. OnEntry && OnExit actions, if required
  // if(state == A && futureState == B){}

  // 4. state transition (clock edge)
  state = futureState;
  Serial.print("NUOVO STATO ATTUALE: ");
  Serial.println(state);

  // 5. update the output [Moore -> dipende solo dallo stato attuale e non dall'ingresso]
  switch (state)
  {
  case 2:
    digitalWrite(LEDPIN, HIGH);
    break;
  case 4:
    digitalWrite(LEDPIN, LOW);
    break;
  }
}
