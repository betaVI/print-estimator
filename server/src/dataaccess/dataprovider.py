from src.models import model, estimate, filament, settings, customer, print

class DataProvider:

    def getSettings(self):
        pass

    def saveSettings(self, settings: settings.Settings):
        pass
    
    def getFilaments(self, id: int = 0):
        pass

    def createFilament(self, filament: filament.Filament):
        pass

    def updateFilament(self, id: int, filament: filament.Filament):
        pass

    def deleteFilament(self, id:int):
        pass

    def getCustomers(self, id: int = 0):
        pass

    def createCustomer(self, customer: customer.Customer):
        pass

    def updateCustomer(self, id: int, customer: customer.Customer):
        pass

    def deleteCustomer(self, id: int):
        pass

    def getPrints(self, id: int = 0):
        pass

    def createPrint(self, print: print.Print):
        pass

    def updatePrint(self, id: int, print: print.Print):
        pass
    
    def deletePrint(self, id: int):
        pass

    def getEstimates(self, id: int = 0):
        pass

    def createEstimate(self, estimate: estimate.Estimate):
        pass

    def updateEstimate(self, id: int, estimate: estimate.Estimate):
        pass

    def deleteEstimate(self, id: int):
        pass