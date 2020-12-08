import requests
from apscheduler.schedulers.background import BackgroundScheduler
import logging

logger = logging.getLogger(__name__)


def backgroundTask1(server):
    with server.app_context():
        logger.info("first task")
        response = requests.get('https://developer.github.com/v3/activity/events/#list-public-events')
        logger.info(f'status code: {response.status_code}')


def backgroundTask2(server):
    with server.app_context():
        logger.info("second task")


def backgroundTask3(server):
    with server.app_context():
        logger.info("third task")


def setupScheduler(server):
    scheduler = BackgroundScheduler(daemon=True)
    scheduler.add_job(lambda: backgroundTask1(server), 'interval', seconds=5)
    scheduler.add_job(lambda: backgroundTask2(server), 'interval', seconds=30)
    scheduler.add_job(lambda: backgroundTask3(server), 'interval', seconds=60)
    scheduler.start()
