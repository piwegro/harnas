from flask import Flask

from db import connect

app = Flask(__name__)

connect()


@app.route("/")
def hello_world():
    return "Hello, world!"
