from ..build import Build


class GradleBuild(Build):
    def __init__(self, gradle_build_cmd, gradle_build_file_path):
        super().__init__(gradle_build_cmd, gradle_build_file_path)

    def build(self):
        pass
