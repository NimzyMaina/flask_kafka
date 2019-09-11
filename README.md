# Flask Kafka

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

Coming soon...


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