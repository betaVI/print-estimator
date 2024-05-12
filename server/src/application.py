import os, sys, decimal, flask.json
from flask import Flask
from flask_cors import CORS
from server.src.container import create_container
from server.src.models import model, estimate

class JsonEncoder(flask.json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, decimal.Decimal):
            return str(obj)
        if isinstance(obj, (model.Model, estimate.Estimate)):
            return obj.__dict__
        return super(JsonEncoder, self).default(obj)

def create_app() -> Flask:
    
    #import blueprints
    #from server.src.controllers import ...
    from server.src.controllers.estimatecontroller import estimateapi
    
    app = Flask(__name__)
    app.json_encoder = JsonEncoder
    app.container = create_container(__name__)
    app.config['SECRET_KEY'] = str(os.urandom(32))

    #import blueprint based on import name
    #app.register_blueprint(...)
    app.register_blueprint(estimateapi)

    CORS(app, resources={r'/*': {'origins': '*'}})

    return app