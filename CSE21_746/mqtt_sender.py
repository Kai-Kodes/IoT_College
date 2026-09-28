import paho.mqtt.client as mqtt
import json
import time

broker="localhost"

topic="sensor/temp"

payload={
    "device_id": "ESP32_001",
    "temperature": 25.5,
    "humidity": 60
}

client = mqtt.Client()

client.connect(broker,1883)

start=time.time()

client.publish(topic,json.dumps(payload))

end=time.time()

print("Published")

print("Time taken to publish message: ", end-start, "seconds")

