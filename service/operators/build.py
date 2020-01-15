from service.factory.BuilderFactory import BuilderFactory
from service.static.config_manager import config


def build(request) -> None:
    builder_factory = BuilderFactory(config_manager=config)
    builder = builder_factory.get_builder(build_type=request.build_type)
    # ////////////////////////////////////////////////////////
    # Generate the local paths needed
    local_path = ""
    # ////////////////////////////////////////////////////////
    cmd = config.commands[request.build_type]
    builder(cmd=cmd, run_file=local_path).build()
