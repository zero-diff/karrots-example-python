""" server testing """
import logging
import unittest

from server import server

logger = logging.getLogger(__name__)

class ServerTestCase(unittest.TestCase):
    """ Flask server testing """

    def setUp(self):
        self.client = server.setup_server().test_client()

    def tearDown(self):
        pass

    def test_route_health(self):
        """ test route /health """
        res = self.client.get('/health')
        self.assertEqual(200, res.status_code)
        expected = """{"status":"UP"}\n"""
        self.assertEqual(expected, res.get_data(as_text=True))

    def test_route_root(self):
        """ test route / """
        res = self.client.get(server.URL_PREFIX + '/')
        self.assertEqual(200, res.status_code)
        expected = """<!DOCTYPE html>
<html lang="en">
<head>
	<meta charset="UTF-8">
	<meta http-equiv="X-UA-Compatible" content="ie=edge">

	<link href="https://fonts.googleapis.com/css?family=Montserrat:300,700" rel="stylesheet">
	<link rel="stylesheet" href="/python/static/styles.css">
	<link rel="shortcut icon" href="/python/static/favicon.ico" type="image/x-icon">
	<title>bzzzzy!</title>
</head>
<body>
<h1>Karrots Hello World</h1>
<h4>An example Python/Flask server with an event loop</h4>
<h4>(version 0.1.9)</h4>
<div class="logo" id="logo" ></div>
<script src="/python/static/main.js"></script>
</body>
</html>"""
        self.assertEqual(expected, res.get_data(as_text=True))

if __name__ == "__main__":
    unittest.main()
