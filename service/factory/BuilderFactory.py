from service.builds import SbtBuild, MavenBuild, GradleBuild
from service.static import Request


class BuilderFactory(object):
    def __init__(self, request: Request, config_manager):
        self.request = request
        self.config = config_manager
        self.builder = None

    def initialize_builder(self):
        builder = self._get_builder()
        cmd = self.config.commands[self.request.build_type]
        self.builder = builder(cmd=cmd, run_file=self.request.local_path)

    def _get_builder(self):
        builds = {
            "gradle": GradleBuild,
            "maven": MavenBuild,
            "sbt": SbtBuild
        }
        return builds[self.request.build_type]
