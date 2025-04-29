import serial
import json
import firebase_admin
from firebase_admin import credentials, db
import time

# Firebase setup
cred = credentials.Certificate("maisha-1fe9c-firebase-adminsdk-fbsvc-7920c9b939.json")
firebase_admin.initialize_app(cred, {"databaseURL": "https://maisha-1fe9c-default-rtdb.firebaseio.com/"})

ref = db.reference("GyroscopeData")  # Firebase database reference

# Open serial port (adjust COM port accordingly)
ser = serial.Serial("COM20", 115200, timeout=1)

try:
    while True:
        line = ser.readline().decode("utf-8").strip()
        if line:
            try:
                # Split CSV data
                timestamp, x, y, z = line.split(",")
                data = {
                    "timestamp": int(timestamp),
                    "x": float(x),
                    "y": float(y),
                    "z": float(z)
                }

                # Upload data to Firebase
                ref.push(data)
                print(f"Uploaded: {data}")

            except ValueError:
                print("Invalid data format, skipping...")
except KeyboardInterrupt:
    print("Stopping data collection.")
    ser.close()

import json
import pandas as pd
from firebase_admin import db

ref = db.reference("GyroscopeData")  
data = ref.get()

if data:
    df = pd.DataFrame(data.values())
    df = df.sort_values("timestamp")  # Sort by time
    df.to_csv("gyroscope_data.csv", index=False)
    print("Data saved to gyroscope_data.csv")
else:
    print("No data found in Firebase.")