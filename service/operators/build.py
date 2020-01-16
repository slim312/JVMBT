from service.factory.BuilderFactory import BuilderFactory
from service.static.config_manager import config
from service.static import Request


def run_build(request: Request) -> None:
    builder = BuilderFactory(request=request, config_manager=config).initialize_builder()
    builder.build()
