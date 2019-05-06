from json import loads
from kafka import KafkaConsumer
consumer = KafkaConsumer('test', bootstrap_servers='130.65.159.69:9092', api_version=(0,10), group_id=None, auto_offset_reset='earliest', value_deserializer=lambda x: loads(x.decode('utf-8'))
for message in consumer:
    print(message)