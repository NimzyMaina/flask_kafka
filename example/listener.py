# from flask import current_app
from example.bus import bus

# bus = current_app.extensions.get('flask_kafka')


def register_listeners():
    # Handle message received from a Kafka topic
    @bus.handle('mpesa-reaper')
    def test_topic_handler(consumer, msg):
        print("Consumed event from topic {topic}: key = {key:12} value = {value:12}".format(
            topic=msg.topic(), key=msg.key().decode('utf-8'), value=msg.value().decode('utf-8')))
