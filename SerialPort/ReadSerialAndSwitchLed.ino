/*
Turn on or off a led using
A) single byte commands (eg., ‘A’. ‘S’)
*/
int LEDPIN = 13;

void setup()
{
  pinMode(LEDPIN, OUTPUT);
  Serial.begin(9600);
  digitalWrite(LEDPIN, LOW);
}

void loop()
{
  /*versione A*/

  char carattere;
  if (Serial.available())
  {
    carattere = Serial.read();
    Serial.print("carattere ricevuto: ");
    Serial.println(carattere);
    // led on-off
    if (carattere == 'A')
    {
      digitalWrite(LEDPIN, HIGH);
    }
    if (carattere == 'S')
    {
      digitalWrite(LEDPIN, LOW);
    }
  }
}
