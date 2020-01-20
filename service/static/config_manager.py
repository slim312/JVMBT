import yaml
import os


class ConfigManager(object):
    def __init__(self, env):
        self._config_path = os.path.join(os.getcwd(), "config.yml") if not os.environ.get(
            "config_path") else os.environ.get("config_path")
        self.config = self.__parse_config()
        self.environment = env

    def __parse_config(self):
        with open(self._config_path) as _config_file:
            return yaml.load(_config_file, Loader=yaml.FullLoader)

    @property
    def build_commands(self):
        return self.config['commands']['build']["main_command"]

    @property
    def additional_commands(self):
        return self.config['commands']['build']["additional_commands"]

    def output_path_flag(self, path, build_type):
        return self.config['commands']['build']["additional_commands"]["output_path"][build_type].format(out=path)

    @property
    def rebuild_commands(self):
        """
        The reason behind this method is that these tools have built-in
        optimization for recompiling projects, therefore we should utilize
        this capability to improve runtime (Different from build_commands
        that are for first time compilation of a project).
        """
        return self.config['commands']['rebuild']

    def get_namenode(self) -> tuple:
        # This is just for debug
        namenode = {
            "prod": {
                "host": "prod_host",
                "port": "prod_port"
            }, "test": {
                "host": "test_host",
                "port": "test_port"
            }, "dev": {
                "host": "dev_host",
                "port": "dev_port"
            }
        }
        return namenode[self.environment]["host"], namenode[self.environment]["port"]

    def get_admin_user(self) -> tuple:
        user_and_pwd = {
            "prod": {
                "user": "prod_user",
                "pwd": "prod_pwd"
            }, "test": {
                "user": "test_user",
                "pwd": "test_pwd"
            }, "dev": {
                "user": "dev_user",
                "pwd": "dev_pwd"
            }
        }
        return user_and_pwd[self.environment]["user"], user_and_pwd[self.environment]["pwd"]

    def get_hdfs_base_path(self):
        return self.config["general"]["paths"]["hdfs"][self.environment]['base_hdfs_path']


config = ConfigManager("dev")
