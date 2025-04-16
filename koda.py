#!/usr/bin/env python3
import adafruit_dht as Adafruit_DHT
import json
import datetime
import os
import time
from git import Repo

# Nastavitve
SENSOR_TYPE = Adafruit_DHT.DHT22
GPIO_PIN = 4
REPO_PATH = '/home/pi/temperature-data'  # Pot do vašega Git repozitorija
DATA_FILE = os.path.join(REPO_PATH, 'data/temperature.json')
LOG_FILE = os.path.join(REPO_PATH, 'log.txt')

def log_error(message):
    with open(LOG_FILE, 'a') as f:
        f.write(f"{datetime.datetime.now()}: {message}\n")

def main():
    # Inicializacija Git repozitorija
    try:
        repo = Repo(REPO_PATH)
    except Exception as e:
        log_error(f"Napaka pri odpiranju repozitorija: {str(e)}")
        return

    # Branje temperature
    try:
        humidity, temperature = Adafruit_DHT.read_retry(SENSOR_TYPE, GPIO_PIN)
        if temperature is None:
            log_error("Napaka pri branju senzorja")
            return

        # Ustvari nov zapis
        new_entry = {
            "temperature": round(temperature, 1),
            "humidity": round(humidity, 1),
            "timestamp": datetime.datetime.utcnow().isoformat() + "Z"
        }

        # Preberi obstoječe podatke ali ustvari novo datoteko
        if os.path.exists(DATA_FILE):
            with open(DATA_FILE, 'r') as f:
                try:
                    data = json.load(f)
                    if not isinstance(data, list):
                        data = [data]
                except json.JSONDecodeError:
                    data = []
        else:
            data = []

        # Dodaj nov zapis
        data.append(new_entry)
        
        # Ohrani samo zadnjih 100 meritev
        if len(data) > 100:
            data = data[-100:]

        # Shrani podatke
        with open(DATA_FILE, 'w') as f:
            json.dump(data, f, indent=2)

        # Posodobi Git
        repo.git.add(DATA_FILE)
        repo.git.commit('-m', f"Avtomatska posodobitev: {new_entry['temperature']}°C")
        origin = repo.remote(name='origin')
        origin.push()

        print(f"Uspešno posodobljeno: {new_entry['temperature']}°C")

    except Exception as e:
        log_error(f"Napaka v glavni zanki: {str(e)}")

if __name__ == '__main__':
    while True:
        main()
        time.sleep(300)  # Počakaj 5 minut med meritvami
