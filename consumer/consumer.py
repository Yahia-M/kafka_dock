from kafka import KafkaConsumer
from flask import Flask, jsonify
import json
import os

app = Flask(__name__)

# Kafka consumer setup
consumer = KafkaConsumer(
    os.getenv("KAFKA_TOPIC"),
    bootstrap_servers=os.getenv("KAFKA_BOOTSTRAP_SERVERS"),
    value_deserializer=lambda x: json.loads(x.decode('utf-8'))
)

# In-memory storage for consumed messages
messages = []

def consume_messages():
    for message in consumer:
        messages.append(message.value)
        print(f"Consumed: {message.value}")

# Start Kafka consumer in a separate thread
import threading
threading.Thread(target=consume_messages, daemon=True).start()

# Flask API to expose consumed messages
@app.route('/messages', methods=['GET'])
def get_messages():
    return jsonify(messages)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)