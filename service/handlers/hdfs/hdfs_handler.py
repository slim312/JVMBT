from hdfs.ext.kerberos import KerberosClient
import logging
import os

# Internal packages:
from service.static import create_kerberos_token, HDFS_PATH_DELIMITER, ROOT
from .exceptions import *

logger = logging.getLogger(__name__)
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

    def upload_file(self, local_path: str, hdfs_path: str, overwrite: bool) -> None:
        self.__create_directory_tree(leaf_dir=self.__get_hdfs_parent_dir(path=hdfs_path))
        if not os.path.exists(local_path):
            raise FileNotFoundError(f"Local file {local_path} not found!")
        self.conn.upload(local_path=local_path, hdfs_path=hdfs_path, overwrite=overwrite)

    def upload_folder(self, local_folder_path: str, hdfs_path: str, overwrite=True) -> None:
        self.conn.upload(local_path=local_folder_path, hdfs_path=hdfs_path, overwrite=overwrite)


def upload_folder_to_hdfs(config, environment, local_path, hdfs_path, overwrite=True):
    logger.info(f"Uploading {local_path} to {hdfs_path}...")
    logger.debug(f"Environment: {environment}, overwrite: {overwrite}")
    nn_host, nn_port = config.get_namenode()
    admin_user, admin_pwd = config.get_admin_user()
    with HdfsHandler(
            host=nn_host,
            port=nn_port,
            user=admin_user,
            token=create_kerberos_token(username=admin_user, pwd=admin_pwd)
    ) as hdfs:
        logger.debug(f"HdfsHandler Created: {hdfs.nn_host}:{hdfs.nn_port} with user {hdfs.user}")
        hdfs.upload_folder(
            local_folder_path=local_path,
            hdfs_path=hdfs_path,
            overwrite=overwrite
        )
    logger.info(f"Jar's upload to {hdfs_path} complete!")
