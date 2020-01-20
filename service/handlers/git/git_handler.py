from git import Repo
import os


class GitHandler(object):
    def __init__(self, url, branch, target_location):
        self._url = url
        self._branch = branch
        self._local_target_location = target_location

    def clone(self):
        if not os.path.exists(self._local_target_location):
            os.makedirs(self._local_target_location)
        repo = Repo.clone_from(url=self._url, to_path=self._local_target_location, branch=self._branch)
        return self._local_target_location

    @property
    def local_base_path(self):
        return self._local_target_location
