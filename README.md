# Flask Kafka

> :warning: **Breaking Changes**: Dropping kafka-python library in favour of **confluent-kafka** due it's support & documentation

This is an easy to use utility to help Flask developers to implement microservices that interact with Kafka. This library has been inspired by two other similar libraries :-

- [`Flask RabbitMQ`](https://github.com/pushyzheng/flask-rabbitmq) 
- [`Kakfaesque`](https://github.com/sankalpjonn/kafkaesque)

After looking around the web and on Github, I was not able to find a lot of content on how to consume from a Kafka topic using the Kafka framework. From what I found, I was able to come up with this library by borrowing from the above libraries. They both had a little of what I wanted so I combined them to come up with this one.

I hope you find this useful.

## Features

- Doesn't block process
- Configure by `config.py`
- Support comsuming from topic by decorator 

## Installation

This project has been commited to Pypi, can be installed by pip:
```shell
$ pip install flask-kafka
```

## Simple example

```python
from flask import Flask, request

from flask_kafka import FlaskKafka
app = Flask(__name__)
app.config["KAFKA_CONFIG"] = {'bootstrap.servers': 'localhost:9092',
                              'group.id': 'foo',
                              'enable.auto.commit': 'false',
                              'auto.offset.reset': 'earliest'}

bus = FlaskKafka()
bus.init_app(app)

# curl http://localhost:5004/publish/test-topic?key=foo&value=bar

@app.route('/publish/<topic>', methods=["get"])
def publish(topic):
    qstr = request.args.to_dict()
    key = qstr['key']
    value = qstr['value']
    publisher = bus.get_producer()
    publisher.produce(topic, key=key, value=value)
    publisher.poll(1)
    return "Published to {} => {} : {}".format(topic, key, value)

@bus.handle('test-topic')
def test_topic_handler(consumer,msg):
    print("Consumed event from topic {topic}: key = {key:12} value = {value:12}".format(
            topic=msg.topic(), key=msg.key().decode('utf-8'), value=msg.value().decode('utf-8')))


# or
# bus.add_topic_handler("test-topic", lambda consumer, msg: print(msg.value()))

if __name__ == '__main__':
    bus.run()
    app.run(debug=True, port=5004, use_reloader=False)

```

## Special Thanks

- [cookieGeGe](https://github.com/cookieGeGe) - Contributed to new structure


## License

```
MIT License

Copyright (c) 2019 Nimrod Kevin Maina

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```