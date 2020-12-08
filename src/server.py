# Example Karrots Python application
#
# It demonstrates two ways to handle data processing:
# 1: periodic background jobs that might make http calls
# 2: http server that handles inbound http requests

import logging.config

from flask import Flask, render_template

import background

logging.config.fileConfig('logging_config.ini')

logger = logging.getLogger(__name__)

server = Flask(__name__)
background.setupScheduler(server)


@server.route("/")
def home():
    return render_template('index.html')


if __name__ == "__main__":
    server.run(debug=True, host='0.0.0.0')
