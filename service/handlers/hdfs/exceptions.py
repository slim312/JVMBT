class BaseHdfsException(Exception):
    pass


class HdfsException(BaseHdfsException):
    pass


class HdfsFileSystemError(HdfsException):
    pass


class HdfsUploadError(HdfsFileSystemError):
    pass


class HdfsFileUploadError(HdfsUploadError):
    pass


class HdfsFolderUploadError(HdfsUploadError):
    pass
