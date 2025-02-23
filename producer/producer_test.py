from kafka import KafkaProducer
from pymongo import MongoClient
import json
import os

# MongoDB connection
mongo_uri = os.getenv("MONGO_URI")
client = MongoClient(mongo_uri)
db = client['mongodbVSCodePlaygroundDB']
collection = db['sales']

# Kafka producer setup
producer = KafkaProducer(
    bootstrap_servers=os.getenv("KAFKA_BOOTSTRAP_SERVERS"),
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

# Read data from MongoDB and produce to Kafka
for document in collection.find():
    producer.send(os.getenv("KAFKA_TOPIC"), document)
    print(f"Produced: {document}")

producer.flush()