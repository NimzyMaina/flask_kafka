from typing import Dict, Callable
import atexit
import os
import platform
import threading
import logging
import sys

from flask_kafka.consumer import KafkaConsumer
from flask_kafka.producer import KafkaProducer


class FlaskKafka(object):

    def __init__(self, app=None):
        self.app = None
        self.logger = self.get_logger()
        self._consumers: Dict[str, KafkaConsumer] = {}
        self._producers: Dict[str, KafkaProducer] = {}
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        self.app = app
        if "flask_kafka" in self.app.extensions:
            raise RuntimeError(
                "A 'Kafka' instance has already been registered on this Flask app."
                " Import and use that instance instead."
            )
        self.app.extensions["flask_kafka"] = self
        kafka_config = self.app.config.setdefault("KAFKA_CONFIG", {})
        self.create_consumer("default", **kafka_config)
        self.create_producer("default", **kafka_config)
        kafka_binds = self.app.config.setdefault("KAFKA_BINDS", {})
        for name, config in kafka_binds.items():
            self.create_consumer(name, **config)
            self.create_producer(name, **config)
        app.app_context().push()

    def get_consumer(self, consumer_name: str = "default") -> KafkaConsumer:
        return self._consumers.get(consumer_name, None)

    def get_producer(self, producer_name: str = "default") -> KafkaProducer:
        return self._producers.get(producer_name, None)

    def add_consumer(self, consumer_name: str, consumer: KafkaConsumer):
        if consumer_name is None or consumer_name == "":
            raise Exception("Consumer name cannot be empty")
        if consumer_name in self._consumers.keys():
            raise Exception("Duplicate consumer name")
        if not isinstance(consumer, KafkaConsumer):
            raise Exception(f"must be {KafkaConsumer.__class__}")
        self._consumers[consumer_name] = consumer

    def create_consumer(self, consumer_name: str, **config):
        self.add_consumer(consumer_name, KafkaConsumer(self.logger,**config))

    def create_producer(self, producer_name: str, **config):
        self.add_producer(producer_name, KafkaProducer(**config))

    def add_producer(self, producer_name: str, producer: KafkaProducer):
        if producer_name is None or producer_name == "":
            raise Exception("Producer name cannot be empty")
        if producer_name in self._producers.keys():
            raise Exception("Duplicate Producer name")
        if not isinstance(producer, KafkaProducer):
            raise Exception(f"must be {KafkaProducer.__class__}")
        self._producers[producer_name] = producer

    def handle(self, topic: str, consumer: str = "default"):
        consumer_obj = self.get_consumer(consumer)
        if consumer_obj is None:
            raise Exception(f"name {consumer} Consumer not registered")
        return consumer_obj.handle(topic)

    def add_topic_handler(self, topic: str, callback: Callable, consumer: str = "default"):
        self.handle(topic, consumer)(callback)

    def _run(self):
        self.logger.info("Consumers found: {}".format(len(self._consumers.items())))
        for name, consumer in self._consumers.items():
            self.logger.info("Starting Consumer: {}".format(name))
            t = threading.Thread(target=consumer.subscribe, name=name)
            t.setDaemon(True)
            t.start()

    def _start(self):
        self._run()

    def run(self, lock: bool = True):
        if not lock:
            self._start()
            return
        else:
            self._start_with_lock()

    def _start_with_lock(self):
        """
        Start the kafka consumer with a lock
        :return:
        """
        default_lock_file_path = os.path.join(os.getcwd(), "flask_kafka.lock")
        lock_file_path = self.app.config.setdefault("KAFKA_LOCK_FILE", default_lock_file_path)
        dir_path = os.path.dirname(lock_file_path)
        self.logger.info(dir_path)
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)
        if platform.system() != 'Windows':
            fcntl = __import__("fcntl")
            f = open(lock_file_path, 'wb')
            try:
                fcntl.flock(f, fcntl.LOCK_EX | fcntl.LOCK_NB)
                self._start()
            except:
                pass

            def unlock():
                fcntl.flock(f, fcntl.LOCK_UN)
                f.close()

            atexit.register(unlock)
        else:
            msvcrt = __import__('msvcrt')
            f = open(lock_file_path, 'wb')
            try:
                msvcrt.locking(f.fileno(), msvcrt.LK_NBLCK, 1)
                self._start()
            except:
                pass

            def _unlock_file():
                try:
                    f.seek(0)
                    msvcrt.locking(f.fileno(), msvcrt.LK_UNLCK, 1)
                except:
                    pass

            atexit.register(_unlock_file)

    @staticmethod
    def get_logger():
        logger = logging.getLogger('flask_kafka')
        ch = logging.StreamHandler(sys.stdout)
        ch.setLevel(logging.INFO)
        formatter = logging.Formatter('[%(asctime)s] [%(name)s] [%(levelname)s] %(message)s')
        ch.setFormatter(formatter)
        logger.addHandler(ch)
        logger.setLevel(logging.INFO)
        return logger
