from flask import Flask, request
from flask_restplus import Api, Resource, fields
from msptools import api as msptoolsapi
from msptools import result
import json

app = Flask(__name__, instance_relative_config=True)
apiflask = Api(app, version="0.1", title="ApiProcess IHCantabria")

msptoolsapi.start(apiflask)
