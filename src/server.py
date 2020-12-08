# Example Karrots Python application
#
# It demonstrates two ways to handle data processing:
# 1: periodic background jobs that might make http calls
# 2: http server that handles inbound http requests

import logging.config

from flask import Flask, render_template

import src.background

service = Flask(__name__)


@service.route("/")
def home():
    return render_template('index.html')


def setup_service():
    logging.config.fileConfig('logging_config.ini')

    logger = logging.getLogger(__name__)

    src.background.setupScheduler(service)

    return service


if __name__ == "__main__":
    app = setup_service()
    app.run(debug=True, host='0.0.0.0')
