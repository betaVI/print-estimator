from flask import Blueprint, request, jsonify, render_template
from dependency_injector.wiring import Provide, inject
from src.dataaccess.dataprovider import DataProvider
from src.container import Container
from src.models import estimate, filament, settings, customer, print

estimateapi = Blueprint('estimateapi', __name__)

@estimateapi.route('/')
def index():
    return render_template("index.html")

@estimateapi.route('/api/settings', methods=[ 'GET', 'PATCH' ])
@inject
def getsettings(db: DataProvider = Provide[Container.db]):
    if request.method == 'GET':
        s = db.getSettings()
        return jsonify({
            'success': True,
            'settings': s
        }), 200
    elif request.method == 'PATCH':
        payload = request.get_json()
        db.saveSettings(settings.Settings(payload))
        return jsonify({
            'success': True
        }), 201
    else:
        return jsonify({
            'success': False
        }), 400
    
@estimateapi.route('/api/customers', methods=[ 'GET', 'POST'])
@estimateapi.route('/api/customers/<int:id>', methods=[ 'GET', 'PATCH', 'DELETE' ])
@inject
def customers(id: int=0, db: DataProvider = Provide[Container.db]):
    if request.method == 'GET':
        customers = db.getCustomers(id)
        if type(customers) is list:
            return jsonify({
                'success': True,
                'customers': customers
            }), 200
        else:
            return jsonify({
                'success': True,
                'customer': customers
            }), 200
    elif request.method == 'POST' and id == 0:
        payload = request.get_json()
        db.createCustomer(customer.Customer(payload))
        return jsonify({
            'success': True,
        }), 201
    elif request.method == 'PATCH' and id != 0:
        payload = request.get_json()
        db.updateCustomer(id, customer.Customer(payload))
        return jsonify({
            'success': True,
        }), 201
    elif request.method == 'DELETE' and id != 0:
        db.deleteCustomer(id)
        return jsonify({
            'success': True
        }), 200
    else:
        return jsonify({
            'success': False
        }), 400

@estimateapi.route('/api/filaments', methods=[ 'GET', 'POST' ])
@estimateapi.route('/api/filaments/<int:id>', methods=[ 'GET', 'PATCH', 'DELETE' ])
@inject
def filaments(id: int=0, db: DataProvider = Provide[Container.db]):
    if request.method == 'GET':
        filaments = db.getFilaments(id)
        if (type(filaments) is list):
            return jsonify({
                'success': True,
                'filaments': filaments
            }), 200
        else:
            return jsonify({
                'success': filaments is not None,
                'filament': filaments
            }), 200
    elif request.method == 'POST' and id == 0:
        payload = request.get_json()
        db.createFilament(filament.Filament(payload))
        return jsonify({
            'success': True
        }), 201
    elif request.method == 'PATCH' and id != 0:
        payload = request.get_json()
        db.updateFilament(id, filament.Filament(payload))
        return jsonify({
            'success': True
        }), 201
    elif request.method == 'DELETE' and id != 0:
        db.deleteFilament(id)
        return jsonify({
            'success': True
        }), 200
    else:
        return jsonify({
            'success': False
        }), 400

@estimateapi.route('/api/estimates', methods=[ 'GET', 'POST' ])
@estimateapi.route('/api/estimates/<int:id>', methods=[ 'GET', 'PATCH', 'DELETE' ])
@inject
def estimates(id: int=0, db: DataProvider = Provide[Container.db]):
    if request.method == 'GET':
        estimates = db.getEstimates(id)
        if (type(estimates) is list):
            return jsonify({
                'success': True,
                'estimates': estimates
            }), 200
        else:
            return jsonify({
                'success': estimates is not None,
                'estimate': estimates
            }), 200
    elif request.method == 'POST' and id == 0:
        payload = request.get_json()
        e = estimate.Estimate(payload)
        db.createEstimate(e)
        return jsonify({
            'success': True
        }), 201
    elif request.method == 'PATCH' and id != 0:
        payload = request.get_json()
        e = estimate.Estimate(payload)
        db.updateEstimate(id, e)
        return jsonify({
            'success': True
        }), 201
    elif request.method == 'DELETE' and id != 0:
        db.deleteEstimate(id)
        return jsonify({
            'success': True
        }), 200
    else:
        return jsonify({ 
            'success': False
        }), 400
    
@estimateapi.route('/api/prints', methods=[ 'GET', 'POST' ])
@estimateapi.route('/api/prints/<int:id>', methods=[ 'GET', 'PATCH', 'DELETE' ])
@inject
def prints(id: int=0, db: DataProvider = Provide[Container.db]):
    if request.method == 'GET':
        prints = db.getPrints(id)
        if type(prints) is list:
            return jsonify({
                'success': True,
                'prints': prints
            })
        else:
            return jsonify({
                'success': True,
                'print': prints
            })
    elif request.method == 'POST' and id == 0:
        payload = request.get_json()
        db.createPrint(print.Print(payload))
        return jsonify({
            'success': True,
        }), 201
    elif request.method == 'PATCH' and id != 0:
        payload = request.get_json()
        db.updatePrint(id, print.Print(payload))
        return jsonify({
            'success': True
        }), 200
    elif request.method == 'DELETE' and id != 0:
        db.deletePrint(id)
        return jsonify({
            'success': True
        }), 200
    else:
        return jsonify({
            'success': False
        }), 400
    
def _validateFilament(payload:dict):
    if 'name' not in payload:
        return 'Name is required'
    if 'cost' not in payload:
        return 'Cost is required'
    if 'grams' not in payload:
        return 'Grams is required'
    #validate the values