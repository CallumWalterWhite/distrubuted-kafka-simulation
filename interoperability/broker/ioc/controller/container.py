from dependency_injector import containers, providers

from interoperability.broker.controller.controllerService import ControllerService
from interoperability.broker.ioc.registry.container import RegistryContainer
from interoperability.broker.ioc.repository.container import RepositoryContainer

class ControllerContainer(containers.DeclarativeContainer):
    controller = providers.Factory(
        ControllerService,
        Id = RegistryContainer.BrokerId,
        Repo = RepositoryContainer.Repository
    )