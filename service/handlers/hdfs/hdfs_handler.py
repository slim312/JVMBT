from hdfs.ext.kerberos import KerberosClient
import logging
import os

# Internal packages:
from service.static import create_kerberos_token
from .exceptions import *

logger = logging.getLogger(__name__)
HDFS_PATH_DELIMITER = "/"
ROOT = "/"
ADDRESS_URL = "http://{namenode}:{port}"


class HdfsHandler(object):
    def __init__(self, host, port, user, pwd=None, token=None):
        self.nn_host = host
        self.nn_port = port
        self.user = user
        self.pwd = pwd
        self.__token = token if token else create_kerberos_token(username=self.user, pwd=self.pwd)

    def __enter__(self):
        address = ADDRESS_URL.format(namenode=self.nn_host, port=self.nn_port)
        self.conn = KerberosClient(address, self.__token)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        try:
            logger.debug(f"Closing connection with HDFS namenode: {self.nn_host}:{self.nn_port}")
            self.conn.disconnect()
        except Exception as e:
            logger.warning(f"Error occurred while closing connection to HDFS namenode: {e}")

    def __create_directory_tree(self, leaf_dir: str) -> None:
        path_parts = leaf_dir.split(HDFS_PATH_DELIMITER)
        build_path = ROOT
        for section in path_parts:
            build_path = HDFS_PATH_DELIMITER.join([build_path, section])
            if not self.conn.exists(build_path):
                self.conn.makedirs(hdfs_path=build_path)
            elif not self.conn.isdir(path=build_path):
                raise FileExistsError(f"Path {build_path} already exists as a file!")

    @staticmethod
    def __get_hdfs_parent_dir(path: str) -> str:
        return HDFS_PATH_DELIMITER.join(path.split(HDFS_PATH_DELIMITER)[:-1])

    @staticmethod
    def __get_file_name_from_path(path):
        return path.split(HDFS_PATH_DELIMITER)[-1]

    def upload_file(self, local_path: str, hdfs_path: str, overwrite=True) -> None:
        self.__create_directory_tree(leaf_dir=self.__get_hdfs_parent_dir(path=hdfs_path))
        # filename = self.__get_file_name_from_path(path=local_path)
        # if self.conn.exists(path=hdfs_path):
        #     raise HdfsUploadError(f"File {filename} already exists at location {hdfs_path}!")
        if not os.path.exists(local_path):
            raise FileNotFoundError(f"Local file {local_path} not found!")
        self.conn.upload(local_path=local_path, hdfs_path=hdfs_path, overwrite=overwrite)

    def upload_folder(self, local_folder_path: str, hdfs_path: str, overwrite=True) -> None:
        self.conn.upload(local_path=local_folder_path, hdfs_path=hdfs_path, overwrite=overwrite)
