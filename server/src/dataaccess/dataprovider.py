from server.src.models import model, estimate

class DataProvider:

    def getEstimates(self, id: int = 0):
        pass

    def createEstimate(self, estimate: estimate.Estimate):
        pass

    def updateEstimate(self, id: int, estimate: estimate.Estimate):
        pass

    def deleteEstimate(self, id: int):
        pass

    def getModelsForEstimate(self, estimateid: int):
        pass

    def createModelForEstimate(self, estimateid: int, model: model.Model):
        pass

    def updateModel(self, estimateid: int, modelid: int, model: model.Model):
        pass
    
    def deleteModel(self, modelid: int):
        pass