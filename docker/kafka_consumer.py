# Before running this program run pip install kafka-python
from __future__ import print_function
from kafka import KafkaConsumer
from json import loads

import os, sys


print("App started X")


consumer = KafkaConsumer(
    'demo-transactions',
    bootstrap_servers=[os.environ['BROKER_SERVICE']],
    auto_offset_reset='earliest')

consumer.subscribe(["transactions"])

print("E")
for message in consumer:
    message = message.value
    print('Message: {}'.format(message))

print("End of consumer reader")