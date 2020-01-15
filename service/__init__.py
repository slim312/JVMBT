from flask import Flask
from flask_restful import Api

app = Flask(__name__)
app.logger.info("App initialized!")
api = Api(app=app)
app.logger.info("Api initialized!")
