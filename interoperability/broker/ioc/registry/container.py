from dependency_injector import containers
import uuid

class RegistryContainer(containers.DeclarativeContainer):
    BrokerId = uuid.uuid4()