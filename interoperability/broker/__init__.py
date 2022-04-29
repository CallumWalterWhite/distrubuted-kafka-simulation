from interoperability.broker.broker import Broker
from interoperability.broker.ioc.container import Container
application = Container()
application.wire(modules=[__name__])