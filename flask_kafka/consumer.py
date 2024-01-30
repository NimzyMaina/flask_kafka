from confluent_kafka import Consumer, KafkaError
import traceback
from typing import Callable
import atexit
import logging
import sys


class KafkaConsumer(object):

    def __init__(self, logger, **config):
        self.handlers = {}
        self.is_running = True
        self.logger = logger
        self._consumer = Consumer(config)
        self.config = config

    def __getattr__(self, item: str):
        return getattr(self._consumer, item)

    def _add_handler(self, topic: str, handler: Callable):
        if self.handlers.get(topic) is None:
            self.handlers[topic] = []
        self.handlers[topic].append(handler)

    def handle(self, topic):
        def decorator(f):
            self._add_handler(topic, f)
            return f

        return decorator

    def _run_handlers(self, msg):
        handlers = self.handlers.get(msg.topic(), [])
        for handler in handlers:
            try:
                if not callable(handler):
                    continue
                handler(self, msg)
            except Exception as e:
                self.logger.error(traceback.format_exc())

    def on_stop(self):
        self.is_running = False
        self.logger.info("closing consumer")
        self._consumer.close()
        self.logger.info("consumer closed")

    def subscribe(self):
        try:
            if not any(self.handlers.keys()):
                self.logger.warning("No handlers have been registered")
                return
            self._consumer.subscribe(topics=list(self.handlers.keys()))
            self.logger.info("Subscribing to topic(s) {}".format(list(self.handlers.keys())))
            atexit.register(self.on_stop)

            while self.is_running:
                msg = self._consumer.poll(timeout=20.0)
                if msg is None:
                    print("No messages received")
                    continue

                if msg.error():
                    if msg.error().code() == KafkaError._PARTITION_EOF:
                        # End of partition event
                        self.logger.error('%% %s [%d] reached end at offset %d\n' %
                                          (msg.topic(), msg.partition(), msg.offset()))
                self._run_handlers(msg)
        finally:
            self.logger.info("closing consumer")
            self._consumer.close()
