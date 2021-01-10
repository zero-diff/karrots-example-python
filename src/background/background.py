"""
    handle the background processing
"""

import logging
import requests
from apscheduler.schedulers.background import BackgroundScheduler

logger = logging.getLogger(__name__)

def setup_background():
    """ setup background processing """
    setup_scheduler()

def background_task1():
    """ example background task1 """
    logger.info('first task')
    response = requests.get(
        'https://developer.github.com/v3/activity/events/#list-public-events')
    logger.info('status code %s:', response.status_code)


def background_task2():
    """ example background task1 """
    logger.info('second task')


def background_task3():
    """ example background task1 """
    logger.info('third task')


def setup_scheduler():
    """ setup background tasks """
    scheduler = BackgroundScheduler(daemon=True)
    # pylint: disable=unnecessary-lambda
    scheduler.add_job(lambda: background_task1(), 'interval', seconds=5)
    # pylint: disable=unnecessary-lambda
    scheduler.add_job(lambda: background_task2(), 'interval', seconds=30)
    # pylint: disable=unnecessary-lambda
    scheduler.add_job(lambda: background_task3(), 'interval', seconds=60)
    scheduler.start()
