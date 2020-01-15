import yaml
import os


class ConfigManager(object):
    def __init__(self):
        self._config_path = os.path.join(os.getcwd(), "config.yml") if not os.environ.get(
            "config_path") else os.environ.get("config_path")
        self.config = self.__parse_config()

    def __parse_config(self):
        with open(self._config_path) as _config_file:
            return yaml.load(_config_file, Loader=yaml.FullLoader)


config = ConfigManager()
