from flask import Flask

from health import check_health

app = Flask(__name__)


@app.route("/")
def hello_world():
    return "Hello, world!"


@app.route("/health")
def health():
    status, message = check_health()
    if status:
        return {
            "status": "ok",
            "message": None
        }
    else:
        return {
            "status": "error",
            "message": message
        }
