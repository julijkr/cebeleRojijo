import Adafruit_DHT
import json
import datetime
import os

# Nastavi senzor
senzor = Adafruit_DHT.DHT22
pin = 4

# Preberi temperaturo
vlaznost, temperatura = Adafruit_DHT.read_retry(senzor, pin)

# Shrani podatke
podatki = {
    "temperatura": round(temperatura, 1),
    "cas": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
}

with open("podatki.json", "w") as datoteka:
    json.dump(podatki, datoteka)

print("Temperatura:", podatki["temperatura"], "°C")