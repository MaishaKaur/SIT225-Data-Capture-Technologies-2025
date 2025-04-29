import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("gyroscope_data.csv")

df.dropna(inplace=True)

df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms")
df["x"] = pd.to_numeric(df["x"], errors="coerce")
df["y"] = pd.to_numeric(df["y"], errors="coerce")
df["z"] = pd.to_numeric(df["z"], errors="coerce")


plt.figure(figsize=(10, 5))

plt.subplot(3, 1, 1)
plt.plot(df["timestamp"], df["x"], label="X-axis", color="r")
plt.legend()

plt.subplot(3, 1, 2)
plt.plot(df["timestamp"], df["y"], label="Y-axis", color="g")
plt.legend()

plt.subplot(3, 1, 3)
plt.plot(df["timestamp"], df["z"], label="Z-axis", color="b")
plt.legend()

plt.tight_layout()
plt.show()

plt.figure(figsize=(10, 5))
plt.plot(df["timestamp"], df["x"], label="X-axis", color="r")
plt.plot(df["timestamp"], df["y"], label="Y-axis", color="g")
plt.plot(df["timestamp"], df["z"], label="Z-axis", color="b")
plt.legend()
plt.xlabel("Timestamp")
plt.ylabel("Gyroscope Readings")
plt.title("Gyroscope Sensor Data")
plt.show()