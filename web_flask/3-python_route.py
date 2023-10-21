#!/usr/bin/python3
"""
Flask app demo for basic routes
one of them accept text arg on url
"""
from flask import Flask
from markupsafe import escape

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


@app.route("/hbnb")
def hbnb_route():
    ''' return string “HBNB”
    on get request on "/hbnb" route
    '''
    return ("HBNB")


@app.route("/c/<text>")
def c_string_route(text):  # must pass text as arg
    ''' return string “c {passed text}”
    on get request on "/c/<text>" route
    which accpts text values
    '''
    newtext = escape(text).replace("_", " ")
    return (f"C {newtext}")


@app.route("/python")
@app.route("/python/<text>")
def py_string_route(text="is cool"):  # must pass text as arg
    ''' return string “python {passed text}”
    on get request on "/python/<text>" route
    which accpts text values
    put also have default value "is cool"
    '''
    newtext = escape(text).replace("_", " ")
    return (f"Python {newtext}")


if __name__ == "__main__":
    # before below lines
    # you still could run this using
    # flask --app 0-hello_route run

    # but here we will define host and port
    # you also could do this on command line
    # with --port --host options
    app.run(host="0.0.0.0", port=5000, debug=False)
