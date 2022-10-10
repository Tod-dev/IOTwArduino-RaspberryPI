// 2 fotoresistori che comunicano con il bridge tramite la porta seriale
const int analogPin1 = A0;
const int analogPin2 = A1;

int sensorValue1 = 0;
int sensorValue2 = 0;

const bool isVerboseToHuman = true;

void setup()
{
  Serial.begin(9600);
}

void loop()
{
  // read values
  sensorValue1 = analogRead(analogPin1);
  sensorValue2 = analogRead(analogPin2);

  // print the result to the serial Monitor
  if (isVerboseToHuman)
  {
    // versione per leggere i dati da una seriale (da un umano)
    Serial.print("sensor1 = ");
    Serial.print(sensorValue1);
    Serial.print("\t sensor2 = ");
    Serial.println(sensorValue2);
  }
  else
  {
    // versione per leggere i dati da una seriale (da un software, vedi bridge in python)
    // SCRIVO UN PACCHETTO DATI PER GARANTIRE L'ORDINE quando leggo dal bridge
    Serial.write(0xff);                                       // start
    Serial.write(0x02);                                       // numero di byte
    Serial.write((char)(map(sensorValue1, 0, 1024, 0, 253))); // mapping da 0 a 1024 del fotoresistore a 0-253, di un byte (char), 254 e 255 sono fe e ff che usiamo per identificare inizio e fine pacchetto
    Serial.write((char)(map(sensorValue2, 0, 1024, 0, 253)));
    Serial.write(0xfe); // start
  }
  // AD converter settle
  delay(2);
}
