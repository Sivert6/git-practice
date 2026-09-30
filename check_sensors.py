import json

import pandas as pd    # Leser CSV og Excel som tabeller.
import yaml            # Leser .yml-filer

#___________________________________________________________________________________________________
# Steg 1: Les instillinger 
#___________________________________________________________________________________________________
with open("config.yml") as f:
    config = yaml.safe_load(f)     # Gjør innholdet om til en dictionary

max_days = config["max_days_since_calibration"]  # Hent ut maks antall dager fra config - 180
output_file = config["output_file"]  # Navnet på resultat

#print(max_days, output_file) # Sjekker at jeg får riktige verdier fra config!

#___________________________________________________________________________________________________

# Steg 2: Les inn dataene
#___________________________________________________________________________________________________

# Excel-filen sier hvor sensoren står og hvem som eier den,
# CSV-filen sier hvor lenge siden den ble kalibrert.

sensors = pd.read_excel("sensors.xlsx")  # Leser inn sensordata fra Excel
calibrations = pd.read_csv("calibrations.csv")  # Leser inn kalibreringsdata fra CSV-filen

#print(sensors)
#print(calibration)

#___________________________________________________________________________________________________
# Steg 3: Koble sammen tabellene og finn sensorene som er over grensen
#___________________________________________________________________________________________________
merged = pd.merge(sensors, calibrations, on="sensor_id")         # Kobler radene som har samme sensor_id
overdue = merged[merged["days_since_calibration"] > max_days]    # Beholder bare radene over 180 dager

#print(overdue)          # Sjekker resultatet

#___________________________________________________________________________________________________
# Steg 4: Lagre resultatet som JSON
#___________________________________________________________________________________________________

alerts = overdue.to_dict(orient="records")   # Gjør tabellen om til en liste med én dictionary per sensor

with open(output_file, "w") as f:            # Åpner filen for skriving ("w" = write). Lages hvis den ikke finnes
    json.dump(alerts, f, indent=2)           # Skriver listen som JSON, med innrykk på 2 så den er lett å lese

print(f"Fant {len(alerts)} sensorer som må kalibreres. Lagret i {output_file}")

