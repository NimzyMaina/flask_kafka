from kafka import KafkaConsumer
import threading
import logging
import sys


class FlaskKafka:
    def __init__(self, interrupt_event, **kw):
        self.consumer = KafkaConsumer(**kw)
        self.handlers={}
        self.interrupt_event = interrupt_event
        logger = logging.getLogger('flask-kafka-consumer')
        ch = logging.StreamHandler(sys.stdout)
        ch.setLevel(logging.INFO)
        formatter = logging.Formatter('[%(asctime)s] [%(name)s] [%(levelname)s] %(message)s')
        ch.setFormatter(formatter)
        logger.addHandler(ch)
        logger.setLevel(logging.INFO)
        self.logger = logger

    def _add_handler(self, topic, handler):
        if self.handlers.get(topic) is None:
            self.handlers[topic] = []
        self.handlers[topic].append(handler)

    def handle(self, topic):
        def decorator(f):
            self._add_handler(topic, f)
            return f
        return decorator

    def _run_handlers(self, msg):
        try:
            handlers = self.handlers[msg.topic]
            for handler in handlers:
                handler(msg)
            self.consumer.commit()
        except Exception as e:
            self.logger.critical(str(e), exc_info=1)
            self.consumer.close()
            sys.exit("Exited due to exception")

    def signal_term_handler(self, signal, frame):
        self.logger.info("closing consumer")
        self.consumer.close()
        sys.exit(0)

    def _start(self):
        self.consumer.subscribe(topics=tuple(self.handlers.keys()))
        self.logger.info("starting consumer...registered signterm")

        for msg in self.consumer:
            self.logger.debug("TOPIC: {}, PAYLOAD: {}".format(msg.topic, msg.value))
            self._run_handlers(msg)
            # stop the consumer
            if self.interrupt_event.is_set():
                self.interrupted_process()
                self.interrupt_event.clear()

    def interrupted_process(self, *args):
        self.logger.info("closing consumer")
        self.consumer.close()
        sys.exit(0)

    def _run(self):
        self.logger.info(" * The flask Kafka application is consuming")
        t = threading.Thread(target=self._start)
        t.start()

    # run the consumer application
    def run(self):
        self._run()
