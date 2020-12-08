def test_index(service, client):
    res = client.get('/')
    assert res.status_code == 200
    expected = """<!DOCTYPE html>
<html lang="en">
<head>
	<meta charset="UTF-8">
	<meta http-equiv="X-UA-Compatible" content="ie=edge">

	<link href="https://fonts.googleapis.com/css?family=Montserrat:300,700" rel="stylesheet">
	<link rel="stylesheet" href="/static/styles.css">
	<link rel="shortcut icon" href="/static/favicon.ico" type="image/x-icon">
	<title>bzzzzy!</title>
</head>
<body>
<h1>Karrots Hello World</h1>
<h4>(An example Python/Flask server with an event loop)</h4>
<div class="logo" id="logo" ></div>
<script src="/static/main.js"></script>
</body>
</html>"""
    assert expected == res.get_data(as_text=True)
