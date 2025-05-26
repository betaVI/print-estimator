import random, time

from src.dataaccess.dataprovider import DataProvider

from src.models import estimate, model, filament, settings

class MemoryProvider(DataProvider):
    def __init__(self) -> None:
        self.estimates = []
        self.settings= settings.Settings({
            'printablehours': 16,
            'laborcost': 30,
            'kwhcost': .018,
            'printlabor': .01,
            'colorchangelabor': .03,
            'postprocessinglabor': .05,
            'electricmarkup': .5,
            'materialmarkup': .5
        })
        self.createEstimate(estimate.Estimate({
            'id': 1,
            'name': 'Catan',
            'models': [
                model.Model({
                    'id': 1,
                    'estimateid': 1,
                    'filamentid': 1,
                    'name': 'Player Piece',
                    'quantity': 6,
                    'grams': 55,
                    'minutes': 241,
                    'postprocessing': True
                })
            ]
        }))

    def getSettings(self):
        self._randomDelay()
        return self.settings
    
    def saveSettings(self, settings: settings.Settings):
        self._randomDelay()
        self.settings = settings

    def getEstimates(self, id: int = 0):
        self._randomDelay()
        if id!=0:
            e = self._getEstimateById(id)
            if e is not None:
                return estimate.Estimate(e.__dict__)
            return None
        return [self._populateEstimateFields(e) for e in self.estimates]
    
    def createEstimate(self, estimate: estimate.Estimate):
        self._randomDelay()
        estimate.id = self._getNextId(self.estimates)
        self.estimates.append(estimate)

    def updateEstimate(self, id: int, estimate: estimate.Estimate):
        self._randomDelay()
        estimate.id = id
        self.estimates = [ estimate if e.id == id else e for e in self.estimates ]
    
    def deleteEstimate(self, id: int):
        self._randomDelay()
        self.estimates.remove(self._getEstimateById(id))

    def _populateEstimateFields(self, estimate: estimate.Estimate) -> estimate.Estimate:
        filamentused = {}
        estimate.totalgrams = 0
        estimate.materialcost = 0
        estimate.totalprints = 0
        estimate.totalprinttime = 0
        estimate.totalpostprocessing = 0
        for m in estimate.models:
            if m.filamentid not in filamentused:
                f = next(iter([fil for fil in self.filaments if fil.id == m.filamentid]))
                filamentused[m.filamentid] = f.cost / f.grams
            m.totalcost = round(filamentused[m.filamentid] * m.grams * m.quantity, 2)
            estimate.totalgrams += m.grams * m.quantity
            estimate.materialcost += m.totalcost
            estimate.totalprints += m.quantity
            estimate.totalprinttime += m.quantity * m.minutes
            estimate.totalpostprocessing += m.quantity if m.postprocessing else 0

        estimate.totalcolors = len(filamentused)

        estimate.materialprofit = round(estimate.materialcost * self.settings.materialmarkup, 2)
        estimate.materialprice = estimate.materialcost + estimate.materialprofit

        estimate.electriccost = round((estimate.totalprinttime / 60) * self.settings.kwhcost, 2)
        estimate.electricprofit = round(estimate.electriccost * self.settings.electricmarkup, 2)
        estimate.electricprice = estimate.electriccost + estimate.electricprofit

        estimate.totallabor = estimate.totalprints * self.settings.printlabor
        estimate.totallabor += estimate.totalcolors * self.settings.colorchangelabor
        estimate.totallabor += estimate.totalpostprocessing * self.settings.postprocessinglabor

        estimate.totalcost = round(estimate.materialcost + estimate.electriccost, 2)
        estimate.laborprice = round(estimate.totallabor * self.settings.laborcost, 2)
        estimate.totalcostlabor = round(estimate.totalcost + estimate.laborprice, 2)

        estimate.minimumprice = round((estimate.materialprofit + estimate.electricprofit) + estimate.totalcostlabor, 2)
        return estimate

    def _randomDelay(self):
        time.sleep(random.randint(1,5))

    def _getFilamentById(self, id: int):
        return next(iter([ e for e in self.filaments if e.id==id ]), None)
    
    def _getEstimateById(self, id: int):
        return next(iter([ e for e in self.estimates if e.id==id ]), None)
    
    def _getNextId(self, list: list):
        if len(list) > 0:
            return max([c.id for c in list]) + 1
        else:
            return 1