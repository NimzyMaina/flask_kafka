from flask import Flask
from example.bus import bus
from example.listener import register_listeners
from rest import rest
# from flask_kafka import FlaskKafka3

app = Flask(__name__)
app.config["KAFKA_CONFIG"] = {'bootstrap.servers': 'localhost:9092',
                              'group.id': 'foo',
                              'enable.auto.commit': 'false',
                              'auto.offset.reset': 'earliest'}


# bus = FlaskKafka3() # Can be instantiated here or an external file
bus.init_app(app)  # 1. MUST be called before any handlers are registered (sets up 'default' consumer & producer)


# @bus.handle('mpesa-reaper')  # 2. MUST be called b4 bus.run() (registers handlers to consumers)
# def test_topic_handler(consumer, msg):
#     print("Consumed event from topic {topic}: key = {key:12} value = {value:12}".format(
#         topic=msg.topic(), key=msg.key().decode('utf-8'), value=msg.value().decode('utf-8')))


if __name__ == '__main__':
    # Start consuming from the Kafka server
    print('running app...')

    # Register handlers from an external file
    register_listeners()  # 2. MUST be called b4 bus.run() (registers handlers to consumers)

    bus.run()  # 3. MUST be called LAST after consumers & handlers have been set up

    app.register_blueprint(rest)

    # Start Flask server
    app.run(port=5004, debug=True, use_reloader=False)
