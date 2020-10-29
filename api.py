from flask import Flask, request
from flask_restplus import Api, Resource, fields
from msptools import api as msptoolsapi
from flask_cors import CORS

app = Flask(__name__, instance_relative_config=True)
CORS(app)
apiflask = Api(app, version="0.0.1", title="ApiProcess IHCantabria")


def create():
    msptoolsapi.start(apiflask)
    return app


if __name__ == "apimsp":
    create()