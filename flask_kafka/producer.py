from confluent_kafka import Producer


class KafkaProducer(object):

    def __init__(self, **conf):
        self._producer = Producer(conf)

    def __getattr__(self, item):
        return getattr(self._producer, item)
