import sqlite3, traceback

from src.dataaccess.dataprovider import DataProvider
from src.models import estimate, settings, filament, model, customer
from src.models.print import Print

class SqliteProvider(DataProvider):
    def __init__(self, connectionstring: str) -> None:
        self.connectionstring = connectionstring
        super().__init__()

        self._execute("""CREATE TABLE IF NOT EXISTS filaments (
                            id INTEGER PRIMARY KEY,
                            name TEXT NOT NULL,
                            type TEXT NOT NULL,
                            isactive INTEGER NOT NULL,
                            color TEXT NOT NULL,
                            cost REAL NOT NULL,
                            grams INTEGER NOT NULL,
                            UNIQUE (name, type, color) 
                        )""")
        
        self._execute("""CREATE TABLE IF NOT EXISTS estimates (
                            id INTEGER PRIMARY KEY,
                            name TEXT NOT NULL,
                            totalgrams INTEGER NOT NULL,
                            materialcost REAL NOT NULL,
                            totalprints INTEGER NOT NULL,
                            totalprinttime INTEGER NOT NULL,
                            totalpostprocessing INTEGER NOT NULL,
                            totalcolors INTEGER NOT NULL,
                            materialprofit REAL NOT NULL,
                            materialprice REAL NOT NULL,
                            electriccost REAL NOT NULL,
                            electricprofit REAL NOT NULL,
                            electricprice REAL NOT NULL,
                            totallabor REAL NOT NULL,
                            totalcost REAL NOT NULL,
                            laborprice REAL NOT NULL,
                            totalcostlabor REAL NOT NULL,
                            minimumprice REAL NOT NULL,
                            UNIQUE(name)
                        )""")
        
        self._execute("""CREATE TABLE IF NOT EXISTS models(
                            id INTEGER PRIMARY KEY,
                            estimateid INTEGER NOT NULL,
                            filamentid INTEGER NOT NULL,
                            name TEXT NOT NULL,
                            quantity INTEGER NOT NULL,
                            grams INTEGER NOT NULL,
                            minutes INTEGER NOT NULL,
                            postprocessing INTEGER NOT NULL,
                            UNIQUE(estimateid, name, filamentid)
                        )""")
        
        self._execute("""CREATE TABLE IF NOT EXISTS settings(
                            id INTEGER PRIMARY KEY,
                            printablehours INTEGER NOT NULL,
                            laborcost INTEGER NOT NULL,
                            kwhcost REAL NOT NULL,
                            printlabor REAL NOT NULL,
                            colorchangelabor REAL NOT NULL,
                            postprocessinglabor REAL NOT NULL,
                            electricmarkup REAL NOT NULL,
                            materialmarkup REAL NOT NULL
                        )""")
        
        self._execute("""CREATE TABLE IF NOT EXISTS customers(
                            id INTEGER PRIMARY KEY,
                            name TEXT NOT NULL,
                            description TEXT NOT NULL,
                            UNIQUE(name)
                      )""")
        
        self._execute("""CREATE TABLE IF NOT EXISTS prints(
                            id INTEGER PRIMARY KEY,
                            customerid INTEGER NOT NULL,
                            estimateid INTEGER NOT NULL,
                            price REAL NOT NULL,
                            createon real NOT NULL 
                      )""")
        
        self.saveSettings(settings.Settings({
            'printablehours': 16,
            'laborcost': 30,
            'kwhcost': .018,
            'printlabor': .01,
            'colorchangelabor': .03,
            'postprocessinglabor': .05,
            'electricmarkup': .5,
            'materialmarkup': .5
        }))

    def getSettings(self):
        config = self._executeOne("SELECT * from settings limit 1")
        return settings.Settings(dict(config))

    def saveSettings(self, settings: settings.Settings):
        records = self._executeRead('select id from settings')
        if records is not None and len(records) > 0:
            sql = 'update settings set printablehours = ?, laborcost = ?, kwhcost = ?, printlabor = ?,'
            sql += ' colorchangelabor = ?, postprocessinglabor = ?,electricmarkup = ?, materialmarkup = ?'
        else:
            sql = 'insert into settings (printablehours, laborcost, kwhcost, printlabor, colorchangelabor, postprocessinglabor, electricmarkup, materialmarkup) values (?,?,?,?,?,?,?,?)'
        self._execute(sql, (settings.printablehours, settings.laborcost, settings.kwhcost, settings.printlabor, settings.colorchangelabor, settings.postprocessinglabor, settings.electricmarkup, settings.materialmarkup))
    
    def getFilaments(self, id: int = 0):
        sql = 'select * from filaments'
        if id != 0:
            sql += ' where id = ?'
            record = self._executeOne(sql, (id,))
            f = filament.Filament(dict(record))
            f.isactive = True if f.isactive == 1 else False
            return f
        else:
            records = self._executeRead(sql)
            filaments = []
            for r in records:
                f = filament.Filament(dict(r))
                f.isactive = True if f.isactive == 1 else False
                filaments.append(f)
            return filaments

    def createFilament(self, filament: filament.Filament):
        sql = 'insert into filaments (name,type,color,isactive,color,cost,grams)'
        sql += ' values (?,?,?,?,?,?,?)'
        self._execute(sql, (filament.name, filament.type, filament.color, 1 if filament.isactive else 0, filament.color, filament.cost, filament.grams))

    def updateFilament(self, id: int, filament: filament.Filament):
        sql = 'update filaments set name = ?, type = ?, color = ?, isactive = ?, color = ?, cost = ?, grams = ? where id = ?'
        values = (filament.name, filament.type, filament.color, 1 if filament.isactive else 0, filament.color, filament.cost, filament.grams, id)
        self._execute(sql, values)

    def deleteFilament(self, id:int):
        sql = 'delete from filaments where id = ?'
        self._execute(sql, (id,))

    def getCustomers(self, id: int):
        sql = 'select * from customers'
        if id != 0:
            sql += ' where id = ?'
            record = self._executeOne(sql, (id,))
            c = customer.Customer(dict(record))
            return c
        else:
            sql += ' order by name'
            return [customer.Customer(dict(r)) for r in self._executeRead(sql)]
        
    def createCustomer(self, customer: customer.Customer):
        sql = 'insert into customers (name, description) values (?,?)'
        values = (customer.name, customer.description)
        self._execute(sql, values)

    def updateCustomer(self, id:int, customer: customer.Customer):
        sql = 'update customers set name = ?, description = ? where id = ?'
        values = (customer.name, customer.description, id)
        self._execute(sql, values)

    def deleteCustomer(self, id:int):
        sql = 'delete from customers where id = ?'
        self._execute(sql, (id,))

    def getPrints(self, id: int=0):
        sql = 'select id, customerid, estimateid, price, date(createon) as createon from prints'
        if id != 0:
            sql += ' where id = ?'
            record = self._executeOne(sql, (id,))
            return Print(dict(record))
        else:
            sql += ' order by createon desc'
            return [Print(dict(r)) for r in self._executeRead(sql)]
    
    def createPrint(self, print: Print):
        sql = "insert into prints (customerid, estimateid, price, createon) values (?,?,?, julianday(?))"
        values = (print.customerid, print.estimateid, print.price, print.createon)
        self._execute(sql, values)

    def updatePrint(self, id:int, print: Print):
        sql = 'update prints set customerid = ?, estimateid = ?, price = ?, createon = julianday(?) where id = ?'
        values = (print.customerid, print.estimateid, print.price, print.createon, id)
        self._execute(sql, values)

    def deletePrint(self, id:int):
        sql = 'delete from prints where id = ?'
        self._execute(sql, (id,))

    def getEstimates(self, id: int = 0):
        sql = 'select * from estimates'
        if id != 0:
            sql += ' where id = ?'
            record = self._executeOne(sql,(id,))
            e = estimate.Estimate(dict(record))
            e.models = self._getModels(e.id)
            return e
        else:
            return [estimate.Estimate(dict(r)) for r in self._executeRead(sql)]
        
    def createEstimate(self, estimate: estimate.Estimate):
        self._populateEstimateFields(estimate)
        sql = 'insert into estimates (name, totalgrams, materialcost, totalprints, totalprinttime, totalpostprocessing, totalcolors, materialprofit, materialprice,'
        sql += ' electriccost, electricprofit, electricprice, totallabor, totalcost, laborprice, totalcostlabor, minimumprice) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?) RETURNING id'
        values = (
            estimate.name, 
            estimate.totalgrams, 
            estimate.materialcost, 
            estimate.totalprints, 
            estimate.totalprinttime, 
            estimate.totalpostprocessing,
            estimate.totalcolors,
            estimate.materialprofit,
            estimate.materialprice,
            estimate.electriccost,
            estimate.electricprofit,
            estimate.electricprice,
            estimate.totallabor,
            estimate.totalcost,
            estimate.laborprice,
            estimate.totalcostlabor,
            estimate.minimumprice
            )
        print('QUERY: ' + sql)
        print('VALUES: ' + str(values))
        lastid = self._executeOne(sql,values)
        print('RESULT: ' + str(lastid))
        self._createModels(lastid['id'], estimate.models)

    def updateEstimate(self, id: int, estimate: estimate.Estimate):
        self._populateEstimateFields(estimate)
        sql = 'update estimates set name = ?, totalgrams = ?, materialcost = ?, totalprints = ?, totalprinttime = ?, totalpostprocessing = ?, totalcolors = ?, '
        sql += 'materialprofit = ?, materialprice = ?, electriccost = ?, electricprofit = ?, electricprice = ?, totallabor = ?, totalcost = ?, '
        sql += 'laborprice = ?, totalcostlabor = ?, minimumprice = ? where id = ?'
        values = (
            estimate.name, 
            estimate.totalgrams, 
            estimate.materialcost, 
            estimate.totalprints, 
            estimate.totalprinttime, 
            estimate.totalpostprocessing,
            estimate.totalcolors,
            estimate.materialprofit,
            estimate.materialprice,
            estimate.electriccost,
            estimate.electricprofit,
            estimate.electricprice,
            estimate.totallabor,
            estimate.totalcost,
            estimate.laborprice,
            estimate.totalcostlabor,
            estimate.minimumprice,
            id
            )
        self._execute(sql, values)
        self._deleteModels(id)
        self._createModels(id, estimate.models)

    def deleteEstimate(self, id: int):
        sql = 'delete from estimates where id = ?'
        self._execute(sql, (id,))
        self._deleteModels(id)

    def _deleteModels(self, estimateid: int):
        sql = 'delete from models where estimateid = ?'
        self._execute(sql, (estimateid,))

    def _getModels(self, estimateid: int) -> list[model.Model]:
        sql = 'select * from models where estimateid = ?'
        values = (estimateid,)
        return [model.Model(dict(r)) for r in self._executeRead(sql,values)]

    def _createModels(self, estimateid: int, models: list[model.Model]):
        for m in models:
            sql = 'insert into models (estimateid, filamentid, name, quantity, grams, minutes, postprocessing) VALUES (?,?,?,?,?,?,?)'
            values = (
                estimateid,
                m.filamentid,
                m.name,
                m.quantity,
                m.grams,
                m.minutes,
                1 if m.postprocessing else 0
            )
            self._execute(sql, values)

    def _executeRead(self, statement, values=None) -> list:
        with self._createConnection() as conn:
            c = conn.cursor()
            try:
                if values is None:
                    c.execute(statement)
                else:
                    c.execute(statement, values)
                records = c.fetchall()
                return records
            except Exception as e:
                print(f'Sqlite ExecuteRead error {traceback.format_exc()}')

    def _executeOne(self, statement, values=None):
        with self._createConnection() as conn:
            c = conn.cursor()
            try:
                if values is None:
                    c.execute(statement)
                else:
                    c.execute(statement, values)
                record = c.fetchone()
                return record
            except Exception as e:
                print(f'Sqlite Execute One error {traceback.format_exc()}')

    def _execute(self, statement, values=None) -> None:
        with self._createConnection() as conn:
            c = conn.cursor()
            try:
                if values == None:
                    c.execute(statement)
                else:
                    c.execute(statement, values)
            except Exception as e:
                print(f'Sqlite Execute error {traceback.format_exc()}')

    def _createConnection(self) -> sqlite3.Connection:
        connection = None
        try:
            connection = sqlite3.connect(self.connectionstring)
            connection.row_factory = sqlite3.Row
        except Exception as e:
            print(f'Sqlite Connection error {traceback.format_exc()}')
        return connection

    def _populateEstimateFields(self, estimate: estimate.Estimate) -> estimate.Estimate:
        config = self.getSettings()
        filamentused = {}
        estimate.totalgrams = 0
        estimate.materialcost = 0
        estimate.totalprints = 0
        estimate.totalprinttime = 0
        estimate.totalpostprocessing = 0
        for m in estimate.models:
            if m.filamentid not in filamentused:
                f = self.getFilaments(m.filamentid)
                filamentused[m.filamentid] = f.cost / f.grams
            m.totalcost = round(filamentused[m.filamentid] * m.grams * m.quantity, 2)
            estimate.totalgrams += m.grams * m.quantity
            estimate.materialcost += m.totalcost
            estimate.totalprints += m.quantity
            estimate.totalprinttime += m.quantity * m.minutes
            estimate.totalpostprocessing += m.quantity if m.postprocessing else 0

        estimate.totalcolors = len(filamentused)

        estimate.materialprofit = round(estimate.materialcost * config.materialmarkup, 2)
        estimate.materialprice = estimate.materialcost + estimate.materialprofit

        estimate.electriccost = round((estimate.totalprinttime / 60) * config.kwhcost, 2)
        estimate.electricprofit = round(estimate.electriccost * config.electricmarkup, 2)
        estimate.electricprice = estimate.electriccost + estimate.electricprofit

        estimate.totallabor = estimate.totalprints * config.printlabor
        estimate.totallabor += estimate.totalcolors * config.colorchangelabor
        estimate.totallabor += estimate.totalpostprocessing * config.postprocessinglabor

        estimate.totalcost = round(estimate.materialcost + estimate.electriccost, 2)
        estimate.laborprice = round(estimate.totallabor * config.laborcost, 2)
        estimate.totalcostlabor = round(estimate.totalcost + estimate.laborprice, 2)

        estimate.minimumprice = round((estimate.materialprofit + estimate.electricprofit) + estimate.totalcostlabor, 2)
        return estimate