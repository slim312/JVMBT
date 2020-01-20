import os

# Internal packages:
# from service.static import HDFS_PATH_DELIMITER
HDFS_PATH_DELIMITER = "/"


class Request(object):
    def __init__(self, input_args, config):
        self.build_type = input_args.build_type
        self.git_url = input_args.git_url
        self.branch = input_args.branch
        self.transaction_id = input_args.transactionId
        self.box_id = input_args.boxId
        self.local_base = self.__get_local_path()
        self.run_script_path = self.__get_run_script_path(input_args.run_script_path)
        self.environment = input_args.environment
        self.config = config
        self.hdfs_path = self.__get_hdfs_location()

    def __get_run_script_path(self, run_script_relative_path: str) -> str:
        # Todo: There is a bug here. For some reason, this line returns C:\\{input_json['run_script_path']}
        # return os.path.join(self.local_base, run_script_relative_path)
        return self.local_base + run_script_relative_path

    def __get_local_path(self) -> str:
        return os.path.join(os.getcwd(), 'tmp', self.transaction_id)

    def __get_hdfs_location(self) -> str:
        hdfs_base_path = self.config.get_hdfs_base_path()
        return HDFS_PATH_DELIMITER.join([hdfs_base_path, self.box_id, "jars"])

    def get_tmp_out_folder(self):
        return os.path.join(self.local_base, "out", self.transaction_id)
