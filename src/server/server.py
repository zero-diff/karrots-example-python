"""
  flask server

  handle http endpoints
"""

import logging
from flask import jsonify, render_template, Flask, Blueprint

logger = logging.getLogger(__name__)

URL_PREFIX = '/python'
service = Flask(__name__)
blue_print = Blueprint('root', __name__, template_folder='templates', static_folder='static',
                       url_prefix=URL_PREFIX)


def setup_server():
    """ service initialization """
    logger.debug("setup complete")
    service.register_blueprint(blue_print)
    return service


@service.route("/health")
def health_check():
    """ handle health check route """
    return jsonify(
        status="UP"
    )


@blue_print.route("/")
def home():
    """ handle root route """
    return render_template('index.html')
