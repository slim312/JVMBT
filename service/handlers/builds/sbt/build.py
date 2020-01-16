from ..build import Build


class SbtBuild(Build):
    def __init__(self, sbt_build_cmd, sbt_build_file_path):
        super().__init__(sbt_build_cmd, sbt_build_file_path)

    def build(self):
        pass
