#!/usr/bin/python3
"""
Flask app demo for basic routes
Also hoe to use jinja2 templates
and pass variables to template from functions
and specify dynamic routes that
accepts text or integers on url
"""
from flask import Flask, render_template
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
    but also have default value "is cool"
    '''
    newtext = escape(text).replace("_", " ")
    return (f"Python {newtext}")


@app.route("/number/<int:n>")
def int_dynmic_route(n):  # must pass n as arg
    ''' return string “{n} is a number”
    on get request on this route
    which accpts integer values
    '''
    return (f"{n} is a number")


@app.route("/number_template/<int:n>")
def int_to_jinja(n):  # must pass n as arg
    ''' return html template using jinja2
    to pass vars from flask route function
    to the jinja2 template
    on get request on this route
    which accpts integer values
    '''
    return render_template('5-number.html', num=n, title="HBNB")


if __name__ == "__main__":
    # before below lines
    # you still could run this using
    # flask --app 0-hello_route run

    # but here we will define host and port
    # you also could do this on command line
    # with --port --host options
    app.run(host="0.0.0.0", port=5000, debug=False)
