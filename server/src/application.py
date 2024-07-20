import os, sys, decimal, flask.json
from flask import Flask
# from flask_cors import CORS
from src.container import create_container
from src.models import model, estimate, filament, settings, customer, print

class JsonEncoder(flask.json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, decimal.Decimal):
            return str(obj)
        if isinstance(obj, (model.Model, estimate.Estimate, filament.Filament, settings.Settings, customer.Customer, print.Print)):
            return obj.__dict__
        return super(JsonEncoder, self).default(obj)

def create_app() -> Flask:
    
    #import blueprints
    #from src.controllers import ...
    from src.controllers.estimatecontroller import estimateapi
    
    app = Flask(__name__, static_folder='static/assets', template_folder='static')
    app.json_encoder = JsonEncoder
    app.container = create_container(__name__)
    app.config['SECRET_KEY'] = str(os.urandom(32))

    #import blueprint based on import name
    #app.register_blueprint(...)
    app.register_blueprint(estimateapi)

    # removed because client and server are hosted on the same app
    # CORS(app, resources={r'/*': {'origins': '*'}})

    return app