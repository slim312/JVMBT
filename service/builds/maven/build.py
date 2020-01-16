from ..build import Build


class MavenBuild(Build):
    def __init__(self, maven_build_cmd, pom_xml_path):
        super().__init__(maven_build_cmd, pom_xml_path)

    def build(self):
        pass
