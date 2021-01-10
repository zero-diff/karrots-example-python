"""
  flask server

  handle http endpoints
"""

import logging
from flask import jsonify, render_template, Flask

logger = logging.getLogger(__name__)

service = Flask(__name__)


def setup_server():
    """ service initialization """
    logger.debug("setup complete")
    return service


@service.route("/health")
def health_check():
    """ handle health check route """
    return jsonify(
        status="UP"
    )


@service.route("/")
def home():
    """ handle root route """
    return render_template('index.html')
