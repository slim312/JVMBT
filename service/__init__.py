from flask import Flask
from flask_restful import Api
from flask_cors import CORS

app = Flask(__name__)
app.logger.info("App initialized!")
CORS(app=app, resources="*", headers='Content-type')
api = Api(app=app)
app.logger.info("Api initialized!")

import service.views
