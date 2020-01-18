from service.handlers.builds import SbtBuild, MavenBuild, GradleBuild
from service.static import Request


class BuilderFactory(object):
    def __init__(self, request: Request, config_manager):
        self.request = request
        self.config = config_manager
        # self.builder = None

    def get_builder(self):
        builder = self._get_builder_type()
        cmd = self.config.build_commands[self.request.build_type]
        # self.builder = builder(cmd, self.request.run_script_path)
        return builder(cmd, self.request.run_script_path)

    def _get_builder_type(self):
        builds = {
            "gradle": GradleBuild,
            "maven": MavenBuild,
            "sbt": SbtBuild
        }
        return builds[self.request.build_type]
