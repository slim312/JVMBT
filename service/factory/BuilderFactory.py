from service.builds import SbtBuild, MavenBuild, GradleBuild


class BuilderFactory(object):
    def __init__(self, config_manager):
        self.config_manager = config_manager

    def get_builder(self, build_type):
        builds = {
            "gradle": GradleBuild,
            "maven": MavenBuild,
            "sbt": SbtBuild
        }
        return builds[build_type]
