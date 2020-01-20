from ..build import Build


class SbtBuild(Build):
    def __init__(self, sbt_build_cmd, sbt_build_file_path, output_parameter=None):
        super().__init__(sbt_build_cmd, sbt_build_file_path)
        self.output_parameter = output_parameter

    def build(self) -> str:
        cmd = [self.cmd, self.run_file]
        if self.output_parameter:
            cmd.append(self.output_parameter)
        self.process_executor.execute(cmd=cmd)
        output_jar_location = self.output_parameter.split("=")[-1]
        return output_jar_location
