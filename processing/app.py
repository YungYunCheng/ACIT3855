import connexion
import json
import os
import requests
from apscheduler.schedulers.background import BackgroundScheduler
import yaml
import logging
from logging import config
import datetime


with open('app_conf.yml', 'r') as f:
    app_config = yaml.safe_load(f.read())
    data_file = app_config["datastore"]["filename"]

with open('log_conf.yml', 'r') as f:
    log_config = yaml.safe_load(f.read())
    logging.config.dictConfig(log_config)

logger = logging.getLogger('basicLogger')

DATA_FILE = data_file


def get_stats():
    logger.info(f"Receive Get Current Statistics request")

    if os.path.isfile(DATA_FILE):
        with open(DATA_FILE, "r") as json_file:
            stats = json.load(json_file)
        logger.debug(json.dumps(stats))
        logger.info("End of Get Current Statistics request")

        return stats, 200

    else:
        er_massage = "There are not static events"
        logger.error(er_massage)
        logger.info(f"End of getting Current Statistics Request")

        return er_massage, 404


def populate_stats():
    """ Periodically update stats """

    logger.info(f"Start Periodic Processing")
    current_time = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")

    if not os.path.isfile(DATA_FILE):
        with open(DATA_FILE, 'w') as json_file:
            temp = json.dumps({"num_cust_orders_readings": 0,
                                "num_comp_orders_readings": 0,
                                "num_product_readings": 0,
                                "max_product_readings": 0,
                                "last_updated": "2018-03-12T10:12:45Z"
                            })
            json_file.write(temp)

    with open(DATA_FILE, "r") as json_file:
        stats = json.load(json_file)
        last_updated = stats["last_updated"]

        res1 = requests.get(app_config['customer_orders']['url'], params={'timestamp': last_updated})
        res2 = requests.get(app_config['completed_orders']['url'], params={'timestamp': last_updated})

        if res1.status_code == 200:

            cust_order_list = res1.json()
            if len(cust_order_list) > 0:
                stats["num_cust_orders_readings"] += len(cust_order_list)

            for order in cust_order_list:
                stats["num_product_readings"] += order["product"]["num_of_prduct"]
                if stats["max_product_readings"] <= order["product"]["num_of_prduct"]:
                     stats["max_product_readings"] = order["product"]["num_of_prduct"]

            logger.info("Query for getting Customer Order History after %s returns %d results" %
                        (last_updated, len(cust_order_list)))
        else:
            logger.error(f"Customer Order History did not get 200 response code")

        if res2.status_code == 200:

            comp_order_list = res2.json()
            if len(comp_order_list) > 0:
                stats["num_comp_orders_readings"] += len(comp_order_list)

            logger.info("Query for getting Completed Order History after %s returns %d results" %
                        (last_updated, len(comp_order_list)))
        else:
            logger.error(f"Completed Order History did not get 200 response code")

        stats["last_updated"] = current_time

    with open(DATA_FILE, "w") as json_file:
        state = json.dumps(stats, indent=2)
        json_file.write(state)


def init_scheduler():
    sched = BackgroundScheduler(daemon=True)
    sched.add_job(populate_stats, 'interval', seconds=app_config['scheduler']['period_sec'])
    sched.start()


app = connexion.FlaskApp(__name__, specification_dir='')
app.add_api("ReadingState.yaml", strict_validation=True, validate_responses=True)

if __name__ == "__main__":
    init_scheduler()
    app.run(port=8100, use_reloader=False)
