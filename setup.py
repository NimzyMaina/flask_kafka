# please install python if it is not present in the system
from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='flask-kafka',
    version='0.1.0',
    packages=['flask_kafka'],
    install_requires=['kafka-python'],
    license='MIT',
    description='An easy to use kafka consumer that uses the confluent kafka library, it runs concurrently with your '
                'flask server',
    author='Nimrod Kevin Maina',
    author_email='nimzy.maina@gmail.com',
    keywords=['kafka', 'consumer', 'kafkaesque', 'flask', 'simple', 'consumer', 'flask style', 'decorator'],
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/nimzymaina/flask_kafka",
    include_package_data=True,
)
