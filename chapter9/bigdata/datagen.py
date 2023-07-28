import json
import csv
from google.cloud import pubsub_v1

project_name = 'dito-contact-center-ai-sandbox'
topic_name = 'sales'
file = 'Sales.csv'

publisher = pubsub_v1.PublisherClient()
topic_path = publisher.topic_path(project_name, topic_name)

with open(file) as filehandle:
    rd = csv.DictReader(filehandle, delimiter=',')
    for row in rd:
        data = json.dumps(dict(row))
        publisher.publish(topic_path, data=data.encode('utf-8'))