import serial
import json
import firebase_admin
from firebase_admin import credentials, db
import time

cred = credentials.Certificate("maisha-1fe9c-firebase-adminsdk-fbsvc-7920c9b939.json")
firebase_admin.initialize_app(cred, {"databaseURL": "https://maisha-1fe9c-default-rtdb.firebaseio.com/GyroscopeData/-OKVOIIO7rSFuCp5ssQ-"})

ref = db.reference("GyroscopeData") 

ser = serial.Serial("COM20", 115200, timeout=1)

try:
    while True:
        line = ser.readline().decode("utf-8").strip()
        if line:
            try:
                timestamp, x, y, z = line.split(",")
                data = {
                    "timestamp": int(timestamp),
                    "x": float(x),
                    "y": float(y),
                    "z": float(z)
                }

                ref.push(data)
                print(f"Uploaded: {data}")

            except ValueError:
                print("Invalid data format, skipping...")
except KeyboardInterrupt:
    print("Stopping data collection.")
ser.close()