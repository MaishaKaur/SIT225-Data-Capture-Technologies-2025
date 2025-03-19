import paho.mqtt.client as mqtt
import json
import csv
import os
import datetime
from pymongo import MongoClient

# MQTT Configuration
MQTT_BROKER = "3cbcfcc04ebd4ed8b9ed004eea65a1c3.s1.eu.hivemq.cloud"
MQTT_PORT = 8883  # Secure MQTT port
MQTT_TOPIC = "gyroscope/data"
MQTT_USERNAME = "hivemq.webclient.1742102354032"
MQTT_PASSWORD = "pxDq<:h5nIuR2*7E!3BJ"

# MongoDB Configuration
MONGO_URI = "mongodb+srv://maisha4829se24:DZkPtoB2K46NEXxS@maisha.z6ssk.mongodb.net/?retryWrites=true&w=majority&appName=Maisha"
DB_NAME = "maisha4829se24"
COLLECTION_NAME = "Gyroscope"

# CSV File Configuration
CSV_FILE = "new_gyroscope_data.csv"

# Ensure CSV file has headers if it doesn't exist
if not os.path.exists(CSV_FILE):
    with open(CSV_FILE, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["timestamp", "x", "y", "z"])  # Assuming gyroscope data has x, y, z values

# Connect to MongoDB
try:
    mongo_client = MongoClient(MONGO_URI)
    mongo_client.admin.command('ping')  # Check if MongoDB is reachable
    db = mongo_client[DB_NAME]
    collection = db[COLLECTION_NAME]
    print("MongoDB connection successful")
except Exception as e:
    print(f"MongoDB Connection Failed: {e}")
    exit(1)

# MQTT Callback when a message is received
def on_message(client, userdata, message):
    print(f"\nRaw message received: {message.payload}")  # Print raw data

    try:
        data = json.loads(message.payload.decode())  # Decode JSON
        print("Decoded JSON:", data)

        if isinstance(data, dict):  # Ensure it's a valid dictionary
            # Add timestamp
            timestamp = datetime.datetime.now().isoformat()
            data["timestamp"] = timestamp

            # Store data in MongoDB
            collection.insert_one(data)
            print("Data inserted into MongoDB")

            # Save data to CSV
            with open(CSV_FILE, mode='a', newline='') as file:
                writer = csv.writer(file)
                writer.writerow([timestamp, data.get("x", ""), data.get("y", ""), data.get("z", "")])

            print("Data saved to CSV file")

        else:
            print("Invalid data format (not a JSON object), skipping...")

    except json.JSONDecodeError:
        print("Invalid JSON received, skipping...")

# MQTT Setup
mqtt_client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
mqtt_client.username_pw_set(MQTT_USERNAME, MQTT_PASSWORD)
mqtt_client.tls_set()  # Enable SSL for secure connection
mqtt_client.on_message = on_message

# Connect to MQTT Broker
try:
    mqtt_client.connect(MQTT_BROKER, MQTT_PORT)
    print("Connected to MQTT broker")
except Exception as e:
    print(f"Failed to connect to MQTT broker: {e}")
    exit(1)

# Subscribe to the MQTT topic
mqtt_client.subscribe(MQTT_TOPIC)
print(f"Subscribed to topic: {MQTT_TOPIC}")

# Start listening for messages
mqtt_client.loop_forever()