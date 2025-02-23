from kafka import KafkaProducer
from pymongo import MongoClient
import os
import json
import time

# Kafka configuration
kafka_broker = 'kafka:9092'
topic = 'mongo_data'

# MongoDB connection
# mongo_uri = os.getenv("MONGODB_URI")
# client = MongoClient(mongo_uri)
# db = client['mongodbVSCodePlaygroundDB']
# collection = db['sales']

# Connect to MongoDB
mongo_uri = "mongodb+srv://dbGDR:dbYahiaUsers@cluster-gdr.yogka.mongodb.net/?retryWrites=true&w=majority&appName=Cluster-GDR"

client = MongoClient(mongo_uri)
db = client['mongodbVSCodePlaygroundDB']
coll = db['sales']

# Kafka producer
producer = KafkaProducer(bootstrap_servers=kafka_broker, value_serializer=lambda v: json.dumps(v).encode('utf-8'))

# Function to fetch data from MongoDB and send to Kafka
def fetch_and_send_data():
    for document in coll.find():
        producer.send(topic, value=document)
        print(f"Produced: {document}")
    producer.flush()

# Loop to resend data every 5 seconds
while True:
    fetch_and_send_data()
    print("Waiting for 5 seconds before resending data...")
    time.sleep(5)  # Wait for 5 seconds