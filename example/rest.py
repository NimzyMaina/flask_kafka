from flask import Blueprint, request
from example.bus import bus

rest = Blueprint('rest', __name__)


def acked(err, msg):
    if err is not None:
        print("Failed to deliver message: %s: %s" % (str(msg), str(err)))
    else:
        print("Message produced: %s" % (str(msg.value())))


@rest.route('/')
def index():
    return "This is a simple flask kafka example api"


@rest.route('/publish/<topic>')
def publish(topic):
    qstr = request.args.to_dict()
    key = qstr['key']
    value = qstr['value']
    publisher = bus.get_producer()
    publisher.produce(topic, key=key, value=value, callback=acked)
    publisher.poll(1)
    return "Published to {} => {} : {}".format(topic, key, value)