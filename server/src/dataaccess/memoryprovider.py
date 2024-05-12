import random, time

from server.src.dataaccess.dataprovider import DataProvider

from server.src.models.estimate import Estimate
from server.src.models.model import Model

class MemoryProvider(DataProvider):
    def __init__(self) -> None:
        self.estimates = [
            Estimate({
                'id': 1,
                'name': 'Catan',
            }),
        ]
        self.models= [
            Model({
                'id': 1,
                'estimateid': 1,
                'name': 'Player Piece',
                'grams': 50,
                'seconds': 276,
                'cost': 1.25
            })
        ]

    def getEstimates(self, id: int = 0):
        self._randomDelay()
        if id!=0:
            estimate = self._getEstimateById(id)
            if estimate is not None:
                return Estimate(estimate.__dict__)
            return None
        return self.estimates
    
    def createEstimate(self, estimate: Estimate):
        self._randomDelay()
        estimate.id = max([e.id for e in self.estimates]) + 1
        self.estimates.append(estimate)

    def updateEstimate(self, id: int, estimate: Estimate):
        self._randomDelay()
        estimate.id = id
        self.estimates = [ estimate if e.id == id else e for e in self.estimates ]
    
    def deleteEstimate(self, id: int):
        self._randomDelay()
        self.estimates.remove(self._getEstimateById(id))

    def getModelsForEstimate(self, estimateid: int):
        self._randomDelay()
        return self._getModelsForEstimate(estimateid)

    def createModelForEstimate(self, estimateid: int, model: Model):
        self._randomDelay()
        model.estimateid = estimateid
        model.id = max([ m.id for m in self.models]) + 1
        self.models.append(model)

    def updateModel(self, estimateid: int, modelid: int, model: Model):
        self._randomDelay()
        model.id = modelid
        model.estimateid = estimateid
        self.models = [ model if m.id == modelid else m for m in self.models ]
    
    def deleteModel(self, modelid: int):
        self._randomDelay()
        self.models.remove(self._getModelById(modelid))

    def _randomDelay(self):
        time.sleep(random.randint(1,5))
    
    def _getEstimateById(self, id: int):
        return next(iter([ e for e in self.estimates if e.id==id ]), None)
    
    def _getModelsForEstimate(self, estimateid: int):
        return [ m for m in self.models if m.estimateid == estimateid]
    
    def _getModelById(self, id: int):
        return next(iter([ m for m in self.models if m.id == id ]), None)