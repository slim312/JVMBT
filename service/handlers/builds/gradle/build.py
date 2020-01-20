from subprocess import Popen, PIPE

from ..build import Build


class GradleBuild(Build):
    def __init__(self, gradle_build_cmd, gradle_build_file_path, output_parameter=None):
        super().__init__(gradle_build_cmd, gradle_build_file_path)
        self.output_parameter = output_parameter

    def build(self) -> str:
        cmd = [self.cmd, self.run_file]
        if self.output_parameter:
            cmd.append(self.output_parameter)
        # self.process_executor.execute(cmd=cmd)
        output_jar_location = self.output_parameter.split("=")[-1]
        return output_jar_location
