<<<<<<< HEAD
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
=======
import json
import datetime
import os
import time
import board
import adafruit_dht
from git import Repo  # Knjižnica za Git

# Nastavitve
DHT_PIN = board.D4  # GPIO4
REPO_PATH = "/home/pi/temperature-data"  # Pot do tvojega Git repozitorija
GIT_REMOTE = "origin"  # Git remote (običajno 'origin')

# Inicializacija
dht = adafruit_dht.DHT22(DHT_PIN)
repo = Repo(REPO_PATH)

def measure_and_save():
    try:
        temperature = dht.temperature
        podatki = {
            "temperatura": round(temperature, 1),
            "cas": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
        # Shrani lokalno
        with open(f"{REPO_PATH}/podatki.json", "w") as datoteka:
            json.dump(podatki, datoteka, indent=2)
        
        # Push na GitHub
        repo.git.add("podatki.json")
        repo.git.commit("-m", f"Avtomatska posodobitev: {podatki['temperatura']}°C")
        repo.git.push(GIT_REMOTE, "main")
        
        print(f"Posodobljeno: {podatki['temperatura']}°C | Čas: {podatki['cas']}")
    
    except Exception as e:
        print(f"Napaka: {str(e)}")

# Glavna zanka
try:
    while True:
        measure_and_save()
        time.sleep(300)  # Meri vsakih 5 minut (300 sekund)
        
except KeyboardInterrupt:
    print("Ustavljam...")
    dht.exit()
>>>>>>> 44511f3 (posodobitev)
