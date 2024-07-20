from dependency_injector import containers, providers
from src import container
from src.dataaccess import dataprovider, memoryprovider, sqliteprovider

from src import container, controllers, dataaccess

class Container(containers.DeclarativeContainer):

    config = providers.Configuration()

    db = providers.Singleton(dataprovider.DataProvider)

def create_container(module_name):
    c = Container()
    c.init_resources()
    c.wire(modules=[module_name, container], packages=[ controllers, dataaccess])

    c.config.sqlite.connectionstring.from_env('SQLITE_CONNECTIONSTRING', as_=str, default='')

    if c.config.sqlite.connectionstring() != '':
        c.db.override(providers.Singleton(
            sqliteprovider.SqliteProvider,
            connectionstring = c.config.sqlite.connectionstring
        ))
    else:
        c.db.override(providers.Singleton(
            memoryprovider.MemoryProvider
        ))