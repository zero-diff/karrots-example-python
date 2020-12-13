"""
    handle the background processing
"""

import logging
import requests
from apscheduler.schedulers.background import BackgroundScheduler

logger = logging.getLogger(__name__)


def background_task1(server):
    """ example background task1 """
    with server.app_context():
        logger.info('first task')
        response = requests.get(
            'https://developer.github.com/v3/activity/events/#list-public-events')
        logger.info('status code %s:', response.status_code)


def background_task2(server):
    """ example background task1 """
    with server.app_context():
        logger.info('second task')


def background_task3(server):
    """ example background task1 """
    with server.app_context():
        logger.info('third task')


def setup_scheduler(server):
    """ setup background tasks """
    scheduler = BackgroundScheduler(daemon=True)
    scheduler.add_job(lambda: background_task1(server), 'interval', seconds=5)
    scheduler.add_job(lambda: background_task2(server), 'interval', seconds=30)
    scheduler.add_job(lambda: background_task3(server), 'interval', seconds=60)
    scheduler.start()
