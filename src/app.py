"""
  example karrots python application

  this example demonstrates two ways to handle data processing:
  1: periodic background jobs that might make http calls
  2: http server that handles inbound http requests
"""

import logging.config

from src.server import server
from src.background import background

service = server.setup_server()

def setup_app():
    """ setup the application """
    logging.config.fileConfig('logging_config.ini')
    background.setup_background()

if __name__ == "__main__":
    setup_app()
    service.run(debug=True, host='0.0.0.0')
