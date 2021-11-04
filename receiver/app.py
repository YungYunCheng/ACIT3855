import connexion
from connexion import NoContent
import datetime
import json
from pykafka import KafkaClient
import requests
import yaml
import logging
from logging import config

HEADERS = {"Content-Type": "application/json"}

with open("app_conf.yml", "r") as f:
    app_config = yaml.safe_load(f.read())
    kafka_info = app_config["events"]

with open('log_conf.yml', 'r') as f:
    log_config = yaml.safe_load(f.read())
    logging.config.dictConfig(log_config)

logger = logging.getLogger('basicLogger')


def customer_orders_reading(body):
    logger.info("Received event %s request with a unique id of %s"
                % ("customer orders", body["order_id"]))

    client = KafkaClient(hosts='%s:%d' % (kafka_info["hostname"], kafka_info["port"]))
    topic = client.topics[str.encode(kafka_info["topic"])]
    producer = topic.get_sync_producer()
    msg = {
        "type": "customer_orders",
        "datetime": datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S"),
        "payload": body
    }
    msg_str = json.dumps(msg)
    producer.produce(msg_str.encode('utf-8'))

    logger.info("Returned event %s response %s"
                % ("customer orders", body["order_id"]))

    return NoContent, 201


def completed_orders_reading(body):

    logger.info("Received event %s request with a unique id of %s"
                % ("completed order", body["order_id"]))

    client = KafkaClient(hosts='%s:%d' % (kafka_info["hostname"], kafka_info["port"]))
    topic = client.topics[str.encode(kafka_info["topic"])]
    producer = topic.get_sync_producer()
    msg = {
        "type": "completed_orders",
        "datetime": datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S"),
        "payload": body
    }
    msg_str = json.dumps(msg)
    producer.produce(msg_str.encode('utf-8'))

    logger.info("Returned event %s response %s"
                % ("customer orders", body["order_id"]))

    return NoContent, 201


app = connexion.FlaskApp(__name__, specification_dir='')
app.add_api("dcheng-Lab01.yaml", strict_validation=True, validate_responses=True)

if __name__ == "__main__":
    app.run(port=8080)