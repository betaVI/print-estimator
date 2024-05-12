from flask import Blueprint, request, jsonify
from dependency_injector.wiring import Provide, inject
from src.dataaccess.dataprovider import DataProvider
from server.src.container import Container
from server.src.models import estimate, model
import re

estimateapi = Blueprint('estimateapi', __name__)

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
        db.createEstimate(estimate.Estimate(payload))
        return jsonify({
            'success': True
        }), 201
    elif request.method == 'PATCH' and id != 0:
        payload = request.get_json()
        db.updateEstimate(id, estimate.Estimate(payload))
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
    
@estimateapi.route('/api/estimates/<int:estimateid>/models', methods=[ 'GET', 'POST' ])
@estimateapi.route('/api/estimates/<int:estimateid>/models/<int:id>', methods=[ 'GET', 'PATCH', 'DELETE' ])
@inject
def models(estimateid: int, id: int=0, db: DataProvider = Provide[Container.db]):
    if request.method == 'GET':
        if id == 0:
            models = db.getModelsForEstimate(estimateid)
            return jsonify({
                'success': True,
                'models': models
            }), 200
        else:
            models = next(iter([ m for m in db.getModelsForEstimate(estimateid) if m.id == id ]),None)
            return jsonify({
                'success': models is not None,
                'model': models
            }), 200
    elif request.method == 'POST' and id == 0:
        payload = request.get_json()
        db.createModelForEstimate(estimateid, model.Model(payload))
        return jsonify({
            'success': True,
        }), 201
    elif request.method == 'PATCH' and id != 0:
        payload = request.get_json()
        db.updateModel(estimateid, id, model.Model(payload))
        return jsonify({
            'success': True
        }), 201
    elif request.method == 'DELETE' and id != 0:
        db.deleteModel(id)
        return jsonify({
            'success': True
        }), 200
    else:
        return jsonify({
            'success': False
        }), 400