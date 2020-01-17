import os


class Request(object):
    def __init__(self, input_json: dict):
        self.build_type = input_json['build_type']
        self.git_url = input_json['git_url']
        self.branch = input_json['branch']
        self.transaction_id = input_json['transactionId']
        self.box_id = input_json['boxId']
        self.local_base = self.__get_local_path()
        self.run_script_path = self.__get_run_script_path(input_json['run_script_path'])

    def __get_run_script_path(self, run_script_relative_path: str) -> str:
        # Todo: There is a bug here. For some reason, this line returns C:\\{input_json['run_script_path']}
        # return os.path.join(self.local_base, run_script_relative_path)
        return self.local_base + run_script_relative_path

    def __get_local_path(self) -> str:
        return os.path.join(os.getcwd(), 'tmp', self.transaction_id)
