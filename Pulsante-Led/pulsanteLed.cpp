int ledPin = 13;   // Il led è connesso al pin 13
int pulsante = 12; // Il pulsante è connesso al pin 7
int val = 0;
/*NB: lo stesso circuito (Bottone e LED) si poteva fare solo con circuiteria
ma in questo modo abbiamo un digital twin, la copia digitale del
circuito e possiamo interagire con essa e fare delle elaborazioni
*/

/* ATTENZIONE !!!
  Questo è un circuito esemplificativo,
  non dobbiamo usare delay, ne altre funzioni bloccanti nella funzione loop() !
*/

void setup()
{
  Serial.begin(9600);
  pinMode(ledPin, OUTPUT);  // Il pin del led è un'uscita
  pinMode(pulsante, INPUT); // Il pin del pulsante è un'entrata
}

void loop()
{
  val = digitalRead(pulsante); // Lettura del pulsante
  Serial.println(val);
  if (val == HIGH)
  {                             // Se il valore del pulsante è HIGH
    digitalWrite(ledPin, HIGH); // Accendi il led
  }
  else
  {                            // Altrimenti:
    digitalWrite(ledPin, LOW); // Spegni il led
  }
  delay(100);
}
