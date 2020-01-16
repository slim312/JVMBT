from git import Repo


class GitHandler(object):
    def __init__(self, url, branch, target_location):
        self._url = url
        self._branch = branch
        self._target_location = target_location

    def clone(self):
        repo = Repo.clone_from(url=self._url, to_path=self._target_location, branch=self._branch)
        return self._target_location
