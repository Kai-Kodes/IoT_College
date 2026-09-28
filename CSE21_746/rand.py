import paho.mqtt.client as mqtt
import json
import time
import sys

# HiveMQ Cloud details
broker = "bd52cc82527c4023b96ce2ebc5298a34.s1.eu.hivemq.cloud"
port = 8883
username = "RedSheronin"
password = "fuckfuckfuckfuck"
topic = "sensor/temp"

payload = {
    "device_id": "ESP32_001",
    "temperature": 25.4,
    "humidity": 60
}

# Connection callback to catch network failures
def on_connect(client, userdata, flags, rc, properties=None):
    if rc == 0:
        print("Successfully connected to HiveMQ Cloud!")
    else:
        print(f"Connection failed! Error code (rc): {rc}")
        print("Tip: Check your username, password, or cluster status.")
        sys.exit(1) # Stop script execution immediately on error

# Initialize client using Callback API Version 2
client = mqtt.Client(callback_api_version=mqtt.CallbackAPIVersion.VERSION2)
client.on_connect = on_connect

# Authentication & TLS Configuration
client.username_pw_set(username, password)
client.tls_set()  # Necessary for secure port 8883

print("Connecting to HiveMQ Cloud...")

try:
    # Set a 15-second keepalive timeout to prevent endless hanging
    client.connect(broker, port, keepalive=15)
except Exception as e:
    print(f"\nCould not reach the broker: {e}")
    print("Please check your internet connection or firewall rules.")
    sys.exit(1)

# Start the background network thread
client.loop_start()

# Give the background loop a brief moment to process the connection handshake
time.sleep(2)

# Measure real publishing time
start = time.time()
result = client.publish(topic, json.dumps(payload), qos=1)

print("Waiting for cloud confirmation...")
result.wait_for_publish()
end = time.time()

print("Published successfully!")
print("Real Cloud Latency :", round((end - start) * 1000, 2), "ms")

# Cleanly stop the loop and disconnect
client.loop_stop()
client.disconnect()