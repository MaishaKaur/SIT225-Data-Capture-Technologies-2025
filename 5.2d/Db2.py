import paho.mqtt.client as mqtt
from influxdb_client import InfluxDBClient, Point, WritePrecision
import json
import logging
import csv
import os
from datetime import datetime

# Setup logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# MQTT Configuration
MQTT_BROKER = "df50967215c74807987115a53bb0855d.s1.eu.hivemq.cloud"
MQTT_PORT = 8883
MQTT_TOPIC = "gyroscope/data"
MQTT_USERNAME = "hivemq.webclient.1742102354032"
MQTT_PASSWORD = "pxDq<:h5nIuR2*7E!3BJ"

# InfluxDB Configuration
INFLUX_URL = "https://us-east-1-1.aws.cloud2.influxdata.com"
INFLUX_TOKEN = "F6fYxxl2aOgmcy2fkqBsSOSl2j_27WWV5ZphlccuNlZyANb_gSyjnHjFpCfqZ0Fgk3Ri-p6BPH6iC0AlcOUAFw=="
INFLUX_ORG = "5.2d"
INFLUX_BUCKET = "gyro_data"

# CSV File Configuration
CSV_FILENAME = "gyro_data.csv"

# Ensure CSV file has a header if it doesn't exist
if not os.path.exists(CSV_FILENAME):
    with open(CSV_FILENAME, mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["timestamp", "x", "y", "z"])  # Write the header row

# Connect to InfluxDB
try:
    client = InfluxDBClient(url=INFLUX_URL, token=INFLUX_TOKEN, org=INFLUX_ORG)
    write_api = client.write_api()
    logging.info("Connected to InfluxDB successfully!")
except Exception as e:
    logging.error(f"Failed to connect to InfluxDB: {e}")
    exit(1)

# MQTT Callback - When message received
def on_message(client, userdata, msg):
    try:
        data = json.loads(msg.payload.decode())
        logging.info(f"Received Data: {data}")

        # Ensure timestamp exists or generate one
        timestamp = data.get("timestamp", datetime.utcnow().isoformat())

        # Create a point for InfluxDB
        point = Point("gyroscope") \
            .field("x", data["x"]) \
            .field("y", data["y"]) \
            .field("z", data["z"]) \
            .time(timestamp, WritePrecision.S)

        # Write to InfluxDB
        write_api.write(bucket=INFLUX_BUCKET, org=INFLUX_ORG, record=point)
        logging.info("Data written to InfluxDB successfully!")

        # Save Data to CSV
        with open(CSV_FILENAME, mode="a", newline="") as file:
            writer = csv.writer(file)
            writer.writerow([timestamp, data["x"], data["y"], data["z"]])
        logging.info("Data saved to CSV successfully!")

    except json.JSONDecodeError:
        logging.error("Failed to decode JSON data!")
    except KeyError as e:
        logging.error(f"Missing expected key: {e}")
    except Exception as e:
        logging.error(f"Error processing data: {e}")

# MQTT Setup with API Version 2
try:
    mqtt_client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
    mqtt_client.username_pw_set(MQTT_USERNAME, MQTT_PASSWORD)
    mqtt_client.tls_set()  # Secure Connection
    mqtt_client.on_message = on_message

    mqtt_client.connect(MQTT_BROKER, MQTT_PORT, 60)
    logging.info(f"Connected to MQTT Broker: {MQTT_BROKER}")

    mqtt_client.subscribe(MQTT_TOPIC)
    logging.info(f"Subscribed to MQTT Topic: {MQTT_TOPIC}")

    mqtt_client.loop_forever()
except Exception as e:
    logging.error(f"Failed to connect to MQTT Broker: {e}")
    exit(1)
