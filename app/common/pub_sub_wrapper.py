from google.cloud import pubsub_v1
import json


class PubSubWrapper:
    project_id = 'aplicaciones-en-la-nube-382813'
    topic_name = 'worker'

    def __init__(self):
        self.publisher = pubsub_v1.PublisherClient()
        self.topic_path = self.publisher.topic_path(self.project_id, self.topic_name)

    def publish_message(self, message):
        data = json.dumps(message).encode('utf-8')
        return self.publisher.publish(self.topic_path, data=data)
