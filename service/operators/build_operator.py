from service.handlers import BuilderFactory, GitHandler
from service.static.config_manager import config
from service.static import Request


def run_build(request: Request) -> None:
    builder = BuilderFactory(request=request, config_manager=config).get_builder()
    git_handler = GitHandler(url=request.git_url, branch=request.branch, target_location=request.local_base)
    git_handler.clone()
    builder.build()
