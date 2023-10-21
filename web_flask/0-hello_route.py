#!/usr/bin/python3
"""
Flask app demo for basic route
just another hello world example
with specifing IP and port
and disabling strict_slashes on routes
"""
from flask import Flask

# make an instance on Flask class and assign
# it to app variable
app = Flask(__name__)

# disable strict _slashes globally
# by default it was on
app.url_map.strict_slashes = False
# another way on @app.route decorator
# @app.route('/', strict_slashes=False)


@app.route("/")
def hello_w():
    ''' return string “Hello HBNB!”
    on get request on "/" route
    '''
    return ("Hello HBNB!")


if __name__ == "__main__":
    # before below lines
    # you still could run this using
    # flask --app 0-hello_route run

    # but here we will define host and port
    # you also could do this on command line
    # with --port --host options
    app.run(host="0.0.0.0",port=5000, debug=False)
