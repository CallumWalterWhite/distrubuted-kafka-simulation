from dependency_injector import containers, providers
import uuid
from interoperability.broker.ioc.registry.container import RegistryContainer
from interoperability.persistence.persistence_provider import PersistenceProvider

class RepositoryContainer(containers.DeclarativeContainer):
    Repository = PersistenceProvider.getRepo(RegistryContainer.BrokerId)