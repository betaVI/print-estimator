from dependency_injector import containers, providers
from server.src import container
from server.src.dataaccess import dataprovider, memoryprovider

from server.src import container, controllers, dataaccess

class Container(containers.DeclarativeContainer):

    config = providers.Configuration()

    db = providers.Singleton(dataprovider.DataProvider)

def create_container(module_name):
    c = Container()
    c.init_resources()
    c.wire(modules=[module_name, container], packages=[ controllers, dataaccess])

    c.config.sqlite.connectionstring.from_env('SQLITE_CONNECTIONSTRING', as_=str, default='')

    c.db.override(providers.Singleton(
        memoryprovider.MemoryProvider
    ))