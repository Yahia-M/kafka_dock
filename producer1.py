from kafka import KafkaProducer
from pymongo import MongoClient
import json

# MongoDB Atlas connection
mongo_uri = "mongodb+srv://dbGDR:dbYahiaUsers@cluster-gdr.yogka.mongodb.net/?retryWrites=true&w=majority&appName=Cluster-GDR"
client = MongoClient(mongo_uri)
db = client['mongodbVSCodePlaygroundDB']
collection = db['sales']

# Kafka producer setup
producer = KafkaProducer(
    bootstrap_servers='localhost:9092',  # Use the correct broker address
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

# Read data from MongoDB and produce to Kafka
for document in collection.find():
    producer.send('<kafka_topic>', document)
    print(f"Produced: {document}")

producer.flush()